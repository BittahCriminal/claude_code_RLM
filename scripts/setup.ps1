#Requires -Version 7.0
<#
.SYNOPSIS
    RLM + Copilot CLI Setup Script for PowerShell 7+

.DESCRIPTION
    Sets up the environment for running RLM with GitHub Copilot CLI.
    Supports both native PowerShell and WSL execution paths.

.EXAMPLE
    .\setup.ps1

.EXAMPLE
    .\setup.ps1 -SkipVenv
#>

[CmdletBinding()]
param(
    [switch]$SkipVenv,
    [switch]$Force
)

$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Status, [string]$Message, [string]$Color = "White")
    $statusColors = @{
        "OK"   = "Green"
        "WARN" = "Yellow"
        "ERR"  = "Red"
        "INFO" = "Cyan"
    }
    $c = if ($statusColors[$Status]) { $statusColors[$Status] } else { $Color }
    Write-Host "[$Status] " -ForegroundColor $c -NoNewline
    Write-Host $Message
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  RLM + Copilot CLI Setup (PowerShell)" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check PowerShell version
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -lt 7) {
    Write-Status "ERR" "PowerShell 7+ required. Current: $psVersion"
    Write-Host "Install with: winget install Microsoft.PowerShell" -ForegroundColor Yellow
    exit 1
}
Write-Status "OK" "PowerShell version: $psVersion"

# Check for Python
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Status "ERR" "Python not found in PATH"
    Write-Host "Install from https://python.org or: winget install Python.Python.3.12" -ForegroundColor Yellow
    exit 1
}
$pyVersion = & python --version 2>&1
Write-Status "OK" "Python: $pyVersion"

# Check for Node.js
$node = Get-Command node -ErrorAction SilentlyContinue
if (-not $node) {
    Write-Status "WARN" "Node.js not found - needed for Copilot CLI"
    Write-Host "  Install: winget install OpenJS.NodeJS.LTS" -ForegroundColor Yellow
} else {
    $nodeVersion = & node --version 2>&1
    Write-Status "OK" "Node.js: $nodeVersion"
}

# Check for Copilot CLI (native)
$copilot = Get-Command copilot -ErrorAction SilentlyContinue
if ($copilot) {
    $copilotVersion = & copilot --version 2>&1 | Select-Object -First 1
    Write-Status "OK" "Copilot CLI (native): $copilotVersion"
} else {
    Write-Status "INFO" "Copilot CLI not found in PATH"

    # Check WSL
    $wsl = Get-Command wsl -ErrorAction SilentlyContinue
    if ($wsl) {
        $wslCopilot = & wsl which copilot 2>$null
        if ($wslCopilot) {
            Write-Status "OK" "Copilot CLI found in WSL"
        } else {
            Write-Status "WARN" "Copilot CLI not in WSL either"
            Write-Host ""
            Write-Host "Install Copilot CLI:" -ForegroundColor Yellow
            Write-Host "  Native (pwsh): npm install -g @github/copilot" -ForegroundColor White
            Write-Host "  WSL:           wsl npm install -g @github/copilot" -ForegroundColor White
        }
    } else {
        Write-Status "WARN" "WSL not available"
        Write-Host "  Install Copilot: npm install -g @github/copilot" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "------------------------------------------------------------" -ForegroundColor Gray
Write-Host "  Setting up Python environment..." -ForegroundColor Cyan
Write-Host "------------------------------------------------------------" -ForegroundColor Gray

# Get script directory and move to repo root
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent $scriptDir
Push-Location $repoRoot

try {
    if (-not $SkipVenv) {
        if (Test-Path ".venv") {
            Write-Status "INFO" "Virtual environment already exists"
        } else {
            Write-Status "INFO" "Creating virtual environment..."
            & python -m venv .venv
            if ($LASTEXITCODE -ne 0) { throw "Failed to create venv" }
            Write-Status "OK" "Virtual environment created"
        }

        # Activate venv
        $activateScript = ".\.venv\Scripts\Activate.ps1"
        if (Test-Path $activateScript) {
            . $activateScript
            Write-Status "OK" "Virtual environment activated"
        }
    }

    # Install RLM MCP server
    Write-Status "INFO" "Installing RLM MCP server..."
    & pip install -e ".\rlm-mcp\" --quiet
    if ($LASTEXITCODE -ne 0) { throw "Failed to install rlm-mcp" }
    Write-Status "OK" "RLM MCP server installed"

} finally {
    Pop-Location
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  Setup Complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Activate environment: .\.venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "  2. Install Copilot CLI (if not done):" -ForegroundColor White
Write-Host "       npm install -g @github/copilot" -ForegroundColor Gray
Write-Host "  3. Authenticate: copilot (follow /login)" -ForegroundColor White
Write-Host "  4. Test: .\scripts\test-copilot.ps1" -ForegroundColor White
Write-Host "  5. Run server: python -m rlm_mcp.server" -ForegroundColor White
Write-Host ""
