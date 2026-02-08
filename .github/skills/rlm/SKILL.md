---
name: rlm
description: Run a Recursive Language Model-style loop for long-context tasks. Uses a persistent local Python REPL, domain expert agents, and an rlm-subcall subagent as the sub-LLM (llm_query).
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Task
---

# rlm (Recursive Language Model workflow)

Use this Skill when:
- The user provides (or references) a very large context file (docs, logs, transcripts, scraped webpages) that won't fit comfortably in chat context.
- You need to iteratively inspect, search, chunk, and extract information from that context.
- You can delegate chunk-level analysis to domain expert agents.

## Mental model

- Main Copilot conversation = the root LM (orchestrator).
- Persistent Python REPL (`rlm_repl.py`) = the external environment.
- Domain expert agents (`agents/`) = specialized sub-LLMs with knowledge bases.
- Subagent `rlm-subcall` = generic sub-LM for chunk extraction.

## Domain Expert Agents

Located in `agents/` directory. Use these for specialized queries:

### TRAPI/Cordillera Agents
| Agent | Path | Expertise |
|-------|------|-----------|
| `trapi` | `agents/trapi/agent.md` | TMDS service, trapi-ui, Cosmos DB, Bicep, Azure subscription |
| `trapi-batch` | `agents/trapi-batch/agent.md` | Batch processing API, Azure Functions, Service Bus |
| `trapi-python-lib` | `agents/trapi-python-lib/agent.md` | Python SDK, trapi-cli, OpenAI helpers |

### Infrastructure Agents
| Agent | Path | Expertise |
|-------|------|-----------|
| `azure-architecture` | `agents/azure-architecture/agent.md` | WAF, CAF, landing zones, solution design |
| `kubernetes` | `agents/kubernetes/agent.md` | K8s, AKS, MicroK8s, K3s |
| `dagger` | `agents/dagger/agent.md` | CI/CD pipelines, containers |

### Programming Agents
| Agent | Path | Expertise |
|-------|------|-----------|
| `csharp-engineering` | `agents/csharp-engineering/agent.md` | .NET, ASP.NET Core (for trapi-batch) |
| `python-engineering` | `agents/python-engineering/agent.md` | Python (for trapi-python-lib) |
| `javascript-engineering` | `agents/javascript-engineering/agent.md` | React, TypeScript (for trapi-ui) |

Run `ls agents/` to see all available expert agents.

## How to run

### Inputs

This Skill reads `$ARGUMENTS`. Accept these patterns:
- `context=<path>` (required): path to the file containing the large context.
- `query=<question>` (required): what the user wants.
- `agent=<agent-name>` (optional): domain expert agent to use (e.g., `trapi`, `trapi-batch`).
- Optional: `chunk_chars=<int>` (default ~200000) and `overlap_chars=<int>` (default 0).

If the user didn't supply arguments, ask for:
1) the context file path, and
2) the query.
3) Optionally suggest a domain expert agent based on the query topic.

### Step-by-step procedure

1. **Select domain expert** (if applicable)
   - Review the query topic and select an appropriate agent from `agents/`
   - Read the agent's `agent.md` to understand its capabilities and subagents
   - Example: For TRAPI batch questions, use `agents/trapi-batch/agent.md`

2. Initialise the REPL state
   ```bash
   python3 .github/skills/rlm/scripts/rlm_repl.py init <context_path>
   python3 .github/skills/rlm/scripts/rlm_repl.py status
   ```

3. Scout the context quickly
   ```bash
   python3 .github/skills/rlm/scripts/rlm_repl.py exec -c "print(peek(0, 3000))"
   python3 .github/skills/rlm/scripts/rlm_repl.py exec -c "print(peek(len(content)-3000, len(content)))"
   ```

4. Choose a chunking strategy
   - Prefer semantic chunking if the format is clear (markdown headings, JSON objects, log timestamps).
   - Otherwise, chunk by characters (size around chunk_chars, optional overlap).

5. Materialise chunks as files (so subagents can read them)
   ```bash
   python3 .github/skills/rlm/scripts/rlm_repl.py exec <<'PY'
   paths = write_chunks('.github/rlm_state/chunks', size=200000, overlap=0)
   print(len(paths))
   print(paths[:5])
   PY
   ```

6. **Subcall loop** (delegate to domain expert or rlm-subcall)
   
   **Option A: Use domain expert agent** (preferred for specialized topics)
   - Read the agent definition: `cat agents/<agent>/agent.md`
   - Use the Task tool with agent type "explore" or "general-purpose"
   - Pass the agent's system prompt, the user query, and chunk file paths
   - Agent subagents (in `agents/<agent>/subagents/`) can handle specific subtasks
   
   **Option B: Use generic rlm-subcall** (for general extraction)
   - For each chunk file, invoke the rlm-subcall subagent with:
     - the user query,
     - the chunk file path,
     - and any specific extraction instructions.
   
   - Keep subagent outputs compact and structured (JSON preferred).
   - Append each subagent result to buffers.

7. Synthesis
   - Once enough evidence is collected, synthesise the final answer in the main conversation.
   - Use the domain expert's output format if available.
   - Reference the agent's `collaborates_with` field for cross-domain questions.

## Guardrails

- Do not paste large raw chunks into the main chat context.
- Use the REPL to locate exact excerpts; quote only what you need.
- Subagents cannot spawn other subagents. Any orchestration stays in the main conversation.
- Keep scratch/state files under .github/rlm_state/.
