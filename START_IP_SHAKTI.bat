@echo off
title IP-SHAKTI Launcher
color 0A

echo.
echo  ======================================================
echo       IP-SHAKTI (Sahayak) - Project Launcher
echo       Multilingual AI for IP ^& Regulatory Guidance
echo  ======================================================
echo.

:: Set project root to wherever this .bat file lives
cd /d "%~dp0"

:: ──────────────────────────────────────────────────────
:: 1. Pre-flight checks
:: ──────────────────────────────────────────────────────
echo [1/4] Running pre-flight checks...

:: Check Python
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

:: Check Node
where node >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Node.js not found. Please install Node.js 18+ and add it to PATH.
    pause
    exit /b 1
)

:: Check .env
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo         Copy .env.example to .env and fill in your API keys.
    pause
    exit /b 1
)

echo         Python  : OK
echo         Node.js : OK
echo         .env    : OK
echo.

:: ──────────────────────────────────────────────────────
:: 2. Install Node dependencies only if missing
:: ──────────────────────────────────────────────────────
echo [2/4] Checking Node.js dependencies...
if not exist "apps\web\node_modules" (
    echo         Installing npm packages (first run only)...
    cd apps\web
    call npm install --silent
    cd ..\..
) else (
    echo         node_modules found, skipping.
)
echo.

:: ──────────────────────────────────────────────────────
:: 3. Start Backend (FastAPI) in a new terminal window
:: ──────────────────────────────────────────────────────
echo [3/4] Starting FastAPI backend on http://localhost:8000 ...
start "IP-SHAKTI Backend" cmd /k "cd /d %~dp0 && title IP-SHAKTI Backend && color 0B && echo. && echo  Starting IP-SHAKTI Backend... && echo  API Docs: http://localhost:8000/docs && echo. && python -m uvicorn apps.api.src.main:app --reload --host 0.0.0.0 --port 8000"
echo         Backend starting in new window...
echo.

:: Give backend a moment to boot
timeout /t 4 /nobreak >nul

:: ──────────────────────────────────────────────────────
:: 4. Start Frontend (Next.js) in a new terminal window
:: ──────────────────────────────────────────────────────
echo [4/4] Starting Next.js frontend on http://localhost:3000 ...
start "IP-SHAKTI Frontend" cmd /k "cd /d %~dp0\apps\web && title IP-SHAKTI Frontend && color 0D && echo. && echo  Starting IP-SHAKTI Frontend... && echo. && npm run dev"
echo         Frontend starting in new window...
echo.

:: ──────────────────────────────────────────────────────
:: Open browser and wait
:: ──────────────────────────────────────────────────────
echo  ======================================================
echo   All services launching! Opening browser in 5 seconds...
echo  ======================================================
echo.
echo   Backend  : http://localhost:8000  (API Docs: /docs)
echo   Frontend : http://localhost:3000
echo.
echo   Press any key in THIS window to STOP all services.
echo.

timeout /t 5 /nobreak >nul
start "" "http://localhost:3000"

pause >nul

:: Cleanup
echo.
echo  Shutting down IP-SHAKTI...
taskkill /fi "WINDOWTITLE eq IP-SHAKTI Backend*" /f >nul 2>&1
taskkill /fi "WINDOWTITLE eq IP-SHAKTI Frontend*" /f >nul 2>&1
echo  All services stopped. Goodbye!
timeout /t 2 /nobreak >nul
