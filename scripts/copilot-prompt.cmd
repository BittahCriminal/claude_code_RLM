@echo off
REM ============================================================================
REM Run a prompt through GitHub Copilot CLI via WSL
REM Usage: copilot-prompt.cmd "Your prompt here"
REM ============================================================================

setlocal EnableDelayedExpansion

if "%~1"=="" (
    echo Usage: copilot-prompt.cmd "Your prompt here"
    echo.
    echo Example:
    echo   copilot-prompt.cmd "Explain what this code does"
    echo   copilot-prompt.cmd "Write a Python function to sort a list"
    exit /b 1
)

REM Check for WSL
where wsl >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] WSL not found. Please install WSL first.
    echo Run: wsl --install
    exit /b 1
)

REM Run Copilot via WSL
echo Running Copilot CLI...
wsl copilot -p %*

endlocal
