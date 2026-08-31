"""
IP-SHAKTI Backend — FastAPI Application Entry Point

This is the main entry point for the AI/ML backend service.
Handles all agent orchestration, RAG pipeline, and external API routing.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="IP-SHAKTI API",
    description="AI backend for IP & regulatory guidance in Ayurveda",
    version="0.1.0",
)

# CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ip-shakti-api"}
