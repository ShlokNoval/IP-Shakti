@echo off
title IP-SHAKTI Services
echo Starting IP-SHAKTI...
echo.

cd /d "%~dp0"

echo [1] Starting Backend (FastAPI)...
start "Backend" cmd /k "cd /d %~dp0apps\api && python -m uvicorn src.main:app --reload --port 8000"

timeout /t 3 /nobreak >nul

echo [2] Starting Frontend (Next.js)...
start "Frontend" cmd /k "cd /d %~dp0apps\web && npm run dev"

echo.
echo Done. Backend: http://localhost:8000 | Frontend: http://localhost:3000
echo Close this window when done.
pause
