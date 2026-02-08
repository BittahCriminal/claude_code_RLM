# Project instructions

This repository serves as a **launch pad** for RLM-assisted automation across the TRAPI ecosystem and Cordillera infrastructure projects.

---

## Related Repositories (Local Paths)

| Repository | Local Path | Purpose |
|------------|------------|---------|
| **cordillera** | `C:\Users\v-leorichard\workspace\cordillera` | GCR cluster configuration, tooling, and utilities for Bonete B200 and future clusters. Management-plane resources for Kubernetes/Volcano configs. |
| **TRAPI.wiki** | `C:\Users\v-leorichard\workspace\TRAPI.wiki` | TRAPI documentation wiki - getting started, deployment info, how-to guides, troubleshooting. |
| **trapi-python-lib** | `C:\Users\v-leorichard\workspace\trapi-python-lib` | Python SDK for TRAPI - includes `trapi-cli`, OpenAI helper injection, request/error caching. |
| **trapi-batch** | `C:\Users\v-leorichard\workspace\trapi-batch` | .NET-based batch processing system - Azure Functions, Service Bus, AOAI-compatible batch API. |
| **trapi-snapshot** | `C:\Users\v-leorichard\workspace\trapi-snapshot` | TRAPI main platform - React UI, Bicep IaC, API Management, CosmosDB, self-service portal. |

---

## TRAPI Ecosystem Overview

**TRAPI** (TnR API Manager / Translation Research API Platform Interface) is an enterprise platform providing secure, managed access to Azure OpenAI and AI services for Microsoft Research.

### Key Components:
- **API Gateway**: Azure API Management fronting Azure OpenAI services
- **Self-Service Portal**: React-based web UI (`trapi-ui/`) for API discovery and management
- **Batch Processing**: Upload-based batch inference for large workloads (AOAI-compatible API)
- **Identity Management**: Azure AD integration with managed service identity support
- **Python SDK**: `trapi-cli` and injectable OpenAI helpers

### Technology Stack:
- **Frontend**: React 18, TypeScript, Vite, Fluent UI, MSAL
- **Backend**: .NET 8 (Batch API), Python (SDK/CLI), Azure Functions
- **Infrastructure**: Azure APIM, Front Door, CosmosDB, Key Vault, Service Bus, Static Web Apps
- **IaC**: Bicep templates throughout

---

## Cordillera Overview

**Cordillera** provides configuration, tooling, and utilities for GCR-operated training clusters (Bonete B200 and future).

### Repository Contents:
- Cluster configuration (Kubernetes manifests, Volcano configs)
- Operational tooling for cluster users/operators
- Documentation for cluster usage and administration
- Utilities for job submission and operational workflows
- `es-metadata.yml` files for code ownership metadata

**Note**: Cordillera hosts management-plane resources; research code belongs in separate repos.

---

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

**Relevant agents for TRAPI/Cordillera work:**
- **azure-architecture** - Azure certs, WAF, architecture patterns
- **kubernetes** - K8s, AKS, K3s (relevant for Cordillera)
- **software-architecture** - Microservices, design patterns
- **dagger** - CI/CD pipelines, SDKs
- **argocd** - GitOps, Argo Workflows

Run `python3 knowledge/query.py list` for all agents.

---

## RLM Mode for Long-Context Tasks

This repository includes a minimal "Recursive Language Model" (RLM) setup for GitHub Copilot:
- Skill: `rlm` in `.github/skills/rlm/`
- Skill: `kb-query` in `.github/skills/kb-query/` (knowledge base queries)
- Subagent (sub-LLM): `rlm-subcall` in `.github/agents/`
- Persistent Python REPL: `.github/skills/rlm/scripts/rlm_repl.py`
- Knowledge query: `knowledge/query.py`

### When to Use RLM:
1. Analyzing large codebases across TRAPI repos
2. Processing comprehensive documentation (e.g., `TRAPI-COMPREHENSIVE-DOCUMENTATION.md`)
3. Cross-repo analysis or migration tasks
4. Large-scale refactoring or code generation

### RLM Procedure:
1) Ask for (or locate) a context file path
2) Run the `/rlm` Skill and follow its procedure
3) Use the REPL and subagent for chunk-level work
4) Synthesize results in the main conversation

---

## Common Automation Tasks

### TRAPI Python Library
```bash
cd C:\Users\v-leorichard\workspace\trapi-python-lib
python init.py  # Setup venv and install
trapi-cli help  # View available commands
trapi-cli quickstart show  # Test basic access
```

### TRAPI Batch System
```bash
cd C:\Users\v-leorichard\workspace\trapi-batch
dotnet build TrapiBatchProcessor.sln
dotnet test
```

### TRAPI Snapshot (Main Platform)
```bash
cd C:\Users\v-leorichard\workspace\trapi-snapshot
# Frontend
cd trapi-ui && npm install && npm run dev
# Infrastructure
az deployment group create --template-file main.bicep
```

---

## Azure DevOps Integration

When creating/updating ADO work items for TRAPI projects:
- **Project**: TRAPI (Azure DevOps)
- Always populate `System.Description` and `Microsoft.VSTS.Common.AcceptanceCriteria`
- Use Gherkin format for acceptance criteria when applicable
- Reference the ADO MCP tools for work item management

---

## File Navigation Tips

| What | Where |
|------|-------|
| TRAPI API docs | `TRAPI.wiki/Reference/` |
| Batch API schema | `trapi-batch/schema/` |
| Bicep modules | `trapi-snapshot/modules/`, `trapi-batch/infra/` |
| React UI code | `trapi-snapshot/trapi-ui/src/` |
| Python SDK source | `trapi-python-lib/src/trapi/` |
| Cordillera automation | `cordillera/automation/` |
| Cordillera utilities | `cordillera/utilities/` |
