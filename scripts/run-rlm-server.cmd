@echo off
REM ============================================================================
REM Start the RLM MCP Server
REM This server provides tools for processing large documents with Copilot CLI
REM ============================================================================

setlocal

REM Get the script directory
set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%.."

REM Activate virtual environment if it exists
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
)

echo Starting RLM MCP Server...
echo Press Ctrl+C to stop
echo.

python -m rlm_mcp.server

endlocal
