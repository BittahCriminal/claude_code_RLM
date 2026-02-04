#Requires -Version 7.0
<#
.SYNOPSIS
    Test GitHub Copilot CLI connectivity and environment detection

.DESCRIPTION
    Verifies Copilot CLI installation and tests both native pwsh and WSL paths.
    Also tests the Python provider's environment detection.

.EXAMPLE
    .\test-copilot.ps1

.EXAMPLE
    .\test-copilot.ps1 -Verbose
#>

[CmdletBinding()]
param()

$ErrorActionPreference = "Continue"

function Write-TestResult {
    param([string]$Test, [bool]$Passed, [string]$Details = "")
    $status = if ($Passed) { "[PASS]" } else { "[FAIL]" }
    $color = if ($Passed) { "Green" } else { "Red" }
    Write-Host $status -ForegroundColor $color -NoNewline
    Write-Host " $Test"
    if ($Details) {
        Write-Host "       $Details" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Copilot CLI Environment Test" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$results = @{
    NativeCopilot = $false
    WslCopilot = $false
    PythonDetection = $false
    QuickTest = $false
}

# Test 1: Native Copilot CLI
Write-Host "Test 1: Native Copilot CLI" -ForegroundColor Yellow
$copilot = Get-Command copilot -ErrorAction SilentlyContinue
if ($copilot) {
    try {
        $version = & copilot --version 2>&1 | Select-Object -First 1
        Write-TestResult "Native copilot found" $true $version
        $results.NativeCopilot = $true
    } catch {
        Write-TestResult "Native copilot found but version check failed" $false $_.Exception.Message
    }
} else {
    Write-TestResult "Native copilot not in PATH" $false "Install: npm install -g @github/copilot"
}

Write-Host ""

# Test 2: WSL Copilot CLI
Write-Host "Test 2: WSL Copilot CLI" -ForegroundColor Yellow
$wsl = Get-Command wsl -ErrorAction SilentlyContinue
if ($wsl) {
    try {
        $wslCopilot = & wsl which copilot 2>$null
        if ($wslCopilot) {
            $wslVersion = & wsl copilot --version 2>&1 | Select-Object -First 1
            Write-TestResult "WSL copilot found" $true $wslVersion
            $results.WslCopilot = $true
        } else {
            Write-TestResult "WSL available but copilot not installed" $false "In WSL: npm install -g @github/copilot"
        }
    } catch {
        Write-TestResult "WSL check failed" $false $_.Exception.Message
    }
} else {
    Write-TestResult "WSL not available" $false "Install: wsl --install"
}

Write-Host ""

# Test 3: Python Environment Detection
Write-Host "Test 3: Python Environment Detection" -ForegroundColor Yellow
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir

try {
    $pythonCode = @"
import sys
sys.path.insert(0, r'$repoRoot\rlm-mcp')
from rlm_mcp.providers import detect_environment, check_environment
env = check_environment()
print(f'Environment: {env.env_type.value}')
print(f'Shell: {env.shell_name}')
print(f'WSL Wrapper: {env.requires_wsl_wrapper}')
print(f'Notes: {env.notes}')
"@

    $result = $pythonCode | python 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-TestResult "Python environment detection works" $true
        $result | ForEach-Object { Write-Host "       $_" -ForegroundColor Gray }
        $results.PythonDetection = $true
    } else {
        Write-TestResult "Python detection failed" $false ($result -join "; ")
    }
} catch {
    Write-TestResult "Python test error" $false $_.Exception.Message
}

Write-Host ""

# Test 4: Quick Copilot Prompt Test
Write-Host "Test 4: Quick Copilot Prompt Test" -ForegroundColor Yellow
Write-Host "       (This may take a few seconds...)" -ForegroundColor Gray

$testPrompt = "Reply with exactly: TEST_OK"

if ($results.NativeCopilot) {
    Write-Host "       Testing via native copilot..." -ForegroundColor Gray
    try {
        $response = & copilot -p $testPrompt --allow-all-tools 2>&1
        if ($response -match "TEST_OK") {
            Write-TestResult "Native copilot prompt works" $true
            $results.QuickTest = $true
        } else {
            Write-TestResult "Native copilot responded but unexpected output" $false
            Write-Verbose "Response: $response"
        }
    } catch {
        Write-TestResult "Native copilot prompt failed" $false $_.Exception.Message
    }
} elseif ($results.WslCopilot) {
    Write-Host "       Testing via WSL copilot..." -ForegroundColor Gray
    try {
        $response = & wsl copilot -p $testPrompt --allow-all-tools 2>&1
        if ($response -match "TEST_OK") {
            Write-TestResult "WSL copilot prompt works" $true
            $results.QuickTest = $true
        } else {
            Write-TestResult "WSL copilot responded but unexpected output" $false
            Write-Verbose "Response: $response"
        }
    } catch {
        Write-TestResult "WSL copilot prompt failed" $false $_.Exception.Message
    }
} else {
    Write-TestResult "Skipped - no copilot available" $false
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Summary" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$passed = ($results.Values | Where-Object { $_ }).Count
$total = $results.Count
$color = if ($passed -eq $total) { "Green" } elseif ($passed -gt 0) { "Yellow" } else { "Red" }

Write-Host "  Tests passed: $passed / $total" -ForegroundColor $color
Write-Host ""

if ($results.NativeCopilot -or $results.WslCopilot) {
    Write-Host "  ✓ Copilot CLI is available" -ForegroundColor Green
    $env = if ($results.NativeCopilot) { "Native PowerShell" } else { "WSL" }
    Write-Host "    Recommended environment: $env" -ForegroundColor Gray
} else {
    Write-Host "  ✗ Copilot CLI not available" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Install Copilot CLI:" -ForegroundColor Yellow
    Write-Host "    npm install -g @github/copilot" -ForegroundColor White
    Write-Host "    copilot  # then /login to authenticate" -ForegroundColor White
}

Write-Host ""
