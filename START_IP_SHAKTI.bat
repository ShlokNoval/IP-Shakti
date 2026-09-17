@echo off
title IP-SHAKTI — One-Click Startup & Service Orchestrator
color 0A
echo ===============================================================================
echo            IP-SHAKTI: AYURVEDIC REGULATORY & IP INTELLIGENCE
echo ===============================================================================
echo.

cd /d "%~dp0"

:: 1. Check environment file
if not exist ".env" (
    if exist ".env.example" (
        echo [!] .env not found. Creating .env from .env.example...
        copy ".env.example" ".env" >nul
        echo [!] Created .env. Please ensure your GROQ_API_KEY is configured.
    ) else (
        echo [!] WARNING: .env file missing in root directory.
    )
)

echo [1/2] Initializing Backend Service (FastAPI & Legal RAG Engine)...
start "IP-SHAKTI Backend (FastAPI)" cmd /k "cd /d %~dp0apps\api && (if not exist .venv (echo Creating Python virtual environment... && python -m venv .venv)) && call .venv\Scripts\activate && (python -c ""import fastapi, sentence_transformers, langchain_groq, pydantic_settings"" 2>nul || (echo Installing backend dependencies from requirements.txt... && pip install -r requirements.txt)) && echo. && echo [OK] Starting FastAPI on http://127.0.0.1:8000 ... && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 3 /nobreak >nul

echo [2/2] Initializing Frontend Service (Next.js & Sahayak Wizard)...
start "IP-SHAKTI Frontend (Next.js)" cmd /k "cd /d %~dp0apps\web && (if not exist node_modules (echo Installing frontend dependencies via npm install... && npm install)) && echo. && echo [OK] Starting Next.js development server on http://localhost:3000 ... && npm run dev"

echo.
echo ===============================================================================
echo  [OK] IP-SHAKTI Services Launched Successfully!
echo  - Frontend Application : http://localhost:3000
echo  - Backend API & Health : http://127.0.0.1:8000  (Docs: http://127.0.0.1:8000/docs)
echo ===============================================================================
echo.
echo You can keep this controller window open or close it. Press any key to exit.
pause >nul
