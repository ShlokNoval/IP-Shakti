"""
Chat API Route — Main endpoint for user queries.

POST /api/v1/chat
  Body: { query, jurisdiction, language, session_id }
  Response: { classification, guidance, section3, abs, sources, confidence, disclaimer }
"""

# TODO: Implement chat endpoint that triggers the LangGraph orchestrator
