"""
LangGraph Orchestrator — The brain of IP-SHAKTI.
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from ...models.chat import ClassifierOutput, FinalResponse, SourceCitation
from .classifier import classifier_agent
from ..rag.retriever import hybrid_retriever

class GraphState(TypedDict):
    query: str
    jurisdiction: str
    language: str
    classification: Optional[ClassifierOutput]
    retrieved_context: List[Dict[str, Any]]
    final_response: Optional[FinalResponse]

def classify_node(state: GraphState) -> Dict[str, Any]:
    """Runs the Classifier Agent to determine product category."""
    classification = classifier_agent.classify(state["query"])
    return {"classification": classification}

def retrieve_node(state: GraphState) -> Dict[str, Any]:
    """Runs the RAG retriever to fetch legal context based on jurisdiction."""
    context = hybrid_retriever.retrieve(state["query"], state["jurisdiction"])
    return {"retrieved_context": context}

def synthesize_node(state: GraphState) -> Dict[str, Any]:
    """
    Synthesizes the final output. In a full system, this would happen 
    AFTER the Domain Agents run. For Shlok's core module, this is the final step.
    """
    category = state["classification"].category if state["classification"] else "UNCLEAR"
    conf = state["classification"].confidence if state["classification"] else 0.0
    
    # Extract sources from retrieved context
    sources = []
    for doc in state["retrieved_context"]:
        meta = doc.get("metadata", {})
        sources.append(SourceCitation(
            name=meta.get("source", "Unknown"),
            section=meta.get("section", "Unknown")
        ))

    final_resp = FinalResponse(
        classification=category,
        jurisdiction=state["jurisdiction"],
        guidance_text=f"Based on your query, this falls under **{category}**. We have reviewed the relevant texts.",
        overall_confidence=conf,
        sources=sources
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
