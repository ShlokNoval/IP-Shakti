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
echo [1/5] Running pre-flight checks...

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
    echo         At minimum, set GOOGLE_API_KEY=AIza...
    pause
    exit /b 1
)

echo         Python  : OK
echo         Node.js : OK
echo         .env    : OK
echo.

:: ──────────────────────────────────────────────────────
:: 2. Install Python dependencies (if needed)
:: ──────────────────────────────────────────────────────
echo [2/5] Checking Python dependencies...
pip install -r apps\api\requirements.txt -q 2>nul
echo         Dependencies ready.
echo.

:: ──────────────────────────────────────────────────────
:: 3. Install Node dependencies (if needed)
:: ──────────────────────────────────────────────────────
echo [3/5] Checking Node.js dependencies...
if not exist "apps\web\node_modules" (
    echo         Installing npm packages (first run only)...
    cd apps\web
    call npm install --silent
    cd ..\..
) else (
    echo         node_modules found, skipping install.
)
echo.

:: ──────────────────────────────────────────────────────
:: 4. Start Backend (FastAPI) in a new terminal window
:: ──────────────────────────────────────────────────────
echo [4/5] Starting FastAPI backend on http://localhost:8000 ...
start "IP-SHAKTI Backend" cmd /k "cd /d %~dp0 && title IP-SHAKTI Backend (FastAPI) && color 0B && echo. && echo  Starting IP-SHAKTI Backend... && echo  API Docs: http://localhost:8000/docs && echo. && python -m uvicorn apps.api.src.main:app --reload --host 0.0.0.0 --port 8000"
echo         Backend starting in new window...
echo.

:: Give backend a moment to boot before frontend tries to connect
timeout /t 3 /nobreak >nul

:: ──────────────────────────────────────────────────────
:: 5. Start Frontend (Next.js) in a new terminal window
:: ──────────────────────────────────────────────────────
echo [5/5] Starting Next.js frontend on http://localhost:3000 ...
start "IP-SHAKTI Frontend" cmd /k "cd /d %~dp0\apps\web && title IP-SHAKTI Frontend (Next.js) && color 0D && echo. && echo  Starting IP-SHAKTI Frontend... && echo. && npm run dev"
echo         Frontend starting in new window...
echo.

:: ──────────────────────────────────────────────────────
:: 6. Wait and open browser
:: ──────────────────────────────────────────────────────
echo  ======================================================
echo   All services launching! Opening browser in 5 seconds...
echo  ======================================================
echo.
echo   Backend  : http://localhost:8000  (API Docs: /docs)
echo   Frontend : http://localhost:3000
echo.
echo   Close this window to stop all services.
echo.

timeout /t 5 /nobreak >nul
start "" "http://localhost:3000"

echo  IP-SHAKTI is running. Press any key to STOP all services.
pause >nul

:: ──────────────────────────────────────────────────────
:: Cleanup: Kill both servers when user presses a key
:: ──────────────────────────────────────────────────────
echo.
echo  Shutting down IP-SHAKTI...
taskkill /fi "WINDOWTITLE eq IP-SHAKTI Backend*" /f >nul 2>&1
taskkill /fi "WINDOWTITLE eq IP-SHAKTI Frontend*" /f >nul 2>&1
echo  All services stopped. Goodbye!
timeout /t 2 /nobreak >nul
