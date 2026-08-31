"""
Base Agent — Shared interface for all domain agents.

All domain agents (Ayurvedic Medicine, Phytopharmaceutical, New Drug,
Cosmetics, Ayurveda-Aahar) inherit from this base class.

Each agent gets:
  - Its own system prompt (from config/prompts/agents/)
  - Access to the RAG retriever (filtered to its domain)
  - Access to the Knowledge Graph (filtered traversals)
  - A structured output schema (Pydantic model)

Model used: Gemini 2.0 Flash (for all domain agents)
"""

# TODO: Implement base agent with common interface:
#   - process(query, context, retrieved_chunks) -> AgentOutput
#   - get_system_prompt() -> str
#   - get_tools() -> list
