"""
LangGraph Orchestrator — Unified Multi-Agent Regulatory & Patent Intelligence Engine.
"""

import json
from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from groq import Groq
from src.models.chat import (
    ClassifierOutput, 
    FinalResponse, 
    SourceCitation, 
    ComplianceAlert
)
from .classifier import classifier_agent
from src.rag.retriever import hybrid_retriever
from src.config.settings import settings

class GraphState(TypedDict):
    query: str
    jurisdiction: str
    language: str
    classification: Optional[ClassifierOutput]
    retrieved_context: List[Dict[str, Any]]
    final_response: Optional[FinalResponse]

def classify_node(state: GraphState) -> Dict[str, Any]:
    classification = classifier_agent.classify(state["query"])
    return {"classification": classification}

def retrieve_node(state: GraphState) -> Dict[str, Any]:
    context = hybrid_retriever.retrieve(state["query"], state["jurisdiction"], top_k=6)
    return {"retrieved_context": context}

def synthesize_node(state: GraphState) -> Dict[str, Any]:
    category = state["classification"].category if state["classification"] else "PROPRIETARY_AYURVEDA"
    base_conf = state["classification"].confidence if state["classification"] else 0.85
    jurisdiction = state.get("jurisdiction", "india")
    
    # Format context for synthesis
    context_chunks = []
    for doc in state["retrieved_context"]:
        src = doc["metadata"].get("source_name", "Statutory Source")
        sec = doc["metadata"].get("category", "")
        content = doc["content"][:450]
        context_chunks.append(f"[{src} | {sec}]\n{content}")
    context_str = "\n\n".join(context_chunks)

    client = Groq(api_key=settings.groq_api_key)
    
    system_prompt = f"""You are IP-SHAKTI, the apex Ministry of Ayush & Indian Patent Office Regulatory Intelligence Engine.
You are evaluating a formulation categorized as: {category} under {jurisdiction.upper()} jurisdiction.

Analyze the innovation against the retrieved legal context.
You MUST output a valid JSON object strictly matching this schema:
{{
  "regulatory_pathway": "Comprehensive explanation of the CDSCO/AYUSH/FSSAI licensing and regulatory approval route.",
  "key_requirements": [
    "Requirement 1: Specific testing, standardization, or dossier milestone",
    "Requirement 2: Specific clinical or quality standard"
  ],
  "ip_options": [
    "Option 1: Specific patent, trade secret, or trademark strategy",
    "Option 2: International PCT or ABS filing strategy"
  ],
  "compliance_alerts": [
    {{
      "check_name": "Section 3(p) Traditional Knowledge Bar",
      "status": "CLEAR",
      "reason": "Detailed legal reasoning based on Section 3(p) and synergy proof."
    }},
    {{
      "check_name": "Section 3(d) & 3(e) Enhanced Efficacy & Synergy",
      "status": "CLEAR",
      "reason": "Detailed legal analysis under Section 3(d)/3(e)."
    }},
    {{
      "check_name": "Biological Diversity Act 2002 (ABS / NBA Compliance)",
      "status": "CLEAR",
      "reason": "Evaluation of NBA approval (Section 3/6) or SBB intimation (Section 7)."
    }},
    {{
      "check_name": "TKDL Prior Art & Novelty Check",
      "status": "CLEAR",
      "reason": "Evaluation against Traditional Knowledge Digital Library prior art."
    }}
  ],
  "sources": [
    {{
      "name": "Drugs and Cosmetics Act / Patents Act / Biological Diversity Act",
      "section": "Rule 122E / Section 3(p) / Section 7",
      "text": "Applicable statutory summary"
    }}
  ]
}}"""

    user_prompt = f"INNOVATION QUERY & PROFILE:\n{state['query']}\n\nRETRIEVED STATUTORY CONTEXT:\n{context_str}"

    regulatory_pathway = ""
    key_requirements: List[str] = []
    ip_options: List[str] = []
    compliance_alerts: List[ComplianceAlert] = []
    sources: List[SourceCitation] = []

    try:
        chat = client.chat.completions.create(
            model=settings.groq_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        data = json.loads(chat.choices[0].message.content)
        
        regulatory_pathway = data.get("regulatory_pathway", "Regulatory assessment synthesized from applicable statutory guidelines.")
        key_requirements = data.get("key_requirements", [])
        ip_options = data.get("ip_options", [])
        
        for raw_alert in data.get("compliance_alerts", []):
            try:
                compliance_alerts.append(ComplianceAlert.model_validate(raw_alert))
            except Exception:
                pass

        for raw_source in data.get("sources", []):
            try:
                sources.append(SourceCitation.model_validate(raw_source))
            except Exception:
                pass

    except Exception as e:
        print(f"Synthesis engine error: {repr(e)}")
        regulatory_pathway = "Formulation evaluated under standard AYUSH and Indian Patent Office statutory requirements."
        key_requirements = [
            "Rule 158B / Rule 122E standardization dossier submission",
            "State Licensing Authority Form 24D/25D manufacturing application",
            "Access and Benefit Sharing intimation under Biological Diversity Act, 2002"
        ]
        ip_options = [
            "File Indian Process & Product Patent application at IPO",
            "Protect proprietary trade secret formulation and register brand trademark"
        ]
        compliance_alerts = [
            ComplianceAlert(check_name="Section 3(p) TKDL Check", status="REVIEW", reason="Synergy data required to overcome traditional knowledge obviousness bar."),
            ComplianceAlert(check_name="Biological Diversity Act 2002", status="CLEAR", reason="State Biodiversity Board intimation mandatory prior to commercial utilization.")
        ]
        sources = [
            SourceCitation(name="Patents Act 1970", section="Section 3(p)"),
            SourceCitation(name="Biological Diversity Act 2002", section="Section 7")
        ]

    # Build rich formatted markdown sections
    sections = []
    if regulatory_pathway:
        sections.append(f"### 📋 Regulatory Pathway\n{regulatory_pathway}")
    
    if key_requirements:
        req_list = "\n".join([f"- {req}" for req in key_requirements])
        sections.append(f"### ⚙️ Key Regulatory Requirements\n{req_list}")
        
    if ip_options:
        ip_list = "\n".join([f"- {opt}" for opt in ip_options])
        sections.append(f"### 💡 Intellectual Property Protection Options\n{ip_list}")

    if compliance_alerts:
        comp_summary = []
        for alert in compliance_alerts:
            status_emoji = "✅" if alert.status == "CLEAR" else ("⚠️" if alert.status == "REVIEW" else "❌")
            comp_summary.append(f"- **{alert.check_name}** [{status_emoji} `{alert.status}`]: {alert.reason}")
        sections.append(f"### ⚖️ Statutory & Compliance Evaluation\n" + "\n".join(comp_summary))

    guidance = "\n\n".join(sections)

    # Weighted confidence score
    confidence_penalty = 0.0
    for alert in compliance_alerts:
        if alert.status == "FAIL":
            confidence_penalty += 0.10
        elif alert.status == "REVIEW":
            confidence_penalty += 0.03
            
    citation_bonus = 0.05 if len(sources) > 0 else 0.0
    overall_conf = round(max(0.30, min(0.98, base_conf - confidence_penalty + citation_bonus)), 2)

    final_resp = FinalResponse(
        classification=category,
        jurisdiction=jurisdiction,
        guidance_text=guidance,
        compliance_alerts=compliance_alerts,
        sources=sources,
        overall_confidence=overall_conf
    )
    return {"final_response": final_resp}

# Build the Graph
workflow = StateGraph(GraphState)
workflow.add_node("classify", classify_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("synthesize", synthesize_node)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "synthesize")
workflow.add_edge("synthesize", END)

orchestrator = workflow.compile()
