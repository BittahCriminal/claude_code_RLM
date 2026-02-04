# Project instructions

## Knowledge Base Query

This repository has a knowledge base with 130+ imported books and documentation across 24 agent domains.

**To answer questions from the knowledge base, use the `/kb-query` skill:**

```bash
# List available agents
python3 knowledge/query.py list

# Search an agent's knowledge
python3 knowledge/query.py search kratix "promise workflow"

# Get agent details
python3 knowledge/query.py list dagger
```

**Available agents include:**
- **kratix** - Platform orchestration, Promises
- **dagger** - CI/CD pipelines, SDKs
- **radius** - Multi-cloud apps, Bicep
- **argocd** - GitOps, Argo Workflows
- **kubernetes** - K8s, AKS, K3s
- **azure-architecture** - Azure certs, WAF
- **security-offensive** - Pentest, forensics
- **data-science** - ML, AI, LLMs
- **software-architecture** - Microservices, patterns
- Run `python3 knowledge/query.py list` for all agents

## RLM mode for long-context tasks

This repository includes a minimal "Recursive Language Model" (RLM) setup for Claude Code:
- Skill: `rlm` in `.claude/skills/rlm/`
- Skill: `kb-query` in `.claude/skills/kb-query/` (knowledge base queries)
- Subagent (sub-LLM): `rlm-subcall` in `.claude/agents/`
- Persistent Python REPL: `.claude/skills/rlm/scripts/rlm_repl.py`
- Knowledge query: `knowledge/query.py`

When the user needs you to work over a context that is too large to paste into chat:
1) Ask for (or locate) a context file path.
2) Run the `/rlm` Skill and follow its procedure.

For knowledge base queries:
1) Identify the relevant agent domain
2) Use `/kb-query` or `python3 knowledge/query.py search <agent> "<query>"`
3) Read relevant chunks and synthesize the answer

Keep the main conversation light: use the REPL and subagent to do chunk-level work, then synthesise.
