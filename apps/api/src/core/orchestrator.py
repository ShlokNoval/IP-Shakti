"""
LangGraph Orchestrator — The brain of IP-SHAKTI.
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from src.models.chat import ClassifierOutput, FinalResponse, SourceCitation, ComplianceAlert, DomainAgentOutput, EngineOutput
from .classifier import classifier_agent
from src.rag.retriever import hybrid_retriever

# Import all agents and engines
from .agents.ayurvedic_medicine_agent import ayurvedic_medicine_agent
from .agents.phytopharmaceutical_agent import phytopharmaceutical_agent
from .agents.new_drug_agent import new_drug_agent
from .agents.cosmetics_agent import cosmetics_agent
from .agents.ayurveda_aahar_agent import ayurveda_aahar_agent

from .engines.section3_evaluator import section3_evaluator
from .engines.abs_compliance import abs_compliance_engine
from .engines.prior_art_checker import prior_art_checker

class GraphState(TypedDict):
    query: str
    jurisdiction: str
    language: str
    classification: Optional[ClassifierOutput]
    retrieved_context: List[Dict[str, Any]]
    
    # Outputs from specialized agents
    domain_output: Optional[DomainAgentOutput]
    engine_outputs: List[EngineOutput]
    
    final_response: Optional[FinalResponse]

def classify_node(state: GraphState) -> Dict[str, Any]:
    classification = classifier_agent.classify(state["query"])
    return {"classification": classification}

def retrieve_node(state: GraphState) -> Dict[str, Any]:
    context = hybrid_retriever.retrieve(state["query"], state["jurisdiction"])
    return {"retrieved_context": context}

def run_agents_node(state: GraphState) -> Dict[str, Any]:
    """Routes to the correct domain agent based on classification, and runs all compliance engines in parallel."""
    category = state["classification"].category if state["classification"] else "UNCLEAR"
    
    # Format context for agents
    context_str = "\n".join([doc["content"] for doc in state["retrieved_context"]])
    
    import concurrent.futures

    domain_agent_runner = None
    if category in ["CLASSICAL_AYURVEDA", "PROPRIETARY_AYURVEDA"]:
        domain_agent_runner = ayurvedic_medicine_agent.analyze
    elif category == "PHYTOPHARMACEUTICAL":
        domain_agent_runner = phytopharmaceutical_agent.analyze
    elif category == "NEW_DRUG":
        domain_agent_runner = new_drug_agent.analyze
    elif category == "COSMETIC":
        domain_agent_runner = cosmetics_agent.analyze
    elif category == "AYURVEDA_AAHAR":
        domain_agent_runner = ayurveda_aahar_agent.analyze

    domain_out = None
    sec3_out = None
    abs_out = None
    prior_art_out = None

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {}
        if domain_agent_runner:
            futures["domain"] = executor.submit(domain_agent_runner, state["query"], context_str)
        futures["sec3"] = executor.submit(section3_evaluator.evaluate, state["query"], context_str)
        futures["abs"] = executor.submit(abs_compliance_engine.evaluate, state["query"], context_str)
        futures["prior_art"] = executor.submit(prior_art_checker.evaluate, state["query"], context_str)
        
        if "domain" in futures:
            try:
                domain_out = futures["domain"].result()
            except Exception as e:
                print(f"Domain agent error: {repr(e)}")
                
        try:
            sec3_out = futures["sec3"].result()
        except Exception as e:
            print(f"Sec3 engine error: {repr(e)}")
            
        try:
            abs_out = futures["abs"].result()
        except Exception as e:
            print(f"ABS engine error: {repr(e)}")
            
        try:
            prior_art_out = futures["prior_art"].result()
        except Exception as e:
            print(f"Prior art engine error: {repr(e)}")

    engine_outputs = [out for out in [sec3_out, abs_out, prior_art_out] if out is not None]
    
    return {
        "domain_output": domain_out,
        "engine_outputs": engine_outputs
    }

def synthesize_node(state: GraphState) -> Dict[str, Any]:
    category = state["classification"].category if state["classification"] else "UNCLEAR"
    base_conf = state["classification"].confidence if state["classification"] else 0.5
    
    # Aggregate compliance alerts
    alerts = []
    for eng_out in state["engine_outputs"]:
        alerts.extend(eng_out.checks)
        
    # Aggregate sources
    sources = []
    sections = []
    
    if state["domain_output"]:
        sources.extend(state["domain_output"].citations)
        
        # 1. Regulatory Pathway
        if state["domain_output"].regulatory_pathway:
            sections.append(f"### 📋 Regulatory Pathway\n{state['domain_output'].regulatory_pathway}")
            
        # 2. Key Requirements
        if state["domain_output"].key_requirements:
            req_list = "\n".join([f"- {req}" for req in state["domain_output"].key_requirements])
            sections.append(f"### ⚙️ Key Regulatory Requirements\n{req_list}")
            
        # 3. IP Options
        if state["domain_output"].ip_options:
            ip_list = "\n".join([f"- {opt}" for opt in state["domain_output"].ip_options])
            sections.append(f"### 💡 Intellectual Property Protection Options\n{ip_list}")
    else:
        sections.append("### 📋 Regulatory Assessment\nClassification required further clarification or manual verification. Escalation to an Ayush/IP legal expert is recommended.")

    # 4. Synthesized Compliance Analysis
    if alerts:
        comp_summary = []
        for alert in alerts:
            status_emoji = "✅" if alert.status == "CLEAR" else ("⚠️" if alert.status == "REVIEW" else "❌")
            comp_summary.append(f"- **{alert.check_name}** [{status_emoji} `{alert.status}`]: {alert.reason}")
        sections.append(f"### ⚖️ Statutory & Compliance Evaluation\n" + "\n".join(comp_summary))

    guidance = "\n\n".join(sections)

    # Weighted confidence score
    confidence_penalty = 0.0
    for alert in alerts:
        if alert.status == "FAIL":
            confidence_penalty += 0.10
        elif alert.status == "REVIEW":
            confidence_penalty += 0.03
            
    citation_bonus = 0.05 if len(sources) > 0 else 0.0
    overall_conf = round(max(0.30, min(0.98, base_conf - confidence_penalty + citation_bonus)), 2)

    final_resp = FinalResponse(
        classification=category,
        jurisdiction=state["jurisdiction"],
        guidance_text=guidance,
        compliance_alerts=alerts,
        sources=sources,
        overall_confidence=overall_conf
    )
    return {"final_response": final_resp}


# Build the Graph
workflow = StateGraph(GraphState)

workflow.add_node("classify", classify_node)
workflow.add_node("retrieve", retrieve_node)
workflow.add_node("run_agents", run_agents_node)
workflow.add_node("synthesize", synthesize_node)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "retrieve")
workflow.add_edge("retrieve", "run_agents")
workflow.add_edge("run_agents", "synthesize")
workflow.add_edge("synthesize", END)

orchestrator = workflow.compile()
