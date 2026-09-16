"""
IP-SHAKTI Backend — FastAPI Application Entry Point

This is the main entry point for the AI/ML backend service.
Handles all agent orchestration, RAG pipeline, and external API routing.
"""

import sys
import os

# Ensure UTF-8 output streams on Windows to prevent charmap codec errors
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from src.api.routes import chat

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "status": "healthy",
        "service": "IP-SHAKTI Regulatory & Patent Intelligence API",
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "ip-shakti-api"}

app.include_router(chat.router, prefix="/api/v1", tags=["chat"])
