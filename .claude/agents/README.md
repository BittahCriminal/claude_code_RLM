# Domain Experts - Azure, Platform Engineering, Score, Books

This directory contains domain-specific expert agents for analyzing Azure architectures, platform engineering patterns, Score workload specifications, and technical books.

## Available Agents (8 total)

### Core RLM
1. **rlm-subcall** - Generic chunk analyzer for any large context

### Azure Experts (4)
2. **azure-architecture-expert** - Cloud Adoption Framework, Well-Architected, landing zones
3. **azure-iam-expert** - Entra ID, RBAC, Managed Identities, authentication
4. **azure-networking-expert** - VNets, VPN Gateway, ExpressRoute, hybrid connectivity
5. **azure-security-expert** - Defender for Cloud, Sentinel, security posture, best practices

### Specialized Domains (3)
6. **books-expert** - Technical books on cloud, Kubernetes, platform engineering
7. **platform-engineering-expert** - IDPs, Backstage, golden paths, developer experience
8. **score-expert** - Score workload specifications, platform-agnostic deployments

## Context/Knowledge Base

### Azure Contexts
- **azure_radius_full.txt** (19KB) - Azure Radius, Landing Zones, CAF
  - Usage: Azure architecture questions

### Azure Security Contexts
- **Azure-Sentinel.pdf** - Azure Sentinel best practices whitepaper
  - Path: `/Users/bittahcriminal/workspace/Platform-Engineering-RLM/Docs/Azure-Sentinel.pdf`
  - Usage: Sentinel incident response and data ingestion guidance
  - Latest guidance: query Azure MCP server (container `magical_zhukovsky`) and pass inline
  
### Platform Engineering
- **platform_engineering_full.txt** (1.6MB) - IDP patterns, Backstage, Team Topologies
  - Usage: Platform engineering best practices

### Score Workloads
- **score_full.txt** (11KB) - Score specification, score-compose, score-k8s
  - Usage: Workload portability, Score YAML questions

### Books (12 titles, ~9MB total)
Located in `books/` subdirectory:

#### Azure Books (4)
- Azure Cloud Projects (Hamid Sadeghpour)
- Azure Data and AI Architect Handbook (Olivier Mertens)
- Azure DevOps Explained
- Azure for Developers (Kamil Mrzygłód)

#### Platform Engineering Books (2)
- Mastering Enterprise Platform Engineering (Mark Peters)
- Platform Engineering for Architects (Max Körbächer)

#### Kubernetes Books (5)
- Implementing GitOps with Kubernetes (Pietro Libro)
- Kubernetes for Generative AI Solutions (Ashok Srirama)
- The Kubernetes Bible (Gineesh Madapparambath)
- Certified Kubernetes Administrator Study Companion
- C# 13 and .NET 9 (includes K8s sections)

## Usage with Claude CLI

### Invoke Specific Agent
```bash
claude

# Azure architecture question
"Use azure-architecture-expert to analyze this landing zone config: [paste config]"

# Platform engineering question
"Use platform-engineering-expert to answer: What is a golden path?"

# Books question
"Use books-expert to find references on Azure AKS best practices"
```

### RLM with Large Context
```bash
# Process large Azure architecture doc
/rlm context=large_caf_doc.txt query="What are the landing zone recommendations?"
# Claude will auto-select azure-architecture-expert if detected

# Process platform engineering book
/rlm context=platform_book.txt query="Summarize the IDP patterns"
# Claude will auto-select books-expert
```

## Usage with GitHub Copilot CLI

### Automatic Routing
```bash
copilot

# Copilot reads AGENTS.md and routes automatically
"What are Azure landing zone best practices?"
# → Routes to azure-architecture-expert

"What do books say about Backstage implementation?"
# → Routes to books-expert + platform-engineering-expert

"Create a Score workload for Azure Functions"
# → Routes to score-expert + azure-architecture-expert
```

### Manual Agent Invocation
```python
# Load agent template
agent_prompt = read(".github/agent_templates/azure-architecture-expert.txt")
context = read(".claude/rlm_contexts/azure_radius_full.txt")

# Invoke with task tool
task({
  agent_type: "task",
  model: "claude-haiku-4.5",
  description: "Analyzing Azure landing zones",
  prompt: f"{agent_prompt}\n\nContext:\n{context}\n\nQuery: {user_query}"
})
```

## Agent Output Format

All agents return JSON with this structure:

```json
{
  "chunk_id": "identifier",
  "relevant": [
    {
      "point": "key finding",
      "evidence": "quote from source",
      "confidence": "high|medium|low"
    }
  ],
  "missing": ["information not found"],
  "suggested_next_queries": ["follow-up questions"],
  "answer_if_complete": "answer or null"
}
```

### Domain-Specific Extensions

**Azure experts add:**
```json
{
  "azure_services": ["list", "of", "services"],
  "iac_snippets": [{"description": "...", "language": "terraform", "code": "..."}],
  "caf_phase": "which CAF phase"
}
```

**Books expert adds:**
```json
{
  "book_title": "extracted from chunk",
  "chapters_covered": ["chapter names"],
  "authors": ["author names"],
  "topic_tags": ["relevant", "tags"]
}
```

**Platform engineering adds:**
```json
{
  "patterns": ["idp-pattern-1", "team-topology-2"],
  "tools": ["backstage", "crossplane"],
  "maturity_level": "nascent|emerging|mature"
}
```

**Score expert adds:**
```json
{
  "score_version": "detected version",
  "resources": ["resource types in spec"],
  "target_platforms": ["kubernetes", "docker-compose"]
}
```

## Context File Details

### azure_radius_full.txt (19KB)
- Source: Azure Radius documentation
- Topics: Landing zones, CAF, management groups
- Format: Markdown documentation
- Best for: Architecture design questions

### platform_engineering_full.txt (1.6MB)
- Source: Compiled platform engineering content
- Topics: IDPs, Backstage, golden paths, Team Topologies
- Format: Mixed markdown and code examples
- Best for: Platform strategy and patterns

### score_full.txt (11KB)
- Source: Score specification docs
- Topics: Score YAML format, score-compose, score-k8s
- Format: Specification + examples
- Best for: Workload portability questions

### Books Directory (9MB)
- Format: Extracted EPUB content (pre-chunked)
- Includes: Metadata headers with book/chapter info
- Organized: One file per book
- Search: Use books-expert agent for discovery

## Adding New Agents

### 1. Create Claude CLI Agent
```bash
# Create .claude/agents/new-expert.md
cat > .claude/agents/new-expert.md << 'EOF'
---
name: new-expert
description: Expert description
tools: Read
model: haiku
---

You are a [DOMAIN] expert...

[Instructions...]
EOF
```

### 2. Create Copilot CLI Template
```bash
# Strip YAML and save to .github/agent_templates/
sed '1{/^---$/!q;};1,/^---$/d' .claude/agents/new-expert.md > .github/agent_templates/new-expert.txt
```

### 3. Add Context File
```bash
# Copy or create context in .claude/rlm_contexts/
cp /path/to/knowledge.txt .claude/rlm_contexts/new_domain_full.txt
```

### 4. Update AGENTS.md
Add agent to registry with:
- Purpose
- Model
- Context path
- Trigger keywords
- Routing logic

### 5. Update Helper Script
Add to `scripts/rlm_copilot_helper.py` if custom loading logic needed.

## Testing Agents

### Test Agent Template
```bash
# Verify template loads
python3 scripts/rlm_copilot_helper.py load-agent azure-architecture-expert

# Should print full agent prompt
```

### Test Context Files
```bash
# Check context exists and is readable
ls -lh .claude/rlm_contexts/azure_radius_full.txt
head -n 50 .claude/rlm_contexts/azure_radius_full.txt
```

### Test with Claude CLI
```bash
claude

# Test single agent
"Use azure-architecture-expert to explain Azure landing zones"

# Test RLM with context
/rlm context=.claude/rlm_contexts/azure_radius_full.txt query="What is CAF?"
```

### Test with Copilot CLI
```bash
copilot

# Test auto-routing
"What are Azure landing zone best practices?"

# Test multi-agent
"Compare platform engineering patterns in books vs Azure CAF"
```

## Maintenance

### Keep Agents in Sync
When updating agent instructions:
1. Edit `.claude/agents/<agent>.md`
2. Regenerate Copilot template:
   ```bash
   sed '1{/^---$/!q;};1,/^---$/d' .claude/agents/<agent>.md > .github/agent_templates/<agent>.txt
   ```
3. Test with both CLIs

### Update Contexts
When new documentation is available:
1. Fetch/compile new content
2. Replace file in `.claude/rlm_contexts/`
3. Update size/description in this README
4. Re-test agents

### Add New Books
```bash
# Copy book context
cp /source/new-book_full.txt .claude/rlm_contexts/books/

# Update books-expert description
# Test with books-expert agent
```

## Troubleshooting

**Agent not found (Copilot CLI):**
- Check `.github/agent_templates/<agent>.txt` exists
- Verify AGENTS.md has agent listed
- Try: `python3 scripts/rlm_copilot_helper.py load-agent <agent>`

**Context not loading:**
- Check file path in `.claude/rlm_contexts/`
- Verify file is readable (not binary)
- Check file size (very large files may need chunking)

**Inconsistent results between CLIs:**
- Verify agent templates are in sync
- Check context files are identical
- Review JSON schema compatibility

**Book content not found:**
- List books: `ls .claude/rlm_contexts/books/`
- Check book filename matches pattern
- Use books-expert to search across all books

## See Also

- `AGENTS.md` - Full agent registry with routing logic
- `COPILOT_CLI_GUIDE.md` - GitHub Copilot CLI usage guide
- `README.md` - Main project documentation
- `.claude/skills/rlm/SKILL.md` - RLM skill definition (Claude CLI)
