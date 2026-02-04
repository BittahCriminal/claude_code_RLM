@echo off
REM ============================================================================
REM Test GitHub Copilot CLI connectivity
REM Verifies that Copilot CLI is installed and authenticated
REM ============================================================================

setlocal EnableDelayedExpansion

echo.
echo ============================================================
echo   Testing GitHub Copilot CLI
echo ============================================================
echo.

REM Test 1: Check for native copilot command
echo [Test 1] Checking for native Copilot CLI...
where copilot >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] Native Copilot CLI found
    for /f "tokens=*" %%i in ('copilot --version 2^>^&1') do (
        echo     Version: %%i
    )
) else (
    echo [--] Native Copilot CLI not found
)

echo.

REM Test 2: Check for WSL
echo [Test 2] Checking for WSL...
where wsl >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo [OK] WSL found

    REM Test 2b: Check for copilot in WSL
    echo [Test 2b] Checking for Copilot CLI in WSL...
    wsl which copilot >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Copilot CLI found in WSL
        for /f "tokens=*" %%i in ('wsl copilot --version 2^>^&1') do (
            echo     Version: %%i
        )
    ) else (
        echo [--] Copilot CLI not found in WSL
        echo     Install with: wsl npm install -g @github/copilot
    )
) else (
    echo [--] WSL not found
    echo     Install with: wsl --install
)

echo.

REM Test 3: Check for legacy gh copilot
echo [Test 3] Checking for legacy gh copilot extension...
where gh >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    gh copilot --version >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo [OK] Legacy gh copilot extension found
        echo     Note: This extension is deprecated as of Oct 2025
    ) else (
        echo [--] Legacy gh copilot extension not installed
    )
) else (
    echo [--] GitHub CLI (gh) not found
)

echo.

REM Test 4: Quick functionality test
echo [Test 4] Running quick Copilot test...
echo (This may take a few seconds)
echo.

REM Try WSL first, then native
wsl which copilot >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo Testing via WSL...
    wsl copilot -p "Say hello in exactly 3 words" --allow-all-tools 2>&1
) else (
    where copilot >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        echo Testing via native CLI...
        copilot -p "Say hello in exactly 3 words" --allow-all-tools 2>&1
    ) else (
        echo [SKIP] No Copilot CLI available for testing
    )
)

echo.
echo ============================================================
echo   Test Complete
echo ============================================================
echo.

endlocal
