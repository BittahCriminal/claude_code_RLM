# Quick Reference - Domain Experts

## Available Agents

| Agent | Context | Size | Use When |
|-------|---------|------|----------|
| `rlm-subcall` | Any file | N/A | Generic large file chunking |
| `azure-architecture-expert` | azure_radius_full.txt | 19KB | Azure CAF, landing zones, compute |
| `azure-iam-expert` | N/A | - | Entra ID, RBAC, identities |
| `azure-networking-expert` | N/A | - | VNets, VPN, ExpressRoute |
| `books-expert` | books/*.txt | 9MB | Technical book references |
| `platform-engineering-expert` | platform_engineering_full.txt | 1.6MB | IDP, Backstage, golden paths |
| `score-expert` | score_full.txt | 11KB | Score workload specs |

## Quick Commands

### Claude CLI
```bash
claude

# Use specific agent
"Use azure-architecture-expert to explain [topic]"

# RLM with large context
/rlm context=file.txt query="your question"

# Multi-agent (explicit)
"Use azure-architecture-expert and platform-engineering-expert to..."
```

### Copilot CLI
```bash
copilot

# Auto-routing (recommended)
"What are Azure landing zone best practices?"

# Multi-domain
"Compare platform engineering books with Azure patterns"

# Explicit agent (if needed)
"Using azure-architecture-expert, explain CAF phases"
```

## Keyword Triggers (Copilot Auto-Routing)

- **azure architecture, landing zone, CAF** → azure-architecture-expert
- **azure iam, entra id, rbac** → azure-iam-expert
- **azure networking, vnet, vpn** → azure-networking-expert
- **book, books, reference, author** → books-expert
- **platform engineering, idp, backstage** → platform-engineering-expert
- **score, score.yaml, workload spec** → score-expert

## Example Queries

**Azure Landing Zones**
```
"Explain Azure landing zone hub-spoke topology"
→ azure-architecture-expert
```

**Platform Engineering from Books**
```
"What do books say about implementing Backstage?"
→ books-expert + platform-engineering-expert
```

**Score for Azure**
```
"Create Score workload for Azure Container Apps"
→ score-expert + azure-architecture-expert
```

**Multi-Domain**
```
"Platform engineering golden path for Azure using Score"
→ platform-engineering-expert + score-expert + azure-architecture-expert
```

## Output Format

All agents return JSON:
```json
{
  "chunk_id": "identifier",
  "relevant": [{
    "point": "finding",
    "evidence": "quote",
    "confidence": "high|medium|low"
  }],
  "missing": ["not found"],
  "suggested_next_queries": ["follow-ups"],
  "answer_if_complete": "answer or null"
}
```

## File Locations

```
.claude/agents/              # Claude CLI (8 agents)
.github/agent_templates/     # Copilot CLI (7 agents)
.claude/rlm_contexts/        # Main contexts (3 files)
.claude/rlm_contexts/books/  # Books (11 files)
.claude/skills/              # Skills (rlm, dagger)
```

## Testing

```bash
# Verify agents
ls .claude/agents/*.md | wc -l  # Should be 8

# Test agent loading
python3 scripts/rlm_copilot_helper.py load-agent azure-architecture-expert

# Check contexts
ls -lh .claude/rlm_contexts/*.txt

# List books
ls .claude/rlm_contexts/books/
```

## Documentation

- **AGENTS.md** - Full registry with routing logic
- **.claude/agents/README.md** - Comprehensive agent docs
- **DOMAIN_EXPERTS_ADDED.md** - Migration details
- **COPILOT_CLI_GUIDE.md** - Copilot CLI guide
- **README.md** - Main documentation

## Tips

1. **Let Copilot route** - Just ask naturally, it detects domains
2. **Use books-expert** - Rich content from 12 technical books
3. **Combine agents** - Multi-domain queries get better answers
4. **Check contexts** - Each agent has specific knowledge bases
5. **Parallel processing** - Copilot CLI runs agents simultaneously

## Maintenance

**Sync from Ruby-IDP:**
```bash
# Copy updated agents
cp Ruby-IDP/.claude/agents/azure-*.md claude_code_RLM/.claude/agents/

# Regenerate Copilot templates
cd claude_code_RLM
for agent in azure-architecture-expert azure-iam-expert azure-networking-expert; do
  sed '1{/^---$/!q;};1,/^---$/d' .claude/agents/${agent}.md > .github/agent_templates/${agent}.txt
done

# Copy updated contexts
cp Ruby-IDP/.claude/rlm_contexts/*.txt claude_code_RLM/.claude/rlm_contexts/
```

## Support

Questions? See:
- AGENTS.md for routing logic
- .claude/agents/README.md for agent details
- DOMAIN_EXPERTS_ADDED.md for full migration info
