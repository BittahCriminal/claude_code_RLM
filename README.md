# Claude Code RLM

A minimal implementation of Recursive Language Models (RLM) for **Claude CLI** and **GitHub Copilot CLI**. Implemented by [Brainqub3](https://brainqub3.com/).

## About

This repository provides a basic RLM setup that enables AI assistants to process documents and contexts that exceed typical context window limits. It implements the core RLM pattern where a root language model orchestrates sub-LLM calls over chunks of a large document.

**This is a basic implementation** of the RLM paper. For the full research, see:

> **Recursive Language Models**
> Alex L. Zhang, Tim Kraska, Omar Khattab
> MIT CSAIL
> [arXiv:2512.24601](https://arxiv.org/abs/2512.24601)

*Abstract: RLMs treat long prompts as part of an external environment and allow the LLM to programmatically examine, decompose, and recursively call itself over snippets of the prompt. RLMs can handle inputs up to two orders of magnitude beyond model context windows.*

### Dual CLI Support

This repository now supports **both Claude CLI and GitHub Copilot CLI**, giving you flexibility in which AI assistant you use.

## Architecture

This implementation maps to the RLM paper architecture as follows:

| RLM Concept | Claude CLI | GitHub Copilot CLI |
|-------------|-----------|-------------------|
| Root LLM | Main conversation (Opus 4.5) | Main conversation (Sonnet 4.5) |
| Sub-LLM (`llm_query`) | `rlm-subcall` agent (auto-discovered) | `task` tool + agent template (Haiku 4.5) |
| External Environment | Persistent Python REPL (`rlm_repl.py`) | Same REPL (shared) |

### Key Differences

- **Claude CLI**: Uses `.claude/agents/rlm-subcall.md` with auto-discovery and skill system (`/rlm`)
- **Copilot CLI**: Uses `.github/agent_templates/rlm-subcall.txt` with manual `task` tool invocation
- **Both**: Share the same Python REPL and chunking logic for consistency

The root LLM orchestrates the overall task, while delegating chunk-level analysis to the faster, lighter sub-LLM (Haiku). The Python REPL maintains state across invocations and provides utilities for chunking, searching, and managing the large context.

## Capabilities

- RLM chunking via a persistent Python REPL with reusable state.
- Domain expert routing for Azure, platform engineering, Score, and books via `AGENTS.md`.
- Non-interactive RLM runner supporting OpenCode, Claude, Codex, Copilot, and Gemini CLIs.
- Provider model selection by explicit `--model`, domain presets, env vars, or defaults.

## How It Works (Detailed Diagram)

```mermaid
flowchart TD
    A[User Query] --> B[Root CLI<br/>Claude/Copilot/OpenCode/Codex/Gemini]
    B -->|1) init context| C[rlm_repl.py<br/>persistent state]
    C -->|2) chunk context| D[.claude/rlm_state/chunks<br/>chunk_0000...chunk_N]
    D -->|3) per-chunk analysis| E[Sub-LLM calls<br/>rlm-subcall or provider run]
    E -->|4) JSON findings| F[Aggregated chunk analyses]
    F -->|5) synthesize| G[Root CLI response]
```

## Prerequisites

**Choose one CLI:**
- **Claude CLI** - Access to [Claude Code](https://claude.ai/claude-code), Anthropic's official CLI tool
- **GitHub Copilot CLI** - Active Copilot subscription ([installation guide](https://docs.github.com/copilot))

**Required for both:**
- **Python 3** - For the persistent REPL environment

## Usage

1. **Clone this repository**
   ```bash
   git clone https://github.com/Brainqub3/claude_code_RLM.git
   cd claude_code_RLM
   ```

2. **Start your preferred CLI in the repository directory**

### Option A: Claude CLI

```bash
claude
```

3. **Run the RLM skill**
   ```
   /rlm
   ```

4. **Follow the prompts** - The skill will ask for:
   - A path to your large context file
   - Your query/question about the content

### Option B: GitHub Copilot CLI

```bash
copilot
```

3. **Request RLM processing**
   ```
   Process large_file.txt using RLM pattern and answer: "What are the main topics?"
   ```

4. **Copilot will automatically**:
   - Load the agent template from `AGENTS.md`
   - Initialize the REPL with your context
   - Chunk the document
   - Invoke multiple `task` calls in parallel for each chunk
   - Synthesize the results

**Alternative (manual control)**:
```bash
# 1. Initialize REPL
python3 .claude/skills/rlm/scripts/rlm_repl.py init large_file.txt

# 2. Prepare chunks
python3 scripts/rlm_copilot_helper.py prepare-chunks "your query" .claude/rlm_state/chunks

# 3. Tell Copilot CLI:
"Using the chunk invocations prepared, analyze all chunks in parallel"
```

### Both CLIs will:
- Initialize the REPL with your context
- Chunk the document appropriately
- Delegate chunk analysis to the sub-LLM (Haiku)
- Synthesize results in the main conversation

### Non-Interactive RLM Runner (OpenCode/Claude/Codex)

If you want to run the RLM loop non-interactively via a CLI provider, use:

```bash
python3 scripts/opencode_rlm_runner.py --context path/to/context.txt --query "your question"
```

Options:
- `--provider opencode|claude|codex|copilot|gemini|auto` (default: opencode)
- `--model provider/model` (optional)
- `--domain general|software|extra-thinking|security|cloud-architecture|devops|data-engineering|ml-ai|frontend|backend|testing|code-review|docs` (optional)
- `--agent <agent>` (optional)
- `--chunk-size 200000` and `--overlap 0`

Gemini support assumes a `gemini` CLI that accepts the prompt as the last argument and optional `--model`.

Model resolution order:
- `--model` flag
- `--domain` preset
- Provider-specific env var: `OPENCODE_MODEL`, `CLAUDE_MODEL`, `CODEX_MODEL`, `COPILOT_MODEL`, `GEMINI_MODEL`
- Built-in defaults (see `scripts/opencode_rlm_runner.py`)

Auto provider selection (when `--provider auto`):
- Picks the first available CLI on PATH in this order: `opencode`, `claude`, `codex`, `copilot`, `gemini`.

The script writes its full output to:
`.claude/rlm_state/opencode_run.json`

## Working with Long Files

When using RLM to process large context files, it is recommended to save them in a dedicated `context/` folder within this project directory. This keeps your working files organized and separate from the RLM implementation code.

```bash
mkdir context
# Place your large documents here, e.g.:
# context/my_large_document.txt
# context/codebase_dump.py
```

## Security Warning

**This project is not intended for production use.**

If you plan to run Claude Code in `--dangerously-skip-permissions` mode:

1. **Ensure your setup is correct** - Verify all file paths and configurations before enabling this mode
2. **Run in an isolated folder** - Never run with skipped permissions in directories containing sensitive data, credentials, or system files
3. **Understand the risks** - This mode allows Claude to execute commands without confirmation prompts, which can lead to unintended file modifications or deletions

**Recommended**: Create a dedicated, isolated working directory specifically for RLM tasks when using dangerous mode:

```bash
# Example: Create an isolated workspace
mkdir ~/rlm-workspace
cd ~/rlm-workspace
git clone https://github.com/Brainqub3/claude_code_RLM.git
cd claude_code_RLM
```

## Repository Structure

```
.
├── CLAUDE.md                          # Project instructions for Claude CLI
├── AGENTS.md                          # Agent registry for GitHub Copilot CLI
├── .claude/
│   ├── agents/
│   │   └── rlm-subcall.md            # Agent for Claude CLI (auto-discovered)
│   └── skills/
│       └── rlm/
│           ├── SKILL.md              # RLM skill for Claude CLI
│           └── scripts/
│               └── rlm_repl.py       # Persistent Python REPL (shared by both CLIs)
├── .github/
│   └── agent_templates/
│       └── rlm-subcall.txt           # Agent template for Copilot CLI (manually loaded)
├── scripts/
│   ├── opencode_rlm_runner.py        # Non-interactive RLM runner
│   └── rlm_copilot_helper.py         # Helper for Copilot CLI workflows
├── context/                           # Recommended location for large context files
└── README.md
```

### File Purposes

| File | Claude CLI | Copilot CLI | Purpose |
|------|-----------|-------------|---------|
| `.claude/agents/rlm-subcall.md` | ✅ Used | ❌ Ignored | Auto-discovered agent |
| `.github/agent_templates/rlm-subcall.txt` | ❌ Ignored | ✅ Used | Manually loaded template |
| `AGENTS.md` | ❌ Ignored | ✅ Used | Agent routing logic |
| `.claude/skills/rlm/scripts/rlm_repl.py` | ✅ Used | ✅ Used | **Shared** REPL |
| `scripts/rlm_copilot_helper.py` | ❌ N/A | ✅ Used | Copilot-specific helper |
| `scripts/opencode_rlm_runner.py` | ❌ N/A | ✅ Used | Non-interactive RLM loop |

## License

See [LICENSE](LICENSE) for details.
