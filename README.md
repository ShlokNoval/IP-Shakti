# 🌿 IP-SHAKTI (Sahayak)
### AI-Powered Ayurvedic Intellectual Property & Regulatory Compliance Engine

> **Smart India Hackathon (SIH) 2026**  
> **Problem Statement ID:** 26045  
> **Ministry:** Ministry of Ayush × All India Institute of Ayurveda (AIIA)  
> **Theme:** MedTech / BioTech / HealthTech / LegalTech  

---

## 📌 Problem Overview & Solution
Ayurvedic drug discovery, traditional formulation commercialization, and botanical medicine patenting face complex statutory hurdles in India and globally:
1. **Section 3(p) of the Patents Act, 1970**: Excludes traditional knowledge or mere aggregations of known properties.
2. **Section 3(d) & 3(e)**: Mandates proven therapeutic synergy / enhanced efficacy over prior art.
3. **Biological Diversity Act, 2002**: Strict Access and Benefit Sharing (ABS) mandates with National Biodiversity Authority (NBA) and State Biodiversity Boards (SBB).
4. **Regulatory Classification Complexities**: Classical formulations (Schedule I texts) vs. Proprietary medicines vs. Phytopharmaceuticals (Rule 122E) vs. Ayurveda-Aahar (FSSAI 2022).

**IP-SHAKTI (Sahayak)** solves this by serving as an intelligent, RAG-grounded decision-support system. It evaluates traditional knowledge conflicts against TKDL, validates statutory criteria under Indian and international laws, and outlines step-by-step regulatory licensing pathways.

---

## ✨ Key Features & Architecture

### 1. 🧙‍♂️ Adaptive (Akinator-Style) Formulation Wizard
- **Dynamic 4-Step Branching**: Intelligently adapts questions based on the selected category:
  - **Classical Ayurveda**: Schedule I classical treatise overlap (Charaka, Sushruta, Ashtanga Hridaya).
  - **Phytopharmaceuticals**: Rule 122E standardization ($\ge 4$ active chemical markers) and fraction extraction.
  - **Ayurveda-Aahar / Cosmetics / New Botanical Drugs**: RDA compliance, FSSAI regulations, Chapter III-A labeling.
- **ABS Biological Sourcing Gate**: Evaluates applicant nationality, wild vs. cultivated herbs, and Section 3/7 NBA approval triggers.
- **Innovation Profile Compiler**: Converts branching responses into a dense, high-dimensional Innovation Disclosure Profile.

### 2. 🌐 Jurisdiction-Scoped Vector Retrieval (36,186 Chunks)
- **Pre-Partitioned Vector Indexing**: The 36,186 legal chunks are partitioned in memory:
  - **🇮🇳 India Corpus (27,294 chunks)**: Indian Patents Act 1970, Drugs & Cosmetics Rules, Schedule I texts, Biological Diversity Act 2002.
  - **🌐 Global Corpus (8,892 chunks)**: WIPO PCT treaties, Nagoya Protocol on ABS, CBD, EPO/USPTO traditional medicine examination guidelines.
- **Sub-Millisecond Search**: In-memory binary cache (`embeddings_cache.npy` + `chunks_cache.pkl`) loads in milliseconds with zero embedding wait times.
- **Zero Statutory Leakage**: Domestic inquiries are never polluted with foreign patent statutes.

### 3. ⚖️ Unified Multi-Agent Legal Engine
- **Statutory Evaluation**: Generates complete regulatory pathways, key statutory requirements, and IP protection options.
- **Compliance Alert Cards**: Interactive visual cards with `CLEAR` (✅), `REVIEW` (⚠️), or `FAIL` (❌) verdicts for Section 3(p), Section 3(d)/(e), ABS, and TKDL conflicts.
- **Verified Statutory Citations**: Exact acts, rules, schedules, and treatise citations verified against the grounded RAG corpus.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Frontend UI** | Next.js 15 (Turbopack), React 19, TypeScript, Vanilla CSS (Glassmorphism & Herbal Theme) |
| **Backend API** | Python 3.10+, FastAPI, Uvicorn, Pydantic v2 |
| **AI / LLM Orchestration** | Groq (`groq/compound-mini` with 70,000 TPM limit), LangGraph, LangChain |
| **Vector Embeddings** | `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors) |
| **Binary Vector Cache** | NumPy (`.npy`) + Pickle (`.pkl`) binary storage for instant cold starts |
| **Legal Corpus** | 36,186 curated chunks from Indian & International legal statutes and AYUSH treatises |

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Node.js** (v18 or higher)
- **Python** (v3.10 or higher)
- **Git**

### 2. Clone and Setup Environment
```bash
# Clone the repository
git clone https://github.com/ShlokNoval/IP-Shakti.git
cd IP-Shakti

# Switch to the main branch
git checkout main
```

Create a `.env` file in the root directory (or copy from `.env.example`):
```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=groq/compound-mini
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

### 3. Running the Application

#### Option A: One-Click Startup (Windows)
Double-click **`START_IP_SHAKTI.bat`** in the root folder. It will automatically launch both backend and frontend servers in separate windows.

#### Option B: Manual Startup

**Terminal 1 — Backend (FastAPI):**
```bash
cd apps/api

# Create & activate virtual environment (optional but recommended)
python -m venv .venv
.\.venv\Scripts\activate   # On Windows
# source .venv/bin/activate  # On Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Start backend server on port 8000
python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload
```

**Terminal 2 — Frontend (Next.js):**
```bash
cd apps/web

# Install dependencies
npm install

# Start Next.js development server on port 3000
npm run dev
```

---

## 📍 Service URLs

- **Frontend Application:** [http://localhost:3000](http://localhost:3000)
- **Backend API Root:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Health Probe:** [http://127.0.0.1:8000/api/v1/health](http://127.0.0.1:8000/api/v1/health)
- **Interactive Swagger Documentation:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📁 Repository Structure

```
IP-Shakti/
├── START_IP_SHAKTI.bat             # One-click Windows startup script
├── .env.example                    # Environment variable template
├── .gitignore                      # Git ignore rules
├── README.md                       # Project documentation
│
├── apps/
│   ├── web/                        # Next.js 15 Frontend
│   │   ├── src/
│   │   │   ├── app/
│   │   │   │   ├── page.tsx        # Dual-mode dashboard & jurisdiction switcher
│   │   │   │   ├── globals.css     # Premium Ayurvedic design system & tokens
│   │   │   │   └── layout.tsx
│   │   │   ├── components/
│   │   │   │   └── IntakeWizard.tsx# 4-Step Adaptive Akinator Formulation Wizard
│   │   │   └── store/
│   │   │       └── chatStore.ts    # Zustand chat state management
│   │   └── package.json
│   │
│   └── api/                        # FastAPI AI Backend
│       ├── data/
│       │   └── processed/          # 36k pre-embedded vector caches (.npy & .pkl)
│       ├── src/
│       │   ├── api/
│       │   │   └── routes/
│       │   │       └── chat.py     # Chat & analysis endpoints
│       │   ├── config/
│       │   │   └── settings.py     # Pydantic configuration & Groq model settings
│       │   ├── core/
│       │   │   ├── classifier.py   # Fast-path profile classifier
│       │   │   └── orchestrator.py # Unified single-pass multi-agent legal engine
│       │   ├── models/
│       │   │   └── chat.py         # Pydantic request/response & alert schemas
│       │   ├── rag/
│       │   │   ├── chunker.py      # Legal text chunking & metadata tagging
│       │   │   ├── embedder.py     # Vector generation script
│       │   │   └── retriever.py    # Partitioned in-memory cosine retriever
│       │   └── main.py             # FastAPI entry point & CORS
│       └── requirements.txt
│
└── Laws_Rules_Data_Sources/        # Source legal documents & schedules
    └── IP Shakti Sources/
        ├── India/                  # Indian statutes, Schedule I texts, ABS rules
        └── Global/                 # WIPO PCT, Nagoya Protocol, CBD treaties
```

---

## ⚖️ Legal Disclaimer
*IP-SHAKTI is an artificial intelligence-powered regulatory and intellectual property decision-support system developed for educational, research, and advisory prototyping under SIH 2026. While the system cross-references verified statutory acts, rules, and classical treatises, formal patent applications and regulatory submissions should be validated with qualified IP attorneys and the Ministry of Ayush.*
