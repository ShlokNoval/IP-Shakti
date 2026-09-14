"""
Chat API Route — Main endpoint for user queries.
"""
import traceback
from fastapi import APIRouter, HTTPException
from src.models.chat import ChatRequest, FinalResponse
from src.core.orchestrator import orchestrator

router = APIRouter()

@router.post("/chat", response_model=FinalResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Initialize LangGraph state
        initial_state = {
            "query": request.query,
            "jurisdiction": request.jurisdiction,
            "language": request.language,
            "classification": None,
            "retrieved_context": [],
            "domain_output": None,
            "engine_outputs": [],
            "final_response": None
        }
        
        # Invoke the LangGraph workflow
        final_state = orchestrator.invoke(initial_state)
        
        if not final_state.get("final_response"):
            raise HTTPException(status_code=500, detail="Failed to generate response")
            
        return final_state["final_response"]
        
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
