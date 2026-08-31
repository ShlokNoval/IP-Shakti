# IP-SHAKTI — Sahayak

> Multilingual, RAG-based, source-cited AI assistant for Intellectual Property & regulatory guidance in Ayurveda.

**SIH 2026 | Problem Statement 26045 | Ministry of Ayush × AIIA**

---

## Quick Start

### Prerequisites
- Node.js 20+
- Python 3.12+
- Git

### Frontend (Next.js)
```bash
cd apps/web
npm install
npm run dev
```

### Backend (FastAPI)
```bash
cd apps/api
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### Environment Variables
Copy `.env.example` to `.env` and fill in:
- `GOOGLE_API_KEY` — Gemini API key (free tier)
- `SUPABASE_URL` + `SUPABASE_ANON_KEY`
- `NEO4J_URI` + `NEO4J_USER` + `NEO4J_PASSWORD`
- `BHASHINI_API_KEY` + `BHASHINI_USER_ID`

---

## Architecture

```
User Query → Intake Gate → Normalizer → Classifier → Orchestrator
                                                          ↓
                              Domain Agents + Compliance Engines
                                                          ↓
                                   RAG + Knowledge Graph + Citations
                                                          ↓
                              Structured Response + Confidence + Sources
```

## Tech Stack

| Layer | Technology |
|:------|:-----------|
| Frontend | Next.js 15, TypeScript, CSS Modules |
| Backend | Python 3.12, FastAPI, LangChain, LangGraph |
| AI/ML | Gemini Flash-Lite, Gemini 2.0 Flash, text-embedding-004 |
| Database | Supabase (PostgreSQL + pgvector) |
| Knowledge Graph | Neo4j AuraDB |
| Translation | Bhashini ULCA API |
| Deployment | Vercel (frontend), Render (backend) |

## Team

Team IP-SHAKTI | SIH 2026

---

> ⚖️ **Disclaimer**: This system provides information and decision support, not legal advice.
