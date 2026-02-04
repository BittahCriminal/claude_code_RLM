# RLM + GitHub Copilot CLI Setup

This branch (`copilot/poc`) is **Copilot-exclusive** with dynamic environment detection for PowerShell (pwsh) and WSL.

## Quick Start

### PowerShell 7+ (Recommended)

```powershell
# 1. Run setup
.\scripts\setup.ps1

# 2. Activate environment
.\.venv\Scripts\Activate.ps1

# 3. Install Copilot CLI (if not already)
npm install -g @github/copilot

# 4. Authenticate
copilot
# Use /login command

# 5. Test
.\scripts\test-copilot.ps1

# 6. Run RLM server
python -m rlm_mcp.server
```

### WSL

```bash
# 1. Install Copilot CLI
npm install -g @github/copilot

# 2. Authenticate
copilot
# Use /login command

# 3. Setup Python environment
cd /mnt/c/path/to/repo
python -m venv .venv
source .venv/bin/activate
pip install -e rlm-mcp/

# 4. Run RLM server
python -m rlm_mcp.server
```

## Environment Detection

The provider automatically detects and adapts to your environment:

| Environment | Detection | Copilot Execution |
|-------------|-----------|-------------------|
| **PowerShell 7+** | `$PSVersionTable`, `$env:PSModulePath` | Direct `copilot` command |
| **WSL (inside)** | `/proc/version` contains "microsoft" | Direct `copilot` command |
| **CMD via WSL** | WSL available, copilot in WSL | `wsl copilot` wrapper |
| **Native Unix** | Linux/macOS platform | Direct `copilot` command |

### Check Your Environment

```powershell
# PowerShell
python -c "from rlm_mcp.providers import check_environment; e=check_environment(); print(f'{e.env_type.value}: {e.notes}')"
```

```bash
# WSL/Unix
python -c "from rlm_mcp.providers import check_environment; e=check_environment(); print(f'{e.env_type.value}: {e.notes}')"
```

## Copilot CLI Features

### Available Models

Run `/model` in Copilot CLI to see all options:

| Model | Notes |
|-------|-------|
| Claude Sonnet 4.5 | Default |
| Claude Sonnet 4 | Previous generation |
| GPT-5 | OpenAI flagship |
| GPT-5 mini | Free (no premium requests) |
| GPT-4.1 | Free (no premium requests) |

### Non-Interactive Mode

For automation (used by RLM):

```powershell
# Basic prompt
copilot -p "Summarize this code"

# With tool approval (for file operations)
copilot -p "Analyze the code in ./src" --allow-all-tools

# Specific model
copilot -p "Explain this" --model gpt-5-mini
```

### Useful Commands

| Command | Description |
|---------|-------------|
| `/login` | Authenticate with GitHub |
| `/model` | Select AI model |
| `/mcp add` | Add MCP server |
| `/agent` | Invoke specialized agent |
| `/delegate` | Async task delegation |

## RLM Usage with Copilot

### Basic Workflow

```python
# 1. Initialize with a large document
rlm_init(path="./large_document.txt")

# 2. Check status
rlm_status()

# 3. Chunk the document
rlm_chunk(size=200000, overlap=1000)

# 4. Process all chunks with Copilot
rlm_subcall_all(prompt="Extract key findings from this section")

# 5. Combine results
rlm_synthesize()
```

### Provider Info

```python
# Check Copilot availability
rlm_list_providers()

# Output includes:
# - Environment type (powershell, wsl_inside, etc.)
# - Copilot version
# - Authentication status
```

## MCP Configuration

### For Copilot CLI

Add RLM as an MCP server:

```
/mcp add rlm python -m rlm_mcp.server
```

Or in `~/.copilot/mcp.json`:

```json
{
  "mcpServers": {
    "rlm": {
      "command": "python",
      "args": ["-m", "rlm_mcp.server"]
    }
  }
}
```

### For Claude Desktop

In `%APPDATA%\Claude\claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "rlm": {
      "command": "python",
      "args": ["-m", "rlm_mcp.server"],
      "cwd": "C:\\path\\to\\repo\\rlm-mcp"
    }
  }
}
```

## Troubleshooting

### "copilot" not recognized

**PowerShell:**
```powershell
# Check if installed globally
npm list -g @github/copilot

# Reinstall
npm install -g @github/copilot

# Verify PATH includes npm global bin
$env:PATH -split ';' | Where-Object { $_ -like '*npm*' }
```

**WSL:**
```bash
# Check installation
which copilot

# Reinstall
npm install -g @github/copilot
```

### Authentication Issues

```powershell
# Start interactive session
copilot

# Use /login command
# Follow browser authentication
```

### Environment Detection Wrong

Set explicit mode via environment variable:

```powershell
# Force WSL mode
$env:COPILOT_USE_WSL = "1"

# Force native mode
$env:COPILOT_USE_WSL = "0"
```

### Long Prompts Failing

The provider automatically uses temp files for prompts >4000 chars. If issues persist:

```powershell
# Check temp directory access
$env:TEMP
Test-Path $env:TEMP
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     RLM MCP Server                          │
│  ┌───────────────────────────────────────────────────────┐ │
│  │              CopilotProvider                          │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │         Environment Detection                   │  │ │
│  │  │  • PowerShell 7+ → Direct copilot              │  │ │
│  │  │  • WSL inside    → Direct copilot              │  │ │
│  │  │  • CMD + WSL     → wsl copilot wrapper         │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │         Command Builder                         │  │ │
│  │  │  copilot -p "prompt" --allow-all-tools         │  │ │
│  │  │  [--model X] [extra_args]                      │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │         Path Conversion (WSL)                   │  │ │
│  │  │  C:\Users\X\file → /mnt/c/Users/X/file         │  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   GitHub Copilot CLI                         │
│        (Claude Sonnet 4.5, GPT-5, GPT-5 mini, etc.)         │
│                Uses your Copilot subscription                │
└─────────────────────────────────────────────────────────────┘
```

## Files in This Branch

| Path | Description |
|------|-------------|
| `rlm-mcp/rlm_mcp/providers/copilot.py` | Dynamic Copilot provider |
| `rlm-mcp/rlm_mcp/providers/__init__.py` | Copilot-only exports |
| `scripts/setup.ps1` | PowerShell setup script |
| `scripts/test-copilot.ps1` | Environment test script |
| `scripts/setup-windows.cmd` | CMD setup (calls WSL) |
| `docs/COPILOT_CLI_SETUP.md` | This documentation |
