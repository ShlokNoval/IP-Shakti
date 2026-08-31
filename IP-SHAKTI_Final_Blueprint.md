# IP-SHAKTI — Final Project Blueprint | SIH 2026

**Sahayak — A Multilingual, RAG-Based, Source-Cited AI Assistant for Intellectual Property & Regulatory Guidance in Ayurveda**

- **SIH 2026**
- **Problem Statement 26045**
- **Ministry of Ayush × AIIA**
- **MedTech / BioTech / HealthTech | Software**

---

## 1. Problem Statement — Decoded

The problem demands an AI assistant that sits at the **intersection of three regimes**:

| Regime | What It Covers | Key Laws/Treaties |
| :--- | :--- | :--- |
| **IP Rights** | Patents, GI, Trademarks, Copyright, Designs, Trade Secrets, Plant Variety | Patents Act 1970, GI Act, TM Act, Copyright Act, Designs Act, PVPFR Act |
| **Drug/Product Regulation** | What category does the product fall in? Each has different rules. | D&C Act 1940, FSSAI Regs, Drugs & Magic Remedies Act |
| **Biodiversity / ABS** | Using Indian biological resources requires compliance | Biodiversity Act 2002, 2024 Rules, Nagoya Protocol, WIPO GRATK 2024 |

> ⚡ **The Key Insight Most Teams Will Miss:**
> You CANNOT give IP advice without first knowing WHAT the product is. A classical Ayurvedic formulation (Chyawanprash) has completely different IP options than a novel phytopharmaceutical extract. The classification MUST come first. This is why our system classifies before it advises.

### What Judges Want to See
| Requirement (from PS) | Our Answer |
| :--- | :--- |
| Jurisdiction toggle (India vs International) | UI toggle + separate answer pipelines per jurisdiction |
| Formulation classification flow | Classifier Agent → 6 categories → Domain Agents |
| ABS compliance helper | Dedicated ABS Compliance Agent |
| TKDL / Prior-art pointer | Prior Art Checker Agent + TK reference database |
| Source citations + confidence | Every response has statute citations + confidence % |
| Multilingual (Bhashini) | Bhashini ULCA API for 22 Indian languages |
| Guardrails + disclaimer | Hardcoded disclaimer, PII redaction, safe abstention |
| DPDP compliance | Consent flows, audit logs, data minimization |

---

## 2. Our 7 USPs — Why We Win

Most of the 500 teams will build a **generic chatbot** with some legal PDFs. Here's what makes us different:

1. **Multi-Agent Architecture, Not a Chatbot:** 10 specialized AI agents with distinct responsibilities, orchestrated by a state machine. Like a real IP law firm with different specialists.
2. **Legal Knowledge Graph (Neo4j):** Statutes, sections, rules, and formulations as connected graph nodes. Enables multi-hop reasoning.
3. **Formulation-First Classification:** System classifies the product into 6 categories BEFORE giving IP advice. Each category has fundamentally different IP posture.
4. **Source-Cited, Confidence-Scored Responses:** Every response cites specific Section/Rule/Article numbers. Confidence 0-100%. Auto-escalation to human when confidence < threshold.
5. **True Bhashini Integration with Voice:** Not Google Translate. Government Bhashini API — ASR → NMT → TTS pipeline for 22 Indian languages including voice input/output.
6. **ABS Compliance Engine:** Automated Biodiversity Act 2002 compliance checker. Checks if biological resources trigger NBA/SBB obligations, PIC/MAT requirements.
7. **Section 3 Patentability Filter:** Automated checking against Section 3(d) known substance, 3(e) mere admixture, 3(f) arrangement, 3(p) traditional knowledge.

---

## 3. System Architecture Overview

**Data flow from user query to final response:**

1. **USER QUERY** (any language)
2. **INTAKE GATE** (Jurisdiction, language, session, PII redaction, disclaimer)
3. **INPUT NORMALIZATION** (Bhashini translates to English, extracts key entities)
4. **CLASSIFIER AGENT** (Gemini Flash-Lite determines product category: Classical/Proprietary/NewDrug/Phyto/Aahar/Cosmetic)
5. **ORCHESTRATOR** (LangGraph reads classification → decides WHICH agents to invoke → builds execution plan)
6. **PARALLEL EXECUTION:** Domain Agent(s), Section 3 Agent, ABS Agent run in parallel.
7. **RAG + KNOWLEDGE GRAPH** (Supabase pgvector + Neo4j - All agents pull from the SAME knowledge base but with different queries/tools)
8. **REASONING + CONFIDENCE SCORING** (Merge all agent outputs, score confidence)
9. **CITATION VALIDATOR** (Verify all cited sections actually exist)
10. **OUTPUT FORMATTER** (Structure into card-based response + Bhashini translate back to user's language)
11. **FINAL RESPONSE** (Classification + Guidance + Sources + Confidence + Disclaimer)

---

## 4. 🤖 The Complete Agent Map — Who Does What, Where

There are **10 AI agents** in the system. 

### LAYER 1 — The Gatekeeper
**Agent 1: Classifier Agent** (`apps/api/src/core/classifier.py`)
- **Model:** Gemini Flash-Lite
- **Job:** Look at the user's product description and classify it into 1 of 6 categories (Classical, Proprietary, New Drug, Phytopharmaceutical, Ayurveda-Aahar, Cosmetic). Output: `{ category: "proprietary", confidence: 0.84, reasoning: "..." }`. If confidence < 60%, asks clarifying questions.

### LAYER 2 — The Decision Maker
**Agent 2: Orchestrator (Router)** (`apps/api/src/core/orchestrator.py`)
- **Model:** LangGraph State Machine (No LLM)
- **Job:** Read the classification result + query intent → decide which specialist agents to call and in what order. Deterministic state machine.

### LAYER 3 — The Domain Specialists (5 agents)
*All use **Gemini 2.0 Flash**.*

- **Agent 3: Ayurvedic Medicine Agent** (`agents/ayurvedic_medicine_agent.py`) - Handles Classical + Proprietary Ayurvedic medicines (D&C Act 1940, Schedule I texts).
- **Agent 4: Phytopharmaceutical Agent** (`agents/phytopharmaceutical_agent.py`) - Handles Rule 122E phytopharmaceutical products.
- **Agent 5: New Drug Agent** (`agents/new_drug_agent.py`) - Handles novel formulations needing clinical trials (Schedule Y).
- **Agent 6: Cosmetics Agent** (`agents/cosmetics_agent.py`) - Handles Ayurvedic cosmetic products (Cosmetics Rules, Chapter III-A).
- **Agent 7: Ayurveda-Aahar Agent** (`agents/ayurveda_aahar_agent.py`) - Handles nutraceuticals, health supplements (FSSAI).

### LAYER 4 — The Compliance Checkers (3 agents)
*All use **Gemini 2.0 Flash + Rule Engines**.*

- **Agent 8: Section 3 Evaluator** (`engines/section3_evaluator.py`) - Checks patentability against Section 3 of Patents Act (3d, 3e, 3f, 3p).
- **Agent 9: ABS Compliance Agent** (`engines/abs_compliance.py`) - Checks Biodiversity Act 2002 & Access-and-Benefit-Sharing obligations.
- **Agent 10: Prior Art & Claim Verification Agent** (`engines/prior_art_checker.py`) - Cross-checks the formulation against traditional knowledge databases and flags TKDL overlaps.

---

## 5. 🧠 AI/ML Models — What We Use, Why, and Where

We use **4 AI/ML models** total. All from Google, all free-tier.

1. **Gemini 2.0 Flash-Lite** 
   - **Used for:** Classifier Agent, Input Normalization, Cross-encoder Reranking.
   - **Why:** Fastest/cheapest. Good for simple tasks (classify, extract, rank) with high throughput.
2. **Gemini 2.0 Flash**
   - **Used for:** ALL 5 Domain Agents, Section 3 Evaluator, ABS Compliance, Prior Art Agent, Output Formatter.
   - **Why:** Primary workhorse. Excellent reasoning capability for legal analysis and structured output (JSON).
3. **Gemini 2.5 Pro**
   - **Used for:** Complex multi-hop reasoning and ambiguous edge cases.
   - **Why:** Deepest reasoning capability. Reserved for <5% of queries to stay within free tier (5 RPM).
4. **text-embedding-004**
   - **Used for:** Document & query embeddings (Supabase pgvector).
   - **Why:** Google's latest embedding model, strong on English legal text.

*(Bhashini ULCA API is used for Hindi/regional translation, Speech-to-text, and Text-to-speech)*

---

## 6. 🔄 LangGraph Orchestration — How It Actually Works

LangGraph is a Python library that builds **AI workflows as a state machine**. It handles State management, Conditional routing, Parallel execution, and Checkpointing.

**Flow:**
1. **INTAKE NODE:** Receives query, detects language, redacts PII.
2. **NORMALIZE NODE:** Bhashini translates to English, extracts key entities.
3. **CLASSIFY NODE:** Gemini Flash-Lite categorizes product.
4. **CONFIDENCE GATE:** Routes to Orchestrate if ≥60%, else Clarify.
5. **ORCHESTRATE NODE:** Deterministic rules build execution plan.
6. **RETRIEVE NODE:** Hybrid RAG search (pgvector + keyword).
7. **GRAPH AUGMENT NODE:** Neo4j queries for legal relationships.
8. **DOMAIN AGENT NODE(S):** Gemini Flash domain experts run in parallel.
9. **COMPLIANCE NODE(S):** Section 3 / ABS / Prior Art checks run.
10. **SYNTHESIZE + SCORE NODE:** Merges outputs, calculates overall confidence.
11. **CITATION VALIDATOR NODE:** Verifies cited sections exist.
12. **FORMAT + TRANSLATE NODE:** Structures JSON response, translates via Bhashini.

---

## 7. RAG Pipeline — How We Find and Cite Sources

- **Hybrid Retrieval (Vector + Keyword):** Uses pgvector for semantic search + PostgreSQL full-text for exact keyword matching (e.g. "Section 3(p)"). Merged via Reciprocal Rank Fusion.
- **Legal-Aware Chunking:** We split legal documents by **Section/Rule/Article boundaries** (not arbitrary token counts) and attach metadata (Act, Section, Jurisdiction).

---

## 8. Knowledge Graph — Why It Matters

Legal reasoning requires following **chains of connections** (e.g. Ashwagandha → biological resource → Biodiversity Act).
- **Schema (Neo4j AuraDB Free):** Acts have Chapters, Chapters have Sections. Sections can AMEND or CROSS-REFERENCE each other. Ingredients are USED IN formulations and GOVERNED BY ABS obligations.

---

## 9. Data Sources (Final & Corrected)

| Source | URL | What We Get | Access |
| :--- | :--- | :--- | :--- |
| **India Code** | indiacode.nic.in | Patents Act 1970, Biodiversity Act 2002, D&C Act 1940, Copyright Act, Designs Act, GI Act, PVPFR Act, Trade Marks Act, Drugs & Magic Remedies Act | Public Statute API (JSON, no key) |
| **IP India** | ipindia.gov.in | Patent search (InPASS), TM search, GI Registry, Design search | Public search interface |
| **TKDL Portal** | tkdl.res.in | TK classification references, published TKDL-related patent cases | Public info pages (full DB is restricted) |
| **National Biodiversity Authority** | nbaindia.org | ABS guidelines, NBA notifications, SBB lists | Public documents |
| **AYUSH Ministry** | ayush.gov.in | AYUSH drug regulations, Ayurvedic Pharmacopoeia, Schedule I texts | Published gazettes |
| **FSSAI** | fssai.gov.in | Ayurveda-Aahar regulations, nutraceutical standards | Public regulations |
| **WIPO** | wipo.int | GRATK Treaty 2024, PCT guide, Madrid/Hague protocols, Budapest Treaty | Free public access |
| **PPV&FR Authority** | plantauthority.gov.in | Plant variety protection, farmers' rights, registration procedures | Public portal |
| **CCRAS (Ministry of Ayush)** | ccras.nic.in | Ayurvedic research data, clinical trial results, formulation studies, drug standards | Public research publications |
| **CDSCO** | cdsco.gov.in | Drug approvals, clinical trial guidelines, new drug applications, regulatory forms | Public portal |

> ⚠️ **TKDL Honest Approach:** The full TKDL database is restricted. We use publicly available TK reference data from CCRAS, Ayurvedic Pharmacopoeia, and Schedule I texts, labeling it as "TKDL-aligned reference data".

---

## 10. Tech Stack — Complete & All Free

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | Next.js 15, TypeScript, Vanilla CSS, Zustand | Full-stack React framework, typing, client state |
| **Backend** | Python 3.12, FastAPI, LangChain, LangGraph | AI/ML service layer, RAG, orchestration |
| **AI/ML** | Gemini 2.0 Flash-Lite, Flash, 2.5 Pro, text-embedding-004 | Free-tier capable LLMs |
| **Database** | Supabase (PostgreSQL 15 + pgvector) | Users, sessions, documents, vectors |
| **Knowledge Graph**| Neo4j AuraDB Free | 200K nodes/400K rels for legal connections |
| **Multilingual** | Bhashini ULCA API | Free, Govt of India ASR+NMT+TTS |
| **Deployment** | Vercel (Next.js), Render (FastAPI) | Free-tier hosting |

---

## 11. Folder Structure
```text
IP-Shakti/
├── apps/
│   ├── web/                         # Next.js 15 Frontend
│   │   ├── public/                  
│   │   ├── src/app/                 # App Router pages (auth, dashboard/chat, api)
│   │   ├── src/components/          # UI, Chat, Layout components
│   │   ├── src/hooks/               # useChat, useJurisdiction, useBhashini
│   │   ├── src/lib/                 # Supabase client, API utils
│   │   ├── src/stores/              # Zustand stores
│   │   └── src/types/               # TypeScript definitions
│   │
│   └── api/                         # Python FastAPI Backend
│       ├── src/main.py              # Entry point
│       ├── src/config/              # Env config, prompt templates
│       ├── src/api/routes/          # HTTP routes (/chat, /classify)
│       ├── src/api/middleware/      # PII redaction, audit logging
│       ├── src/core/                # THE BRAIN — Agents and Orchestrator
│       │   ├── orchestrator.py      
│       │   ├── classifier.py        
│       │   ├── agents/              # Domain agents
│       │   ├── engines/             # Compliance checkers (Section 3, ABS, Prior Art)
│       │   └── reasoning/           # Multi-hop reasoning
│       ├── src/rag/                 # Retriever, chunker, embedder, citation
│       ├── src/knowledge_graph/     # Neo4j client, cypher queries, ETL
│       └── src/services/            # Bhashini & Supabase clients
│       ├── data/corpus/             # Raw legal documents
│       └── data/graph_seeds/        # KG seed data
├── supabase/migrations/             
├── docs/                            
├── .env.example
├── .gitignore
├── README.md
```

---

## 12. Multilingual & Voice (Bhashini)

- **User speaks Hindi** → Browser captures audio → **Bhashini ASR API** (Hindi speech → Hindi text) → **Bhashini NMT API** (Hindi text → English text).
- Backend processes in English → English response generated.
- **Bhashini NMT API** (English → Hindi text) → **Bhashini TTS API** (Hindi text → Hindi speech audio) → **User hears response in Hindi**.

---

## 13. Security & DPDP Compliance
- **Consent:** Explicit consent modal before first use.
- **Data minimization:** PII redacted before LLM processing.
- **Audit logging:** Every query logged with timestamp, user ID, confidence.
- **Disclaimer:** Hardcoded "information, not legal advice".

---

## 14. Output Format — What the User Sees
```
┌─────────────────────────────────────────────┐
│  PRODUCT CLASSIFICATION                     │
│  Proprietary / potentially non-classical    │
│  Confidence: 84%                            │
├─────────────────────────────────────────────┤
│  JURISDICTION: India 🇮🇳                     │
├─────────────────────────────────────────────┤
│  RELEVANT AREAS                             │
│  ✓ Patent     ✓ Traditional Knowledge       │
│  ✓ Biodiversity / ABS  ✓ AYUSH Regulation   │
├─────────────────────────────────────────────┤
│  SECTION 3 ANALYSIS                         │
│  § 3(d): Novel process — REVIEW ⚠️          │
│  § 3(e): Not mere admixture — CLEAR ✅      │
│  § 3(p): TK overlap — REVIEW ⚠️             │
├─────────────────────────────────────────────┤
│  SOURCES                                    │
│  [1] Patents Act, 1970 — Section 3(d)       │
│  [2] Patents Act, 1970 — Section 3(p)       │
│  [3] Biodiversity Act, 2002 — Section 3     │
├─────────────────────────────────────────────┤
│  CONFIDENCE: 82%  ████████████████░░░░      │
├─────────────────────────────────────────────┤
│  ⚖️ DISCLAIMER: Information, not legal       │
│  advice. Consult a qualified professional.  │
└─────────────────────────────────────────────┘
```

---

## 15. Phased Roadmap
- **P0: Foundation:** Scaffold, DB setup, basic UI, first corpus batch.
- **P1: Core Intelligence:** Classifier, orchestrator, 3 domain agents, hybrid RAG, citations, basic Bhashini.
- **P2: Differentiation:** Knowledge graph, remaining agents, voice interface, evaluation.
- **P3: Hardening:** Optimization, DPDP audit, documentation.
