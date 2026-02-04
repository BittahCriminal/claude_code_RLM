# RLM Sub-Agents

Domain-specific agents that process knowledge from imported sources (epub, pdf, txt, video/audio).

## Available Agents

### Cloud & Infrastructure

| Agent | Domain | Description | Knowledge |
|-------|--------|-------------|-----------|
| [azure-architecture](./azure-architecture/agent.md) | Azure Architecture | WAF, CAF, landing zones, solution design | 25 sources |
| [azure-networking](./azure-networking/agent.md) | Azure Networking | VNets, hub-spoke, Private Link, hybrid | 2 sources |
| [azure-security](./azure-security/agent.md) | Azure Security | Identity, Entra ID, Defender, Zero Trust | 5 sources |
| [cloud-architecture](./cloud-architecture/agent.md) | Cloud Architecture | AWS, GCP, OCI, multi-cloud | 6 sources |
| [kubernetes](./kubernetes/agent.md) | Kubernetes | MicroK8s, K3s, standard K8s, AKS | 8 sources |
| [platform-engineering](./platform-engineering/agent.md) | Platform Engineering | IDP, DevEx, self-service automation | 2 sources |
| [argocd](./argocd/agent.md) | Argo CD | GitOps, Kubernetes CD, ApplicationSets | 1 source (web, TTL: 30d) |
| [kratix](./kratix/agent.md) | Kratix | Platform orchestration, Promises, IDP | 1 source (web, TTL: 30d) |
| [dagger](./dagger/agent.md) | Dagger | Programmable CI/CD, containers, SDKs | 1 source (web, TTL: 30d) |
| [radius](./radius/agent.md) | Radius | Cloud-native apps, multi-cloud, Bicep | 1 source (web, TTL: 30d) |

### Security

| Agent | Domain | Description | Knowledge |
|-------|--------|-------------|-----------|
| [security-offensive](./security-offensive/agent.md) | Security Offensive | Pentest, ethical hacking, red team, forensics | 23 sources |
| [cryptography](./cryptography/agent.md) | Cryptography | Encryption, protocols, PKI, secure coding | 2 sources |
| [reverse-engineering](./reverse-engineering/agent.md) | Reverse Engineering | Binary analysis, disassembly, debugging | 5 sources |
| [sbom-analysis](./sbom-analysis/agent.md) | SBOM Analysis | Docker Scout, Trivy, CVE analysis | - |

### Programming Languages

| Agent | Domain | Description | Knowledge |
|-------|--------|-------------|-----------|
| [programming](./programming/agent.md) | Programming | Algorithms, data structures, CS fundamentals | 2 sources |
| [python-engineering](./python-engineering/agent.md) | Python | Python, Django, Flask, FastAPI, pandas | 3 sources |
| [javascript-engineering](./javascript-engineering/agent.md) | JavaScript | JS, TypeScript, Node.js, React, Vue | 3 sources |
| [go-engineering](./go-engineering/agent.md) | Go | Golang, concurrency, cloud-native | 1 source |
| [ruby-engineering](./ruby-engineering/agent.md) | Ruby | Ruby, Rails, gems, RSpec | 2 sources |
| [cpp-engineering](./cpp-engineering/agent.md) | C++ | Modern C++, STL, performance | 1 source |
| [csharp-engineering](./csharp-engineering/agent.md) | C# | .NET, ASP.NET Core, Clean Architecture | 2 sources |

### Data & AI

| Agent | Domain | Description | Knowledge |
|-------|--------|-------------|-----------|
| [data-science](./data-science/agent.md) | Data Science | ML, deep learning, AI, NLP, generative AI | 16 sources |
| [data-engineering](./data-engineering/agent.md) | Data Engineering | ETL/ELT, pipelines, lakehouse, governance | 3 sources |

### Architecture & DevOps

| Agent | Domain | Description | Knowledge |
|-------|--------|-------------|-----------|
| [software-architecture](./software-architecture/agent.md) | Software Architecture | Microservices, event-driven, DDD, system design | 14 sources |
| [linux-administration](./linux-administration/agent.md) | Linux Administration | System admin, bash, DevOps, containers | 5 sources |

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
