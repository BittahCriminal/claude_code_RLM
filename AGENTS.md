# RLM Agents for GitHub Copilot CLI

This file enables GitHub Copilot CLI to use the RLM (Recursive Language Model) pattern with custom agent routing.

## Available Agents

### 1. rlm-subcall (Generic)

**Purpose**: Acts as the RLM sub-LLM (llm_query). Analyzes chunks of large context files and extracts relevant information.

**Model**: Claude Haiku 4.5 (fast, cost-effective for chunk processing)

**When to use**:
- Processing large context files that exceed normal context windows
- User provides a very large document (docs, logs, transcripts, scraped webpages)
- Need to analyze multiple chunks of a document in parallel

**Trigger keywords**: RLM, recursive language model, large context, chunk analysis, long document

---

### 2. azure-architecture-expert

**Purpose**: Analyzes Azure architecture, Cloud Adoption Framework, Well-Architected Framework, landing zones, and compute/storage/database patterns.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/azure_radius_full.txt` (19KB)

**Expertise**:
- Cloud Adoption Framework (CAF) - all phases
- Well-Architected Framework pillars
- Landing zones (enterprise-scale, start-small)
- Management groups and policy design
- Compute: VMs, VMSS, AKS, Container Apps, Functions
- Storage: Blob, Files, Data Lake
- Databases: Azure SQL, Cosmos DB, PostgreSQL

**Trigger keywords**: azure architecture, landing zone, CAF, well-architected, azure compute, azure storage, cosmos db, aks

---

### 3. azure-iam-expert

**Purpose**: Analyzes Azure identity, access management, Entra ID, RBAC, Managed Identities, and authentication patterns.

**Model**: Claude Haiku 4.5

**Expertise**:
- Entra ID (formerly Azure AD)
- RBAC roles and assignments
- Managed Identities (system/user-assigned)
- Service Principals and App Registrations
- Conditional Access policies
- Privileged Identity Management (PIM)
- Azure AD B2B/B2C

**Trigger keywords**: azure iam, entra id, azure ad, rbac, managed identity, service principal, conditional access

---

### 4. azure-networking-expert

**Purpose**: Analyzes Azure networking including VNets, VPN Gateway, ExpressRoute, Traffic Manager, Application Gateway, and hybrid connectivity.

**Model**: Claude Haiku 4.5

**Expertise**:
- Virtual Networks (VNets) and subnets
- VPN Gateway (site-to-site, point-to-site)
- ExpressRoute (private connectivity)
- Azure Firewall and Network Security Groups
- Load Balancer and Application Gateway
- Traffic Manager and Front Door
- Private Link and Service Endpoints

**Trigger keywords**: azure networking, vnet, vpn gateway, expressroute, azure firewall, application gateway, private link

---

### 5. azure-security-expert

**Purpose**: Analyzes Azure security best practices across Defender for Cloud, Sentinel, identity, network, data, and governance controls.

**Model**: Claude Haiku 4.5

**Context**:
- `/Users/bittahcriminal/workspace/Platform-Engineering-RLM/Docs/Azure-Sentinel.pdf`
- Azure MCP server (`mcr.microsoft.com/azure-sdk/azure-mcp`, container: `magical_zhukovsky`) for latest guidance

**Expertise**:
- Defender for Cloud (Secure Score, recommendations, compliance)
- Microsoft Sentinel (SIEM/SOAR, connectors, analytics rules)
- Entra ID security (MFA, Conditional Access, PIM)
- Network security (NSG, Azure Firewall, WAF, DDoS)
- Data protection (Key Vault, encryption, secrets)
- DevSecOps (secure CI/CD, supply chain controls)

**Trigger keywords**: azure security, defender for cloud, sentinel, security posture, zero trust, SOC, SIEM, SOAR

---

### 6. books-expert

**Purpose**: Analyzes content from ingested technical books covering cloud platforms, networking, DevOps, Kubernetes, and platform engineering.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/books/` directory (12 books, ~9MB)

**Books Available**:
- Azure Cloud Projects
- Azure Data and AI Architect Handbook
- Azure DevOps Explained
- Azure for Developers
- Implementing GitOps with Kubernetes
- Kubernetes for Generative AI Solutions
- The Kubernetes Bible
- Mastering Enterprise Platform Engineering
- Platform Engineering for Architects
- Certified Kubernetes Administrator Study Companion

**Trigger keywords**: book, books, technical literature, reference, author, chapter, best practices from books

---

### 7. platform-engineering-expert

**Purpose**: Analyzes Internal Developer Platforms (IDP), golden paths, Backstage, developer experience, and platform engineering principles.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/platform_engineering_full.txt` (1.6MB)

**Expertise**:
- Internal Developer Platforms (IDP)
- Golden paths and paved roads
- Backstage platform
- Self-service infrastructure
- Developer portals
- Platform-as-a-Product mindset
- Team Topologies and Conway's Law

**Trigger keywords**: platform engineering, idp, internal developer platform, backstage, golden path, developer experience, self-service

---

### 8. score-expert

**Purpose**: Analyzes Score workload specifications, score-compose, score-k8s, and platform-agnostic workload definitions.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/score_full.txt` (11KB)

**Expertise**:
- Score specification format
- score.yaml structure
- score-compose (Docker Compose output)
- score-k8s (Kubernetes manifests output)
- Workload portability across platforms
- Resource dependencies
- Service connections

**Trigger keywords**: score, score.yaml, workload specification, score-compose, score-k8s, score spec

---

### 9. azure-devops-expert

**Purpose**: Analyzes Azure DevOps practices across Pipelines, Repos, Boards, Artifacts, and Test Plans.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/books/azure-devops-explained-unknown-author-db1ecf5b_full.txt`

**Expertise**:
- Azure Pipelines (YAML, classic, agents, environments)
- Azure Repos (Git workflows, branching, code review)
- Azure Boards (work items, sprints, backlogs)
- Azure Artifacts (feeds, packages, retention)
- Azure Test Plans (manual, automated testing)
- Service connections, permissions, governance

**Trigger keywords**: azure devops, azure pipelines, azure repos, azure boards, azure artifacts, azure test plans

---

### 10. csharp-engineering-expert

**Purpose**: Extracts C# and .NET engineering guidance, language features, and performance practices.

**Model**: Claude Haiku 4.5

**Context**: `.claude/rlm_contexts/books/c-13-and-net-9-modern-cross-platform-development-f-aa3a7aab_full.txt`

**Expertise**:
- C# language features (C# 13)
- .NET 9 runtime and libraries
- async/await, LINQ, collections, generics
- ASP.NET Core patterns and APIs
- Performance, diagnostics, testing

**Trigger keywords**: c#, dotnet, .net, asp.net, roslyn, nuget

---

### 11. golang-engineering-expert

**Purpose**: Extracts Go software engineering guidance from provided content.

**Model**: Claude Haiku 4.5

**Context**: none (use user-provided content or MCP server backups)

**Expertise**:
- Go language basics, concurrency, and standard library usage
- API design, testing, and performance
- Tooling (go mod, go test, go fmt)

**Trigger keywords**: go, golang, goroutine, gopher, go modules

---

### 12. ruby-engineering-expert

**Purpose**: Extracts Ruby software engineering guidance from provided content.

**Model**: Claude Haiku 4.5

**Context**: none (use user-provided content or MCP server backups)

**Expertise**:
- Ruby language features and idioms
- Rails architecture, testing, and performance
- Gems, Bundler, and tooling

**Trigger keywords**: ruby, rails, rake, bundler, active record

---

### 13. typescript-engineering-expert

**Purpose**: Extracts TypeScript software engineering guidance from provided content.

**Model**: Claude Haiku 4.5

**Context**: none (use user-provided content or MCP server backups)

**Expertise**:
- TypeScript types, generics, and inference
- Node.js and frontend tooling
- Testing, linting, and build pipelines

**Trigger keywords**: typescript, ts, tsconfig, node, tsc

---

### 14. security-scanning-expert

**Purpose**: Analyzes container security scanning practices and uses Trivy results for vulnerability reporting.

**Model**: Claude Haiku 4.5

**Context**: none (use user-provided content or MCP server backups)

**Expertise**:
- Trivy image scanning for pulled Docker images
- CVE severity triage and remediation guidance
- SBOM generation and vulnerability reporting
- Integrating security scans into CI pipelines

**Trigger keywords**: trivy, container scan, vulnerability scan, sbom, cve, image security

---

## How GitHub Copilot CLI Should Use This Agent

### For Claude CLI Users
```bash
# Skill invocation (auto-discovery)
/rlm context=path/to/file.txt query="What are the main points?"
```

### For GitHub Copilot CLI Users

When the user requests RLM processing:

1. **Initialize REPL** with context file:
   ```bash
   python3 .claude/skills/rlm/scripts/rlm_repl.py init <context_path>
   ```

2. **Create chunks** as separate files:
   ```bash
   python3 .claude/skills/rlm/scripts/rlm_repl.py exec <<'PY'
   paths = write_chunks('.claude/rlm_state/chunks', size=200000, overlap=0)
   print('\n'.join(paths))
   PY
   ```

3. **Invoke rlm-subcall agent** for EACH chunk using the `task` tool:
   ```javascript
   task({
     agent_type: "task",
     model: "claude-haiku-4.5",
     description: "Analyzing chunk 1/N",
     prompt: `
   [Read from .github/agent_templates/rlm-subcall.txt]
   
   Chunk file path: ${chunk_path}
   User query: ${user_query}
   
   Instructions:
   1. Read the chunk file
   2. Extract information relevant to the query
   3. Return JSON with the required schema
     `
   })
   ```

4. **Process chunks in parallel** when possible (launch multiple task calls simultaneously)

5. **Synthesize results** from all chunk analyses in the main conversation

---

## Agent Template Location

The full agent prompt is stored in:
- **Claude CLI**: `.claude/agents/rlm-subcall.md` (auto-discovered)
- **Copilot CLI**: `.github/agent_templates/rlm-subcall.txt` (manually loaded)

Both contain identical instructions for consistency across CLI tools.

---

## Output Format (Required)

The rlm-subcall agent MUST return JSON with this exact schema:

```json
{
  "chunk_id": "identifier or 'inline'",
  "relevant": [
    {
      "point": "key finding",
      "evidence": "short quote or paraphrase (<30 words)",
      "confidence": "high|medium|low"
    }
  ],
  "missing": ["what could not be determined from this chunk"],
  "suggested_next_queries": ["optional sub-questions for other chunks"],
  "answer_if_complete": "If this chunk alone answers the query, put answer here, otherwise null"
}
```

---

## Example: RLM Workflow in Copilot CLI

```
User: "Process large_document.txt and find all mentions of security vulnerabilities"

Copilot CLI (you):
Step 1: Initialize REPL
  $ python3 .claude/skills/rlm/scripts/rlm_repl.py init large_document.txt
  
Step 2: Create chunks
  $ python3 .claude/skills/rlm/scripts/rlm_repl.py exec -c "paths = write_chunks('.claude/rlm_state/chunks', size=200000); print('\\n'.join(paths))"
  Output: 
    .claude/rlm_state/chunks/chunk_0000.txt
    .claude/rlm_state/chunks/chunk_0001.txt
    ...
    .claude/rlm_state/chunks/chunk_0009.txt

Step 3: Load agent template
  Read .github/agent_templates/rlm-subcall.txt

Step 4: Invoke agent for each chunk (in parallel)
  task(agent_type="task", model="claude-haiku-4.5", 
       prompt="[agent template] + Chunk: .claude/rlm_state/chunks/chunk_0000.txt + Query: 'Find security vulnerabilities'")
  task(agent_type="task", model="claude-haiku-4.5", 
       prompt="[agent template] + Chunk: .claude/rlm_state/chunks/chunk_0001.txt + Query: 'Find security vulnerabilities'")
  ... (repeat for all 10 chunks in parallel)

Step 5: Collect JSON responses from all tasks

Step 6: Synthesize final answer:
  "Found 3 security vulnerabilities across the document:
   1. SQL Injection risk in auth.py (chunk 2, high confidence)
   2. Hardcoded API key in config.json (chunk 5, high confidence)
   3. Unvalidated user input in api.py (chunk 7, medium confidence)"
```

---

## Routing Logic

**Automatic triggers** (when Copilot CLI should use RLM):
- User says: "process large file", "analyze long document", "use RLM pattern"
- File size > 500KB and user asks questions about its contents
- User explicitly references multiple chunks or pagination

**Manual trigger**:
- User says: "Use the rlm-subcall agent to analyze..."

---

## Notes

- **Parallel processing**: Always invoke multiple task calls simultaneously when analyzing multiple chunks
- **Model selection**: Use `claude-haiku-4.5` for cost-effective chunk processing
- **Context isolation**: Each chunk is analyzed independently with no cross-chunk awareness
- **Synthesis happens in main conversation**: The root LLM (you) combines results
- **State persistence**: REPL maintains state across invocations via pickle file
- **Sequential orchestration**: For workflows that depend on intermediate outputs (e.g., build/pull an image → Trivy scan → threat model), run steps in order and pass artifacts between agents.

---

## Sequential Orchestration Rules

When a workflow involves Docker images, the orchestrator must execute the following in order:
1. Build or pull the Docker image.
2. Run `trivy image <image>` and record vulnerabilities.
3. Generate an SBOM (via Trivy or the configured tooling).
4. Produce a threat model assessment (TMA) for the system where the image is used.

Use the `security-scanning-expert` for scan interpretation and threat model assessment. If additional system context is required, gather it first and then proceed with the ordered steps.

---

## MCP Server Backups

MCP servers available in Docker Desktop (currently created, not running):
- `mcp/grafana` (container: `youthful_newton`)
- `stickerdaniel/linkedin-mcp-server:1.4.0` (container: `confident_heisenberg`)
- `mcr.microsoft.com/azure-sdk/azure-mcp` (container: `magical_zhukovsky`)
- `mcp/notion` (container: `intelligent_shaw`)
- `ghcr.io/github/github-mcp-server` (container: `youthful_bhabha`)
- `mcp/git` (container: `festive_satoshi`)
- `mcp/jetbrains` (container: `funny_grothendieck`)

When a knowledge base chunk is insufficient, the root agent should:
1. Start the relevant MCP container with `docker start <container_name>`.
2. Query the MCP server using the configured MCP client.
3. Provide results to sub-agents as inline content for extraction.

For `azure-security-expert`, always pull latest security guidance from the Azure MCP server and pass it inline alongside the Sentinel PDF chunks.

---

## Next Steps

- Add dedicated Go/Ruby/TypeScript context files under `.claude/rlm_contexts/` for richer extraction.
- Extend `scripts/rlm_copilot_helper.py` if you want it to auto-recognize the new agents.

---

## Auto-Routing Logic for Copilot CLI

When the user asks a question, analyze keywords to determine which agent(s) to invoke:

### Single-Domain Queries
- **Azure architecture** → `azure-architecture-expert`
- **Azure IAM/identity** → `azure-iam-expert`
- **Azure networking** → `azure-networking-expert`
- **Azure security** → `azure-security-expert`
- **Azure DevOps** → `azure-devops-expert`
- **Books/references** → `books-expert`
- **Platform engineering** → `platform-engineering-expert`
- **Score workloads** → `score-expert`
- **C#** → `csharp-engineering-expert`
- **Golang** → `golang-engineering-expert`
- **Ruby** → `ruby-engineering-expert`
- **TypeScript** → `typescript-engineering-expert`
- **Security scanning** → `security-scanning-expert`
- **Generic large file** → `rlm-subcall`

### Multi-Domain Queries (invoke multiple agents in parallel)
- "Azure architecture with Radius" → `azure-architecture-expert` + load azure_radius_full.txt context
- "Platform engineering best practices from books" → `platform-engineering-expert` + `books-expert`
- "Score workload for Azure" → `score-expert` + `azure-architecture-expert`
- "Kubernetes platform engineering" → `platform-engineering-expert` + `books-expert` (filter K8s books)
- "Azure DevOps from books" → `azure-devops-expert` + `books-expert`
- "Docker image security" → `security-scanning-expert` + `platform-engineering-expert`

### Context Loading Strategy

For each agent, load the appropriate context:

```javascript
// Azure architecture queries
context_path = ".claude/rlm_contexts/azure_radius_full.txt"

// Azure security queries
context_paths = [
  "/Users/bittahcriminal/workspace/Platform-Engineering-RLM/Docs/Azure-Sentinel.pdf"
]
// Pull latest guidance via Azure MCP server (container: magical_zhukovsky)

// Azure DevOps queries
context_path = ".claude/rlm_contexts/books/azure-devops-explained-unknown-author-db1ecf5b_full.txt"

// Platform engineering queries  
context_path = ".claude/rlm_contexts/platform_engineering_full.txt"

// Score workload queries
context_path = ".claude/rlm_contexts/score_full.txt"

// C# queries
context_path = ".claude/rlm_contexts/books/c-13-and-net-9-modern-cross-platform-development-f-aa3a7aab_full.txt"

// Books queries - load specific books or all
context_paths = [
  ".claude/rlm_contexts/books/azure-*.txt",  // For Azure questions
  ".claude/rlm_contexts/books/*platform*.txt",  // For platform eng
  ".claude/rlm_contexts/books/*kubernetes*.txt",  // For K8s
  ".claude/rlm_contexts/books/*gitops*.txt"  // For GitOps/CI/CD
]
```

## Example Workflows

### Example 1: Azure Landing Zone Question
```
User: "What are the best practices for Azure landing zones?"

Copilot CLI:
1. Detect keywords: "azure", "landing zones"
2. Route to: azure-architecture-expert
3. Load context: .claude/rlm_contexts/azure_radius_full.txt
4. Invoke: task(agent_type="task", model="haiku", 
              prompt="[azure-architecture-expert template] + context + query")
5. Return structured findings with CAF phases and recommendations
```

### Example 2: Platform Engineering with Books
```
User: "What do books say about implementing Internal Developer Platforms?"

Copilot CLI:
1. Detect keywords: "books", "internal developer platforms"
2. Route to: books-expert + platform-engineering-expert
3. Load contexts:
   - .claude/rlm_contexts/books/*platform*.txt
   - .claude/rlm_contexts/platform_engineering_full.txt
4. Invoke both agents in parallel:
   - task(...books-expert + platform books...)
   - task(...platform-engineering-expert + context...)
5. Synthesize findings from both with book citations
```

### Example 3: Score Workload for Azure
```
User: "How do I create a Score workload that deploys to Azure AKS?"

Copilot CLI:
1. Detect keywords: "score workload", "azure aks"
2. Route to: score-expert + azure-architecture-expert
3. Load contexts:
   - .claude/rlm_contexts/score_full.txt
   - .claude/rlm_contexts/azure_radius_full.txt
4. Invoke both agents in parallel
5. Combine Score spec guidance with Azure AKS patterns
```

### Example 4: Docker Image Threat Model
```
User: "Scan our Docker image and provide a threat model"

Copilot CLI:
1. Build or pull the Docker image using the appropriate pipeline or tooling
2. Run `trivy image <image>` to collect vulnerabilities
3. Route results to: security-scanning-expert
4. Produce a threat model assessment based on scan findings
```

## Agent Template Location

All agent prompts are in `.github/agent_templates/`:
- `rlm-subcall.txt`
- `azure-architecture-expert.txt`
- `azure-iam-expert.txt`
- `azure-networking-expert.txt`
- `azure-security-expert.txt`
- `azure-devops-expert.txt`
- `csharp-engineering-expert.txt`
- `golang-engineering-expert.txt`
- `ruby-engineering-expert.txt`
- `typescript-engineering-expert.txt`
- `security-scanning-expert.txt`
- `books-expert.txt`
- `platform-engineering-expert.txt`
- `score-expert.txt`

Load with:
```bash
python3 scripts/rlm_copilot_helper.py load-agent <agent-name>
```
