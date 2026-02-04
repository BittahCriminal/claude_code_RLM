# RLM Sub-Agents

Domain-specific agents that process knowledge from imported sources (epub, pdf, txt).

## Available Agents

| Agent | Domain | Description |
|-------|--------|-------------|
| [platform-engineering](./platform-engineering/agent.md) | Platform Engineering | IDP, DevEx, self-service automation |
| [azure-architecture](./azure-architecture/agent.md) | Azure Architecture | WAF, CAF, landing zones, solution design |
| [azure-networking](./azure-networking/agent.md) | Azure Networking | VNets, hub-spoke, Private Link, hybrid connectivity |
| [azure-security](./azure-security/agent.md) | Azure Security | Identity, Entra ID, Defender, Sentinel, Zero Trust |
| [sbom-analysis](./sbom-analysis/agent.md) | SBOM Analysis | Docker Scout, Trivy, CVE analysis, supply chain |
| [csharp-engineering](./csharp-engineering/agent.md) | C# Engineering | .NET, ASP.NET Core, Clean Architecture, DDD |
| [argocd](./argocd/agent.md) | Argo CD | GitOps, Kubernetes CD, ApplicationSets |

## Adding Knowledge

1. Place source files in `knowledge/sources/`:
   - `epub/` - E-books
   - `pdf/` - PDF documents
   - `txt/` - Text/markdown files

2. Import using the knowledge importer:
   ```bash
   python knowledge/importer.py <file> <agent-domain> [tags] [title]
   ```

   Example:
   ```bash
   python knowledge/importer.py sources/epub/azure-waf.epub azure-architecture "waf,reliability" "Azure Well-Architected Framework"
   ```

3. Imported knowledge appears in `knowledge/processed/<agent>/`

## Agent Schema

See [agent-schema.md](./agent-schema.md) for the full agent definition schema.

## How Agents Work

1. **Query Routing**: Queries are routed to agents based on tag matching
2. **Knowledge Lookup**: Agent retrieves relevant chunks from its knowledge base
3. **Subcall**: Copilot CLI processes the query with knowledge context
4. **Response**: Agent formats response according to its output schema

## Creating New Agents

1. Create directory: `agents/<domain-name>/`
2. Create `agent.md` with frontmatter (see schema)
3. Add domain to `knowledge/importer.py` AgentDomain enum
4. Import relevant knowledge sources
