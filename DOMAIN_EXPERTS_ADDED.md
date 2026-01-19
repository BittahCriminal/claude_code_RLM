# Domain Experts Added from Ruby-IDP

## Summary

Successfully copied 7 domain-specific expert agents and their knowledge bases from the Ruby-IDP repository to enable rich domain expertise in the RLM system.

## What Was Copied

### 1. Agent Definitions (Claude CLI Format)

Copied to `.claude/agents/`:
- ✅ `azure-architecture-expert.md` - Azure CAF, Well-Architected, landing zones
- ✅ `azure-iam-expert.md` - Entra ID, RBAC, Managed Identities
- ✅ `azure-networking-expert.md` - VNets, VPN Gateway, ExpressRoute
- ✅ `books-expert.md` - Technical books analyzer
- ✅ `platform-engineering-expert.md` - IDP, Backstage, golden paths
- ✅ `score-expert.md` - Score workload specifications

### 2. Agent Templates (Copilot CLI Format)

Generated in `.github/agent_templates/`:
- ✅ `azure-architecture-expert.txt`
- ✅ `azure-iam-expert.txt`
- ✅ `azure-networking-expert.txt`
- ✅ `books-expert.txt`
- ✅ `platform-engineering-expert.txt`
- ✅ `score-expert.txt`

(YAML frontmatter stripped, identical instructions otherwise)

### 3. Knowledge Base / Contexts

Copied to `.claude/rlm_contexts/`:
- ✅ `azure_radius_full.txt` (19KB) - Azure Radius, Landing Zones, CAF
- ✅ `platform_engineering_full.txt` (1.6MB) - IDP patterns, Backstage
- ✅ `score_full.txt` (11KB) - Score specification

Copied to `.claude/rlm_contexts/books/` (12 books, ~9MB):
- ✅ `azure-cloud-projects-*.txt` (541KB)
- ✅ `azure-data-and-ai-architect-*.txt` (537KB)
- ✅ `azure-devops-explained-*.txt` (73KB)
- ✅ `azure-for-developers-*.txt` (1.1MB)
- ✅ `c-13-and-net-9-*.txt` (1.5MB)
- ✅ `certified-kubernetes-administrator-*.txt` (256KB)
- ✅ `implementing-gitops-with-kubernetes-*.txt` (886KB)
- ✅ `kubernetes-for-generative-ai-*.txt` (694KB)
- ✅ `mastering-enterprise-platform-engineering-*.txt` (776KB)
- ✅ `platform-engineering-for-architects-*.txt` (854KB)
- ✅ `the-kubernetes-bible-*.txt` (1.4MB)

### 4. Skills

Copied to `.claude/skills/`:
- ✅ `dagger/SKILL.md` - Dagger CI/CD skill (from Ruby-IDP)

### 5. Documentation

Created/Updated:
- ✅ `AGENTS.md` - Updated with 7 agents + routing logic
- ✅ `.claude/agents/README.md` - Comprehensive agent documentation
- ✅ `DOMAIN_EXPERTS_ADDED.md` - This file

## Total Content Size

```
Agents (definitions):       ~20KB (6 files)
Agent templates:            ~18KB (6 files)
Contexts (main):           ~1.7MB (3 files)
Books contexts:            ~9.0MB (12 files)
Skills:                    ~5KB (1 file)
Documentation:             ~15KB (2 files)
─────────────────────────────────────
TOTAL:                     ~10.7MB
```

## Agent Capabilities

### Azure Experts (3 agents)

**azure-architecture-expert**
- Cloud Adoption Framework (all phases)
- Well-Architected Framework (5 pillars)
- Landing zones (enterprise-scale, start-small)
- Management groups hierarchy
- Compute: VMs, VMSS, AKS, Container Apps, Functions
- Storage: Blob, Files, Data Lake
- Databases: Azure SQL, Cosmos DB, PostgreSQL

**azure-iam-expert**
- Entra ID (Azure AD)
- RBAC roles and custom roles
- Managed Identities (system/user-assigned)
- Service Principals and App Registrations
- Conditional Access policies
- Privileged Identity Management (PIM)
- Azure AD B2B/B2C

**azure-networking-expert**
- Virtual Networks (VNets) and subnets
- VPN Gateway (site-to-site, point-to-site)
- ExpressRoute (private connectivity)
- Azure Firewall and NSGs
- Load Balancer and Application Gateway
- Traffic Manager and Front Door
- Private Link and Service Endpoints

### Specialized Experts (3 agents)

**books-expert**
- Analyzes 12 technical books
- Topics: Azure, Kubernetes, Platform Engineering, GitOps, DevOps
- Extracts: Best practices, patterns, code examples
- Provides: Book citations, chapter references, author attribution

**platform-engineering-expert**
- Internal Developer Platforms (IDP)
- Backstage platform
- Golden paths and paved roads
- Self-service infrastructure
- Developer portals
- Platform-as-a-Product mindset
- Team Topologies application

**score-expert**
- Score specification format (score.yaml)
- score-compose (Docker Compose output)
- score-k8s (Kubernetes manifests output)
- Workload portability
- Resource dependencies
- Service connections

## Usage Examples

### Example 1: Azure Landing Zone Question (Claude CLI)
```bash
claude

"Use azure-architecture-expert to explain Azure landing zone hub-spoke topology"

# Or with RLM for large context
/rlm context=.claude/rlm_contexts/azure_radius_full.txt query="Explain landing zones"
```

### Example 2: Platform Engineering from Books (Copilot CLI)
```bash
copilot

"What do technical books say about implementing Backstage for IDPs?"
# → Auto-routes to books-expert + platform-engineering-expert
# → Searches relevant books in parallel
# → Synthesizes findings with citations
```

### Example 3: Score Workload for Azure (Both CLIs)
```bash
# Copilot CLI (natural language)
"Create a Score workload specification for deploying to Azure Container Apps"
# → Routes to score-expert + azure-architecture-expert

# Claude CLI (explicit)
"Use score-expert and azure-architecture-expert to create a Score spec for ACA"
```

### Example 4: Multi-Domain Query
```bash
"How do I implement a platform engineering golden path for Azure using Score?"
# → Invokes 3 agents in parallel:
#    - platform-engineering-expert (golden path patterns)
#    - score-expert (Score specifications)
#    - azure-architecture-expert (Azure services)
# → Synthesizes comprehensive answer
```

## Routing Logic

### Keyword Detection

Copilot CLI analyzes user queries for these keywords:

**Azure architecture triggers:**
- azure architecture, landing zone, CAF, well-architected, azure compute
- azure storage, cosmos db, aks, management groups

**Azure IAM triggers:**
- azure iam, entra id, azure ad, rbac, managed identity
- service principal, conditional access, pim

**Azure networking triggers:**
- azure networking, vnet, vpn gateway, expressroute
- azure firewall, application gateway, private link

**Books triggers:**
- book, books, technical literature, reference, author, chapter
- best practices from books, what do books say

**Platform engineering triggers:**
- platform engineering, idp, internal developer platform, backstage
- golden path, developer experience, self-service

**Score triggers:**
- score, score.yaml, workload specification, score-compose, score-k8s

### Multi-Agent Invocation

When multiple domains are detected, agents are invoked **in parallel**:

```javascript
// Query: "Azure landing zone with platform engineering best practices"
// Detected: azure + platform engineering

task(agent="azure-architecture-expert", context=azure_radius_full.txt, ...)
task(agent="platform-engineering-expert", context=platform_engineering_full.txt, ...)

// Both run simultaneously
// Results synthesized after both complete
```

## Integration with Existing RLM

### Unchanged Components
- ✅ `.claude/skills/rlm/scripts/rlm_repl.py` - Same REPL script
- ✅ `rlm-subcall` agent - Still available for generic chunks
- ✅ RLM skill (`/rlm`) - Works with all agents
- ✅ Chunking logic - Same algorithm

### Enhanced Components
- ✅ AGENTS.md - Now has 7 agents vs 1
- ✅ Auto-routing - Detects domain and selects appropriate agent(s)
- ✅ Context loading - Loads domain-specific knowledge bases
- ✅ Parallel processing - Multi-agent queries run simultaneously

## Testing

### Quick Tests

**Test agent availability:**
```bash
# Claude CLI
ls .claude/agents/*.md | wc -l  # Should show 7

# Copilot CLI
ls .github/agent_templates/*.txt | wc -l  # Should show 7
```

**Test context files:**
```bash
ls -lh .claude/rlm_contexts/*.txt  # Should show 3 files
ls -lh .claude/rlm_contexts/books/*.txt | wc -l  # Should show 12
```

**Test agent loading:**
```bash
python3 scripts/rlm_copilot_helper.py load-agent azure-architecture-expert
# Should print full agent prompt
```

### Full Workflow Tests

**Test 1: Single Azure Agent (Claude CLI)**
```bash
claude
"Use azure-architecture-expert to explain Azure management groups"
```

**Test 2: Books Search (Copilot CLI)**
```bash
copilot
"Search technical books for Kubernetes best practices"
```

**Test 3: Multi-Agent Synthesis (Either CLI)**
```bash
"Combine Azure architecture patterns with platform engineering golden paths"
```

## Maintenance

### Keep Agents Synced

When updating agent instructions in Ruby-IDP:
1. Copy updated `.md` from Ruby-IDP to claude_code_RLM
2. Regenerate `.txt` template:
   ```bash
   cd claude_code_RLM
   sed '1{/^---$/!q;};1,/^---$/d' .claude/agents/<agent>.md > .github/agent_templates/<agent>.txt
   ```
3. Test with both CLIs

### Update Contexts

When Ruby-IDP knowledge bases are updated:
```bash
cd claude_code_RLM
cp /path/to/Ruby-IDP/.claude/rlm_contexts/azure_radius_full.txt .claude/rlm_contexts/
cp /path/to/Ruby-IDP/.claude/rlm_contexts/platform_engineering_full.txt .claude/rlm_contexts/
# etc.
```

### Add New Books

```bash
# Copy new book from Ruby-IDP
cp /path/to/Ruby-IDP/.claude/rlm_contexts/books/new-book_full.txt .claude/rlm_contexts/books/

# Update .claude/agents/README.md with book info
```

## Benefits

### For Claude CLI Users
- ✅ Domain experts auto-discovered
- ✅ `/rlm` skill works with all agents
- ✅ Rich, structured responses with domain knowledge

### For Copilot CLI Users
- ✅ Automatic routing to correct expert(s)
- ✅ Parallel multi-agent processing
- ✅ Natural language queries

### For Both
- ✅ Consistent agent behavior
- ✅ Same knowledge base
- ✅ Rich domain expertise (Azure, Platform Eng, Score, Books)
- ✅ ~10MB of curated technical content
- ✅ JSON-structured outputs for downstream processing

## Next Steps

1. **Test thoroughly** - Try example queries with both CLIs
2. **Add more agents** - Consider AWS/GCP experts if needed
3. **Expand contexts** - Add more books or documentation
4. **Create examples** - Document common use cases
5. **Integrate with CI/CD** - Use dagger skill for build pipelines

## See Also

- `AGENTS.md` - Full agent registry
- `.claude/agents/README.md` - Agent documentation
- `COPILOT_CLI_GUIDE.md` - Copilot CLI guide
- `README.md` - Main documentation
- `MIGRATION_SUMMARY.md` - Copilot CLI migration details
