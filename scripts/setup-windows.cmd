@echo off
REM ============================================================================
REM RLM Copilot CLI Setup Script for Windows
REM ============================================================================
REM This script sets up the environment for running RLM with Copilot CLI
REM Requires: Python 3.10+, Node.js (for Copilot CLI), WSL or PowerShell 7+
REM ============================================================================

setlocal EnableDelayedExpansion

echo.
echo ============================================================
echo   RLM + Copilot CLI Setup for Windows
echo ============================================================
echo.

REM Check for Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python not found in PATH
    echo Please install Python 3.10+ from https://python.org
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python found: %PYVER%

REM Check for pip
where pip >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] pip not found
    exit /b 1
)
echo [OK] pip found

REM Check for Node.js (needed for Copilot CLI)
where node >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] Node.js not found - needed for Copilot CLI
    echo Install from https://nodejs.org or: winget install OpenJS.NodeJS.LTS
) else (
    for /f "tokens=*" %%i in ('node --version 2^>^&1') do set NODEVER=%%i
    echo [OK] Node.js found: !NODEVER!
)

REM Check for WSL (recommended for Windows)
where wsl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARN] WSL not found - recommended for Copilot CLI on Windows
    echo Install with: wsl --install
) else (
    echo [OK] WSL found
)

REM Check for Copilot CLI
where copilot >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [INFO] Copilot CLI not found in Windows PATH
    echo Checking WSL...
    wsl which copilot >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo [WARN] Copilot CLI not found in WSL either
        echo Install with: npm install -g @github/copilot
        echo Or in WSL: wsl npm install -g @github/copilot
    ) else (
        echo [OK] Copilot CLI found in WSL
    )
) else (
    echo [OK] Copilot CLI found
)

echo.
echo ------------------------------------------------------------
echo   Setting up Python virtual environment...
echo ------------------------------------------------------------

REM Get the script directory (where this script lives)
set SCRIPT_DIR=%~dp0
REM Go up one level to repo root
cd /d "%SCRIPT_DIR%.."

if exist .venv (
    echo [INFO] Virtual environment already exists
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Failed to create virtual environment
        exit /b 1
    )
    echo [OK] Virtual environment created
)

REM Activate venv
call .venv\Scripts\activate.bat

echo.
echo ------------------------------------------------------------
echo   Installing RLM MCP Server...
echo ------------------------------------------------------------

pip install -e rlm-mcp\ --quiet
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install rlm-mcp
    exit /b 1
)
echo [OK] RLM MCP Server installed

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Activate the environment: .venv\Scripts\activate.bat
echo   2. Install Copilot CLI (if not done):
echo      - In WSL: npm install -g @github/copilot
echo      - Then authenticate: copilot (follow /login)
echo   3. Run the RLM MCP server: python -m rlm_mcp.server
echo.
echo For more details, see: docs\COPILOT_CLI_SETUP.md
echo.

endlocal
