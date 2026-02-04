# Knowledge Base

Import and manage knowledge from epub, pdf, and text files for RLM sub-agents.

## Directory Structure

```
knowledge/
├── importer.py         # Knowledge import module
├── sources/            # Place source files here
│   ├── epub/           # E-books (.epub)
│   ├── pdf/            # Documents (.pdf)
│   └── txt/            # Text files (.txt, .md)
├── imports/            # Staging area (optional)
└── processed/          # Processed knowledge (auto-generated)
    └── <agent-domain>/
        └── <knowledge-id>/
            ├── metadata.json
            ├── content.txt
            └── chunks/
                ├── chunk_0000.txt
                ├── chunk_0001.txt
                └── ...
```

## Quick Start

### 1. Install Dependencies

```bash
# For EPUB support
pip install ebooklib beautifulsoup4

# For PDF support (choose one)
pip install pypdf
# OR
pip install pdfplumber
```

### 2. Import Knowledge

```python
from knowledge.importer import KnowledgeImporter

importer = KnowledgeImporter()

# Import an EPUB
metadata = importer.import_file(
    "sources/epub/platform-engineering-book.epub",
    agent="platform-engineering",
    tags=["idp", "devex"],
    title="Platform Engineering Guide"
)

# Import a PDF
metadata = importer.import_file(
    "sources/pdf/azure-networking.pdf",
    agent="azure-networking",
    tags=["vnet", "private-link"]
)

# Import text/markdown
metadata = importer.import_file(
    "sources/txt/argocd-patterns.md",
    agent="argocd",
    tags=["gitops", "applicationset"]
)
```

### 3. CLI Usage

```bash
python knowledge/importer.py <file> <agent> [tags] [title]

# Examples
python knowledge/importer.py sources/epub/book.epub azure-architecture "waf,caf" "Azure Guide"
python knowledge/importer.py sources/pdf/trivy-docs.pdf sbom-analysis "trivy,cve"
```

## Supported Formats

| Format | Extensions | Library Required |
|--------|------------|------------------|
| EPUB | `.epub` | `ebooklib`, `beautifulsoup4` |
| PDF | `.pdf` | `pypdf` or `pdfplumber` |
| Text | `.txt`, `.md` | None |

## Agent Domains

| Domain ID | Description |
|-----------|-------------|
| `platform-engineering` | Platform engineering, IDP, DevEx |
| `azure-architecture` | Azure solutions architecture |
| `azure-networking` | Azure networking services |
| `azure-security` | Azure security and identity |
| `sbom-analysis` | SBOM, Docker Scout, Trivy |
| `csharp-engineering` | C# and .NET development |
| `argocd` | Argo CD and GitOps |

## Metadata Schema

Each imported knowledge entry has metadata:

```json
{
  "id": "azure-architecture_azure-waf_a1b2c3d4",
  "source_file": "azure-waf.epub",
  "source_format": "epub",
  "title": "Azure Well-Architected Framework",
  "agent_domain": "azure-architecture",
  "tags": ["waf", "reliability", "security"],
  "author": "Microsoft",
  "import_date": "2026-02-03T10:30:00",
  "chunk_count": 15,
  "char_count": 250000,
  "checksum": "sha256...",
  "custom_metadata": {}
}
```

## Chunking

Documents are automatically chunked for processing:

- **Default chunk size**: 200,000 characters (~50K tokens)
- **Default overlap**: 1,000 characters
- **Smart boundaries**: Chunks break at paragraph boundaries when possible

Customize chunking:
```python
metadata = importer.import_file(
    "large-doc.pdf",
    agent="azure-architecture",
    chunk_size=100000,    # Smaller chunks
    chunk_overlap=2000    # More overlap
)
```

## Listing Knowledge

```python
from knowledge.importer import KnowledgeImporter

importer = KnowledgeImporter()

# List all knowledge
all_knowledge = importer.list_knowledge()

# List knowledge for specific agent
azure_knowledge = importer.list_knowledge(agent="azure-architecture")

for k in azure_knowledge:
    print(f"{k.title}: {k.chunk_count} chunks")
```
