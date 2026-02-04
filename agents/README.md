# RLM Sub-Agents

Domain-specific agents that process knowledge from imported sources (epub, pdf, txt, video/audio).

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
| [kubernetes](./kubernetes/agent.md) | Kubernetes | MicroK8s, K3s, standard K8s, AKS |

## Adding Knowledge

1. Place source files in `knowledge/sources/`:
   - `epub/` - E-books
   - `pdf/` - PDF documents
   - `txt/` - Text/markdown files
   - `video/` - Video files (mp4, mkv, webm) - transcribed via Whisper

2. Import using the knowledge importer:
   ```bash
   # Text/document files
   python knowledge/importer.py <file> <agent-domain> [tags] [title]

   # Video files (with transcription)
   python knowledge/importer.py video.mp4 kubernetes "aks,tutorial" "AKS Tutorial" base
   ```

   Examples:
   ```bash
   # EPUB book
   python knowledge/importer.py sources/epub/azure-waf.epub azure-architecture "waf,reliability"

   # PDF document
   python knowledge/importer.py sources/pdf/k8s-patterns.pdf kubernetes "patterns,deployments"

   # Video tutorial (transcribed)
   python knowledge/importer.py sources/video/microk8s-setup.mp4 kubernetes "microk8s,setup" "MicroK8s Setup Guide" small
   ```

3. Imported knowledge appears in `knowledge/processed/<agent>/`

## Agent Schema

See [agent-schema.md](./agent-schema.md) for the full agent definition schema.

## How Agents Work

1. **Query Routing**: Queries are routed to agents based on tag matching
2. **Knowledge Lookup**: Agent retrieves relevant chunks from its knowledge base
3. **Subcall**: Copilot CLI processes the query with knowledge context
4. **Response**: Agent formats response according to its output schema

## Video/Audio Transcription

Video and audio files are automatically transcribed using Whisper:

```bash
# Install transcription support (choose one)
pip install faster-whisper  # Recommended - faster
pip install openai-whisper  # Original OpenAI implementation

# Also requires ffmpeg for video conversion
# Windows: winget install ffmpeg
# macOS: brew install ffmpeg
# Linux: apt install ffmpeg
```

Whisper models (size vs accuracy trade-off):
- `tiny` - Fastest, lowest accuracy
- `base` - Good balance (default)
- `small` - Better accuracy
- `medium` - High accuracy
- `large` - Best accuracy, slowest

## Creating New Agents

1. Create directory: `agents/<domain-name>/`
2. Create `agent.md` with frontmatter (see schema)
3. Add domain to `knowledge/importer.py` AgentDomain enum
4. Import relevant knowledge sources
