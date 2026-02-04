"""Knowledge Base Importer for RLM Agents.

Imports content from epub, pdf, and text files, processes them,
and tags with metadata for agent-specific knowledge bases.

Supported formats:
- EPUB: E-books (requires ebooklib)
- PDF: Documents (requires pypdf or pdfplumber)
- TXT/MD: Plain text and markdown files

Usage:
    from knowledge.importer import KnowledgeImporter

    importer = KnowledgeImporter()
    importer.import_file("book.epub", agent="azure-architecture", tags=["networking", "vnet"])
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any


class SourceFormat(Enum):
    """Supported source file formats."""
    EPUB = "epub"
    PDF = "pdf"
    TXT = "txt"
    MD = "md"


class AgentDomain(Enum):
    """Available agent domains for knowledge mapping."""
    PLATFORM_ENGINEERING = "platform-engineering"
    AZURE_ARCHITECTURE = "azure-architecture"
    AZURE_NETWORKING = "azure-networking"
    AZURE_SECURITY = "azure-security"
    SBOM_ANALYSIS = "sbom-analysis"
    CSHARP_ENGINEERING = "csharp-engineering"
    ARGOCD = "argocd"


@dataclass
class KnowledgeMetadata:
    """Metadata for imported knowledge content."""
    id: str
    source_file: str
    source_format: str
    title: str
    agent_domain: str
    tags: List[str] = field(default_factory=list)
    author: Optional[str] = None
    import_date: str = field(default_factory=lambda: datetime.now().isoformat())
    chunk_count: int = 0
    char_count: int = 0
    checksum: str = ""
    custom_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> "KnowledgeMetadata":
        return cls(**data)


@dataclass
class KnowledgeChunk:
    """A chunk of knowledge content with metadata."""
    id: str
    knowledge_id: str
    index: int
    content: str
    start_pos: int
    end_pos: int
    section: Optional[str] = None
    page: Optional[int] = None


class KnowledgeImporter:
    """Import and process knowledge from various file formats."""

    def __init__(self, base_dir: Path | str | None = None):
        """Initialize the importer.

        Args:
            base_dir: Base directory for knowledge storage.
                      Defaults to ./knowledge relative to this file.
        """
        if base_dir is None:
            base_dir = Path(__file__).parent
        self.base_dir = Path(base_dir)
        self.imports_dir = self.base_dir / "imports"
        self.processed_dir = self.base_dir / "processed"

        # Ensure directories exist
        self.imports_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    def import_file(
        self,
        file_path: Path | str,
        agent: str | AgentDomain,
        title: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author: Optional[str] = None,
        custom_metadata: Optional[Dict[str, Any]] = None,
        chunk_size: int = 200000,
        chunk_overlap: int = 1000,
    ) -> KnowledgeMetadata:
        """Import a file into the knowledge base.

        Args:
            file_path: Path to the source file
            agent: Target agent domain
            title: Optional title (extracted from file if not provided)
            tags: Optional list of tags for categorization
            author: Optional author name
            custom_metadata: Optional additional metadata
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks

        Returns:
            KnowledgeMetadata for the imported content
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        # Determine format
        suffix = file_path.suffix.lower().lstrip(".")
        try:
            source_format = SourceFormat(suffix)
        except ValueError:
            raise ValueError(f"Unsupported file format: {suffix}")

        # Normalize agent domain
        if isinstance(agent, str):
            try:
                agent = AgentDomain(agent)
            except ValueError:
                raise ValueError(f"Unknown agent domain: {agent}")

        # Extract content based on format
        content, extracted_title, extracted_author = self._extract_content(
            file_path, source_format
        )

        # Generate ID
        content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
        knowledge_id = f"{agent.value}_{file_path.stem}_{content_hash}"

        # Create metadata
        metadata = KnowledgeMetadata(
            id=knowledge_id,
            source_file=str(file_path.name),
            source_format=source_format.value,
            title=title or extracted_title or file_path.stem,
            agent_domain=agent.value,
            tags=tags or [],
            author=author or extracted_author,
            char_count=len(content),
            checksum=hashlib.sha256(content.encode()).hexdigest(),
            custom_metadata=custom_metadata or {},
        )

        # Chunk content
        chunks = self._chunk_content(
            content, knowledge_id, chunk_size, chunk_overlap
        )
        metadata.chunk_count = len(chunks)

        # Save processed content
        self._save_knowledge(metadata, content, chunks)

        return metadata

    def _extract_content(
        self, file_path: Path, source_format: SourceFormat
    ) -> tuple[str, Optional[str], Optional[str]]:
        """Extract text content from a file.

        Returns:
            Tuple of (content, title, author)
        """
        if source_format == SourceFormat.EPUB:
            return self._extract_epub(file_path)
        elif source_format == SourceFormat.PDF:
            return self._extract_pdf(file_path)
        elif source_format in (SourceFormat.TXT, SourceFormat.MD):
            return self._extract_text(file_path)
        else:
            raise ValueError(f"Unsupported format: {source_format}")

    def _extract_epub(self, file_path: Path) -> tuple[str, Optional[str], Optional[str]]:
        """Extract content from EPUB file."""
        try:
            import ebooklib
            from ebooklib import epub
            from bs4 import BeautifulSoup
        except ImportError:
            raise ImportError(
                "EPUB support requires: pip install ebooklib beautifulsoup4"
            )

        book = epub.read_epub(str(file_path))

        # Extract metadata
        title = None
        author = None
        for item in book.get_metadata("DC", "title"):
            title = item[0]
            break
        for item in book.get_metadata("DC", "creator"):
            author = item[0]
            break

        # Extract content
        content_parts = []
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), "html.parser")
                text = soup.get_text(separator="\n", strip=True)
                if text:
                    content_parts.append(text)

        return "\n\n".join(content_parts), title, author

    def _extract_pdf(self, file_path: Path) -> tuple[str, Optional[str], Optional[str]]:
        """Extract content from PDF file."""
        try:
            import pypdf
        except ImportError:
            try:
                import pdfplumber
                return self._extract_pdf_pdfplumber(file_path)
            except ImportError:
                raise ImportError(
                    "PDF support requires: pip install pypdf  OR  pip install pdfplumber"
                )

        reader = pypdf.PdfReader(str(file_path))

        # Extract metadata
        title = None
        author = None
        if reader.metadata:
            title = reader.metadata.get("/Title")
            author = reader.metadata.get("/Author")

        # Extract content
        content_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                content_parts.append(text)

        return "\n\n".join(content_parts), title, author

    def _extract_pdf_pdfplumber(self, file_path: Path) -> tuple[str, Optional[str], Optional[str]]:
        """Extract content from PDF using pdfplumber."""
        import pdfplumber

        content_parts = []
        with pdfplumber.open(str(file_path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content_parts.append(text)

        return "\n\n".join(content_parts), None, None

    def _extract_text(self, file_path: Path) -> tuple[str, Optional[str], Optional[str]]:
        """Extract content from text/markdown file."""
        content = file_path.read_text(encoding="utf-8")

        # Try to extract title from first heading
        title = None
        lines = content.split("\n")
        for line in lines[:10]:
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip()
                break
            elif line and not line.startswith("#"):
                title = line[:100]
                break

        return content, title, None

    def _chunk_content(
        self,
        content: str,
        knowledge_id: str,
        chunk_size: int,
        overlap: int,
    ) -> List[KnowledgeChunk]:
        """Split content into chunks."""
        chunks = []
        start = 0
        index = 0

        while start < len(content):
            end = min(start + chunk_size, len(content))

            # Try to break at paragraph/sentence boundary
            if end < len(content):
                # Look for paragraph break
                para_break = content.rfind("\n\n", start + chunk_size // 2, end)
                if para_break > start:
                    end = para_break

            chunk_content = content[start:end]
            chunk_id = f"{knowledge_id}_chunk_{index:04d}"

            chunks.append(KnowledgeChunk(
                id=chunk_id,
                knowledge_id=knowledge_id,
                index=index,
                content=chunk_content,
                start_pos=start,
                end_pos=end,
            ))

            start = end - overlap if overlap < end - start else end
            index += 1

        return chunks

    def _save_knowledge(
        self,
        metadata: KnowledgeMetadata,
        content: str,
        chunks: List[KnowledgeChunk],
    ) -> None:
        """Save processed knowledge to disk."""
        # Create agent-specific directory
        agent_dir = self.processed_dir / metadata.agent_domain
        agent_dir.mkdir(parents=True, exist_ok=True)

        knowledge_dir = agent_dir / metadata.id
        knowledge_dir.mkdir(parents=True, exist_ok=True)

        # Save metadata
        metadata_path = knowledge_dir / "metadata.json"
        metadata_path.write_text(metadata.to_json())

        # Save full content
        content_path = knowledge_dir / "content.txt"
        content_path.write_text(content)

        # Save chunks
        chunks_dir = knowledge_dir / "chunks"
        chunks_dir.mkdir(exist_ok=True)

        for chunk in chunks:
            chunk_path = chunks_dir / f"{chunk.id}.txt"
            chunk_path.write_text(chunk.content)

    def list_knowledge(self, agent: Optional[str | AgentDomain] = None) -> List[KnowledgeMetadata]:
        """List all imported knowledge, optionally filtered by agent."""
        results = []

        if agent:
            if isinstance(agent, AgentDomain):
                agent = agent.value
            search_dirs = [self.processed_dir / agent]
        else:
            search_dirs = [d for d in self.processed_dir.iterdir() if d.is_dir()]

        for agent_dir in search_dirs:
            if not agent_dir.exists():
                continue
            for knowledge_dir in agent_dir.iterdir():
                if not knowledge_dir.is_dir():
                    continue
                metadata_path = knowledge_dir / "metadata.json"
                if metadata_path.exists():
                    data = json.loads(metadata_path.read_text())
                    results.append(KnowledgeMetadata.from_dict(data))

        return results


# Convenience function for CLI usage
def import_knowledge(
    file_path: str,
    agent: str,
    tags: Optional[str] = None,
    title: Optional[str] = None,
) -> None:
    """CLI-friendly import function."""
    importer = KnowledgeImporter()
    tag_list = tags.split(",") if tags else []
    metadata = importer.import_file(
        file_path, agent, title=title, tags=tag_list
    )
    print(f"Imported: {metadata.title}")
    print(f"  ID: {metadata.id}")
    print(f"  Chunks: {metadata.chunk_count}")
    print(f"  Characters: {metadata.char_count}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python importer.py <file_path> <agent> [tags] [title]")
        print("\nAgents:", ", ".join(a.value for a in AgentDomain))
        sys.exit(1)

    import_knowledge(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None,
        sys.argv[4] if len(sys.argv) > 4 else None,
    )
