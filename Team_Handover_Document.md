# IP-SHAKTI — Team Handover & Context Document

> **ATTENTION AI AGENTS (AntiGravity / IDEs):**
> If you are reading this document, you are assisting a developer on the IP-SHAKTI project for SIH 2026. Read this entire document carefully to understand the system architecture, tech stack, and your specific module boundaries. Do NOT modify files outside of your assigned module to prevent merge conflicts.

## 1. Project Overview
**IP-SHAKTI (Sahayak)** is a multilingual, RAG-based, source-cited AI assistant for Intellectual Property & Regulatory guidance in Ayurveda. 
- **Tech Stack (Strictly Free-Tier):** Next.js 15 (Frontend), Python 3.12 / FastAPI (Backend), LangChain/LangGraph (Orchestration), Gemini 2.0 Flash/Flash-Lite (LLMs), Supabase + pgvector (Vector DB), Neo4j AuraDB (Knowledge Graph), Bhashini (Multilingual).
- **Core Concept:** It is a Multi-Agent system (10 agents), NOT a single chatbot. It classifies the product first, routes it to domain specialists, runs compliance checks (Section 3 Patentability, ABS Biodiversity), and outputs a structured, cited response.

## 2. Git & Branching Strategy
- **Base Branch:** All team members will clone `shlok` branch, and start working and pushing working code on their branch (NOT `main`), also refer docs and this doc for more contexts.
- **Your Branch:** Create a branch for your specific module (e.g., `frontend-dev`, `domain-agents-dev`, `compliance-dev`).
- **Merging:** You will push your code to your branch. Shlok (Lead) will review and merge your branch into the `shlok` branch.
- **Rules:** DO NOT touch files outside your assigned module. If you need a change in a shared file (like a Pydantic schema), communicate with Shlok.

---

## 3. Module Division (Minimal Interdependence)

To ensure no merge conflicts, the project is divided into 4 isolated modules. All modules communicate via predefined Pydantic schemas (JSON contracts).

### 👑 Module 1: Core Orchestration & Integration (Assigned to: Shlok / Lead)
**Role:** The "Traffic Cop" and final synthesizer.
**Responsibilities:**
- FastAPI setup and API routes (`apps/api/src/api/routes/`).
- LangGraph Orchestrator (`apps/api/src/core/orchestrator.py`).
- The Gatekeeper / Classifier Agent (`apps/api/src/core/classifier.py`).
- RAG Retriever logic combining vector + graph search (`apps/api/src/rag/retriever.py`).
- Final synthesis and Confidence Scoring.
**Boundaries:** Shlok orchestrates the agents, but does not write the internal logic for the Domain or Compliance agents.

### 💻 Module 2: Frontend & Multilingual UI (Assigned to: Subordinate 1)
**Role:** The User Experience.
**Responsibilities:**
- Next.js 15 UI development (`apps/web/*`).
- Chat interface with Markdown and Citation rendering.
- State management using Zustand.
- Integrating the Bhashini API for Hindi voice/text translation.
**Boundaries:** 100% isolated to `apps/web/`. You do not need the backend to be finished to start; mock the backend API responses using the JSON contracts below.

### 🌿 Module 3: Domain Agents (Assigned to: Subordinate 2)
**Role:** The Legal Specialists.
**Responsibilities:**
- Writing the specific system prompts, few-shot examples, and logic for the 5 domain agents.
- **Files Owned:** 
  - `apps/api/src/core/agents/base_agent.py`
  - `ayurvedic_medicine_agent.py`
  - `phytopharmaceutical_agent.py`
  - `new_drug_agent.py`
  - `cosmetics_agent.py`
  - `ayurveda_aahar_agent.py`
**Boundaries:** You assume that when your agent is called, it will be handed a `query` and `retrieved_legal_context`. Your ONLY job is to make the Gemini 2.0 Flash model reason over that context and output the correct JSON schema. You do not worry about how the context is retrieved or how the agent is routed.

### ⚖️ Module 4: Compliance Engines & Data Pipelines (Assigned to: Subordinate 3)
**Role:** The Rule Enforcers & Data Loaders.
**Responsibilities:**
- Writing the deterministic compliance rules (using Gemini + hardcoded logic).
- **Files Owned (Engines):**
  - `apps/api/src/core/engines/section3_evaluator.py` (Patent Act checks)
  - `apps/api/src/core/engines/abs_compliance.py` (Biodiversity checks)
  - `apps/api/src/core/engines/prior_art_checker.py`
- **Files Owned (Data Pipeline):**
  - Scripts to chunk PDFs and push to Supabase (`apps/api/src/rag/chunker.py`, `embedder.py`).
  - Script to push entities to Neo4j (`apps/api/src/knowledge_graph/graph_builder.py`).
**Boundaries:** Your compliance engines must take a formulation description and output a strict Pass/Fail/Review checklist in JSON.

---

## 4. The Shared Contracts (Pydantic / JSON)
*Since modules are separated, this is how they talk to each other. Adhere to these formats.*

### A. Classifier to Orchestrator (Shlok's Domain)
```json
{
  "category": "PHYTOPHARMACEUTICAL",
  "confidence": 0.92,
  "reasoning": "Standardized extract mentioned..."
}
```

### B. Domain Agent Output (Subordinate 2's Domain)
```json
{
  "regulatory_pathway": "Requires approval under Rule 122E...",
  "key_requirements": ["Standardized marker", "Safety data"],
  "ip_options": ["Patent", "Trade Secret"],
  "citations": ["Rule 122E, D&C Act"]
}
```

### C. Compliance Engine Output (Subordinate 3's Domain)
```json
{
  "engine": "Section 3 Evaluator",
  "checks": [
    {"rule": "3(d)", "status": "REVIEW", "reason": "Modified process needs proven enhanced efficacy"},
    {"rule": "3(p)", "status": "CLEAR", "reason": "Not found in traditional texts"}
  ]
}
```

### D. Final Backend Response to Frontend (Subordinate 1's Domain)
```json
{
  "classification": "Phytopharmaceutical",
  "jurisdiction": "India",
  "guidance_text": "Markdown formatted text...",
  "compliance_alerts": [...],
  "sources": [{"name": "Rule 122E", "link": "..."}],
  "overall_confidence": 0.85
}
```
