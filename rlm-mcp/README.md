# RLM MCP Server

**Provider-agnostic Recursive Language Model implementation via MCP**

Process documents that exceed typical context window limits by orchestrating subcalls to various CLI tools - **no API pay-as-you-go billing required**.

## Overview

RLM (Recursive Language Model) enables handling inputs up to two orders of magnitude beyond model context windows. This MCP server implements RLM using CLI tools rather than direct API calls, meaning you use your existing subscriptions and free tiers.

### Supported CLI Providers

| Provider | CLI Tool | Billing | Notes |
|----------|----------|---------|-------|
| **Gemini** | `gemini` | Free tier (60 req/min, 1000/day) | 1M token context |
| **OpenCode** | `opencode` | Your configured providers | 75+ backends |
| **Claude Code** | `claude` | Your subscription | Opus/Sonnet/Haiku |
| **Copilot** | `gh copilot` | Your subscription | Code-focused |

## Installation

### 1. Install the MCP Server

```bash
cd rlm-mcp
pip install -e .
```

### 2. Install Your Preferred CLI Tool(s)

**Gemini CLI** (Recommended for free tier):
```bash
npm install -g @google/gemini-cli
gemini  # Follow browser auth
```

**OpenCode**:
```bash
# See https://github.com/opencode-ai/opencode for install options
brew install opencode  # macOS
```

**Claude Code**:
```bash
npm install -g @anthropic-ai/claude-code
claude login
```

**GitHub Copilot CLI**:
```bash
gh extension install github/gh-copilot
gh auth login
```

### 3. Configure Your MCP Client

Add to your MCP client configuration (e.g., Claude Desktop, OpenCode, etc.):

```json
{
  "mcpServers": {
    "rlm": {
      "command": "python",
      "args": ["-m", "rlm_mcp.server"],
      "cwd": "/path/to/rlm-mcp"
    }
  }
}
```

Or using the installed script:
```json
{
  "mcpServers": {
    "rlm": {
      "command": "rlm-mcp"
    }
  }
}
```

## Usage

### Basic Workflow

1. **Initialize** - Load your large document:
   ```
   rlm_init(path="/path/to/large_document.txt")
   ```

2. **Scout** - Preview the content:
   ```
   rlm_peek(start=0, end=2000)
   rlm_grep(pattern="important term")
   ```

3. **Set Provider** - Choose your CLI tool:
   ```
   rlm_set_provider(provider="gemini")
   ```

4. **Chunk** - Split into manageable pieces:
   ```
   rlm_chunk(size=200000, overlap=1000)
   ```

5. **Process** - Analyze each chunk:
   ```
   rlm_subcall_all(prompt="Summarize the key points in this section")
   ```

6. **Synthesize** - Combine results:
   ```
   rlm_synthesize()
   ```

### Available Tools

| Tool | Description |
|------|-------------|
| `rlm_init` | Load a document into state |
| `rlm_status` | Show current state (doc, chunks, results) |
| `rlm_peek` | Preview document content |
| `rlm_grep` | Search document with regex |
| `rlm_chunk` | Split document into chunks |
| `rlm_subcall` | Process a single chunk |
| `rlm_subcall_all` | Process all chunks (with parallelism) |
| `rlm_synthesize` | Combine all results |
| `rlm_set_provider` | Configure CLI provider |
| `rlm_list_providers` | Show available providers |
| `rlm_add_buffer` | Store intermediate text |
| `rlm_get_buffers` | Retrieve stored text |
| `rlm_reset` | Clear all state |
| `rlm_export_results` | Export results as JSON |

## Example: Analyzing a Large SEC Filing

```python
# 1. Load the document
rlm_init(path="./10k_filing.txt")
# Output: {"success": true, "document": {"char_count": 428000, ...}}

# 2. Check what providers are available
rlm_list_providers()
# Output shows which CLIs are installed and authenticated

# 3. Set provider to Gemini (free tier)
rlm_set_provider(provider="gemini")

# 4. Chunk the document (200K chars ~ 50K tokens)
rlm_chunk(size=200000, overlap=2000)
# Output: {"chunk_count": 3, ...}

# 5. Process all chunks
rlm_subcall_all(
    prompt="Extract all financial metrics and their values from this section. Format as a list.",
    parallel=2  # Process 2 chunks at a time
)

# 6. Combine results
rlm_synthesize()
# Output: Combined analysis from all chunks
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MCP Client (Root LLM)                     │
│               (Claude Desktop, OpenCode, etc.)               │
└─────────────────────────┬───────────────────────────────────┘
                          │ MCP Protocol
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      RLM MCP Server                          │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                   State Manager                      │    │
│  │  • Document context    • Chunk boundaries            │    │
│  │  • Processing results  • Intermediate buffers        │    │
│  └─────────────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                  Provider Layer                      │    │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │    │
│  │  │ Gemini  │ │OpenCode │ │ Claude  │ │ Copilot │   │    │
│  │  │   CLI   │ │   CLI   │ │  Code   │ │   CLI   │   │    │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │    │
│  └───────┼──────────┼──────────┼──────────┼─────────┘    │
└──────────┼──────────┼──────────┼──────────┼──────────────┘
           │          │          │          │
           ▼          ▼          ▼          ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ gemini   │ │ opencode │ │ claude   │ │ gh       │
    │ (subprocess)           │ (subprocess)│ copilot  │
    └──────────┘ └──────────┘ └──────────┘ └──────────┘
         │            │            │            │
         ▼            ▼            ▼            ▼
    [Free Tier]  [Your Config] [Subscription] [Subscription]
```

## Provider Details

### Gemini CLI
- **Best for**: Free usage, large contexts (1M tokens)
- **Limits**: 60 requests/minute, 1000 requests/day
- **Install**: `npm install -g @google/gemini-cli`
- **Auth**: Browser-based OAuth

### OpenCode
- **Best for**: Using existing provider configs (AWS Bedrock, Azure, Ollama, etc.)
- **Limits**: Depends on your configured provider
- **Install**: See [opencode-ai/opencode](https://github.com/opencode-ai/opencode)
- **Auth**: Per-provider configuration

### Claude Code
- **Best for**: High-quality analysis with Claude models
- **Limits**: Based on your subscription
- **Install**: `npm install -g @anthropic-ai/claude-code`
- **Auth**: `claude login`

### GitHub Copilot CLI
- **Best for**: Code-focused analysis
- **Limits**: Based on your Copilot subscription
- **Install**: `gh extension install github/gh-copilot`
- **Auth**: `gh auth login`

## Configuration

### State Directory

By default, state is stored in `.rlm_mcp_state/`. To customize:

```python
from rlm_mcp.state import StateManager
sm = StateManager(state_dir="/custom/path")
```

### Provider Timeouts

Default timeout is 5 minutes. To adjust:

```python
from rlm_mcp.providers import GeminiProvider, ProviderConfig

config = ProviderConfig(
    name="gemini",
    command="gemini",
    timeout_seconds=600,  # 10 minutes
)
provider = GeminiProvider(config)
```

## Comparison with Original RLM Skill

| Feature | Original RLM Skill | RLM MCP Server |
|---------|-------------------|----------------|
| Interface | Claude Code only | Any MCP client |
| Sub-LLM | Claude Haiku only | Gemini, OpenCode, Claude, Copilot |
| Billing | API usage | CLI subscriptions/free tiers |
| Portability | Claude Code specific | Works with any MCP-compatible tool |

## Contributing

Contributions welcome! Areas of interest:
- Additional CLI providers (Ollama, LMStudio, etc.)
- Enhanced chunking strategies (semantic, by section)
- Better synthesis/aggregation tools
- Streaming support

## License

MIT License - See LICENSE file for details.

## References

- [Recursive Language Models](https://arxiv.org/abs/example) - Zhang, Kraska & Khattab (MIT CSAIL)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [OpenCode](https://github.com/opencode-ai/opencode)
