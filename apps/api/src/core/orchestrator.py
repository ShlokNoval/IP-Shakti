"""
LangGraph Orchestrator — The brain of IP-SHAKTI.
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from ...models.chat import ClassifierOutput, FinalResponse, SourceCitation, ComplianceAlert, DomainAgentOutput, EngineOutput
from .classifier import classifier_agent
from ..rag.retriever import hybrid_retriever

# Import all agents and engines
from .agents.ayurvedic_medicine_agent import ayurvedic_medicine_agent
from .agents.phytopharmaceutical_agent import phytopharmaceutical_agent
from .agents.new_drug_agent import new_drug_agent
from .agents.cosmetics_agent import cosmetics_agent
from .agents.ayurveda_aahar_agent import ayurveda_aahar_agent

from .engines.section3_evaluator import section3_evaluator
from .engines.abs_compliance import abs_compliance
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
    """Routes to the correct domain agent based on classification, and runs all compliance engines."""
    category = state["classification"].category if state["classification"] else "UNCLEAR"
    
    # Format context for agents
    context_str = "\n".join([doc["content"] for doc in state["retrieved_context"]])
    
    # 1. Run Domain Agent
    domain_out = None
    if category in ["CLASSICAL_AYURVEDA", "PROPRIETARY_AYURVEDA"]:
        domain_out = ayurvedic_medicine_agent.analyze(state["query"], context_str)
    elif category == "PHYTOPHARMACEUTICAL":
        domain_out = phytopharmaceutical_agent.analyze(state["query"], context_str)
    elif category == "NEW_DRUG":
        domain_out = new_drug_agent.analyze(state["query"], context_str)
    elif category == "COSMETIC":
        domain_out = cosmetics_agent.analyze(state["query"], context_str)
    elif category == "AYURVEDA_AAHAR":
        domain_out = ayurveda_aahar_agent.analyze(state["query"], context_str)
        
    # 2. Run Compliance Engines (Parallelizable, but sequential here for simplicity)
    sec3_out = section3_evaluator.evaluate(state["query"], context_str)
    abs_out = abs_compliance.evaluate(state["query"], context_str)
    prior_art_out = prior_art_checker.evaluate(state["query"], context_str)
    
    return {
        "domain_output": domain_out,
        "engine_outputs": [sec3_out, abs_out, prior_art_out]
    }

def synthesize_node(state: GraphState) -> Dict[str, Any]:
    category = state["classification"].category if state["classification"] else "UNCLEAR"
    conf = state["classification"].confidence if state["classification"] else 0.0
    
    # Aggregate compliance alerts
    alerts = []
    for eng_out in state["engine_outputs"]:
        alerts.extend(eng_out.checks)
        
    # Aggregate sources
    sources = []
    if state["domain_output"]:
        sources.extend(state["domain_output"].citations)
        guidance = state["domain_output"].regulatory_pathway + "\n\n**IP Options:**\n" + "\n".join(["- " + opt for opt in state["domain_output"].ip_options])
    else:
        guidance = "Classification unclear. Escalation to human expert recommended."

    final_resp = FinalResponse(
        classification=category,
        jurisdiction=state["jurisdiction"],
        guidance_text=guidance,
        compliance_alerts=alerts,
        sources=sources,
        overall_confidence=conf
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
