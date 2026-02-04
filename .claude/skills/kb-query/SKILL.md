---
name: kb-query
description: Query the knowledge base for a specific agent domain. Use this to answer questions using imported books, documentation, and web content.
allowed-tools:
  - Read
  - Bash
  - Task
---

# kb-query (Knowledge Base Query)

Use this Skill when:
- The user asks a question that can be answered from imported knowledge (books, docs, web)
- The user wants to query a specific agent's knowledge base
- You need to find information from the imported documentation

## Available Agents

Run this to see available agents and their knowledge:
```bash
python3 knowledge/query.py list
```

## How to run

### Step 1: Identify the agent domain

Based on the user's question, identify which agent domain is most relevant:
- **kratix** - Platform orchestration, Promises, IDP
- **dagger** - CI/CD pipelines, containers, SDKs
- **radius** - Multi-cloud apps, Bicep, Recipes
- **argocd** - GitOps, Argo Workflows
- **kubernetes** - K8s, AKS, MicroK8s, K3s
- **azure-architecture** - Azure certifications, WAF, CAF
- **security-offensive** - Pentest, hacking, forensics
- **data-science** - ML, AI, deep learning
- **software-architecture** - Microservices, patterns
- (and many more - run `python3 knowledge/query.py list` to see all)

### Step 2: Search the knowledge base

```bash
python3 knowledge/query.py search <agent> "<search terms>"
```

Example:
```bash
python3 knowledge/query.py search kratix "promise workflow pipeline"
```

### Step 3: Read relevant chunks

The search results show chunk paths. Read the most relevant ones:
```bash
# Use the Read tool to read chunk files
```

### Step 4: For comprehensive queries, use RLM subcall

If the question requires processing multiple chunks, combine the agent's knowledge and use the RLM workflow:

```bash
# Combine all knowledge for the agent
python3 knowledge/query.py combine <agent> .claude/rlm_state/context.txt

# Initialize RLM with combined context
python3 .claude/skills/rlm/scripts/rlm_repl.py init .claude/rlm_state/context.txt

# Check status
python3 .claude/skills/rlm/scripts/rlm_repl.py status
```

Then use the rlm-subcall subagent to process chunks and synthesize the answer.

### Step 5: Answer the question

Synthesize the information from the chunks to answer the user's question.
Include references to the source material when helpful.

## Quick Reference

```bash
# List all agents with knowledge
python3 knowledge/query.py list

# List knowledge for specific agent
python3 knowledge/query.py list kratix

# Search agent's knowledge
python3 knowledge/query.py search kratix "promises"

# Get chunk paths for a knowledge entry
python3 knowledge/query.py chunks kratix_web_a1934b82a3b8e052

# Combine agent knowledge into single file
python3 knowledge/query.py combine kratix .claude/rlm_state/kratix_context.txt
```

## Example Workflow

User asks: "How do I create a Kratix Promise?"

1. Identify agent: `kratix`
2. Search: `python3 knowledge/query.py search kratix "create promise"`
3. Read top matching chunks
4. Synthesize answer with code examples from the documentation
