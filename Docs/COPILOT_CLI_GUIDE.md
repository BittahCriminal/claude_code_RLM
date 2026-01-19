# GitHub Copilot CLI Quick Start

This guide shows how to use RLM with GitHub Copilot CLI specifically.

## Installation

```bash
# macOS/Linux
brew install copilot-cli

# npm (all platforms)
npm install -g @github/copilot

# Then launch
copilot
```

## Quick Usage

### Simple (Let Copilot orchestrate)

```
You: "Process large_document.txt using RLM and find all mentions of security"

Copilot will:
1. Read AGENTS.md for routing logic
2. Initialize REPL
3. Create chunks  
4. Invoke task() calls in parallel
5. Synthesize results
```

### Manual Control (Step-by-step)

```bash
# 1. Initialize REPL with your context
python3 .claude/skills/rlm/scripts/rlm_repl.py init context/large_file.txt

# 2. Create chunks
python3 .claude/skills/rlm/scripts/rlm_repl.py exec <<'PY'
paths = write_chunks('.claude/rlm_state/chunks', size=200000, overlap=0)
print('\n'.join(paths))
PY

# 3. Load agent template
python3 scripts/rlm_copilot_helper.py load-agent rlm-subcall

# 4. Prepare chunk invocations
python3 scripts/rlm_copilot_helper.py prepare-chunks "your query" .claude/rlm_state/chunks

# 5. Tell Copilot:
# "Using these chunk invocations, analyze all chunks in parallel with task() calls"
```

## How Copilot Uses task() Tool

For each chunk, Copilot will invoke:

```javascript
task({
  agent_type: "task",           // or "explore" for fast searches
  model: "claude-haiku-4.5",    // Fast & cheap
  description: "Analyzing chunk 1/10",
  prompt: `
    [Agent template from .github/agent_templates/rlm-subcall.txt]
    
    Chunk file: .claude/rlm_state/chunks/chunk_0000.txt
    User query: Find all security vulnerabilities
    
    Read the chunk file and return JSON with findings.
  `
})
```

## Parallel Processing

Copilot CLI can launch **multiple task calls simultaneously**:

```javascript
// All launched at once
task({...chunk_0...})
task({...chunk_1...})
task({...chunk_2...})
...
task({...chunk_9...})

// Results arrive independently
// Copilot synthesizes when all complete
```

## Differences from Claude CLI

| Feature | Claude CLI | Copilot CLI |
|---------|-----------|-------------|
| **Agent discovery** | Automatic (`.claude/agents/`) | Manual (`AGENTS.md`) |
| **Skill invocation** | `/rlm` command | Natural language request |
| **Sub-LLM calls** | Implicit | Explicit `task()` calls |
| **Parallel processing** | Sequential by default | Native parallel support |
| **Agent template** | `.claude/agents/rlm-subcall.md` | `.github/agent_templates/rlm-subcall.txt` |
| **REPL** | Same (`rlm_repl.py`) | Same (`rlm_repl.py`) |

## Example Session

```
$ copilot

You: Process the file context/transcript.txt using RLM and summarize the key decisions

Copilot: I'll use the RLM pattern to analyze this large file. Let me:

1. Initialize REPL...
   $ python3 .claude/skills/rlm/scripts/rlm_repl.py init context/transcript.txt
   ✓ Loaded 1.2MB context

2. Create chunks (200k chars each)...
   $ python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "..."
   ✓ Created 6 chunks

3. Analyzing all chunks in parallel...
   [Launches 6 task() calls simultaneously]
   
   task(agent_type="task", model="haiku", prompt="[chunk 0]...")
   task(agent_type="task", model="haiku", prompt="[chunk 1]...")
   ...
   task(agent_type="task", model="haiku", prompt="[chunk 5]...")

4. Results collected:
   - Chunk 0: Found 2 key decisions (high confidence)
   - Chunk 1: No decisions mentioned
   - Chunk 2: Found 1 decision (medium confidence)
   ...

5. Synthesized Summary:
   
   ## Key Decisions from Transcript
   
   1. **Migrate to Kubernetes** (high confidence)
      - Mentioned in chunks 0, 3
      - Timeline: Q2 2026
   
   2. **Adopt GraphQL API** (high confidence)
      - Mentioned in chunks 0, 4
      - Replace REST endpoints
   
   3. **Implement OAuth 2.1** (medium confidence)
      - Mentioned in chunk 2
      - Security requirement
```

## Tips

- **Let Copilot orchestrate**: Just ask naturally, it will follow `AGENTS.md`
- **Use helper script**: For manual control, `rlm_copilot_helper.py` prepares invocations
- **Parallel by default**: Copilot launches multiple chunks simultaneously
- **Check REPL state**: `python3 .claude/skills/rlm/scripts/rlm_repl.py status`

## Troubleshooting

**Copilot doesn't find chunks:**
```bash
# Check chunks were created
ls -la .claude/rlm_state/chunks/
```

**Agent template not found:**
```bash
# Verify template exists
cat .github/agent_templates/rlm-subcall.txt
```

**REPL state lost:**
```bash
# Re-initialize
python3 .claude/skills/rlm/scripts/rlm_repl.py init <context_file>
```

## Advanced: Custom Chunk Size

```python
# Larger chunks (300k chars)
python3 .claude/skills/rlm/scripts/rlm_repl.py exec <<'PY'
paths = write_chunks('.claude/rlm_state/chunks', size=300000, overlap=5000)
print(f"Created {len(paths)} chunks with 5k overlap")
PY
```

## More Help

- See `AGENTS.md` for routing logic
- See `.github/agent_templates/` for agent prompts
- See `scripts/rlm_copilot_helper.py` for helper commands
