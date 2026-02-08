"""Knowledge Base Importer for RLM Agents.

Imports content from epub, pdf, text, and video files, processes them,
and tags with metadata for agent-specific knowledge bases.

Supported formats:
- EPUB: E-books (requires ebooklib)
- PDF: Documents (requires pypdf or pdfplumber)
- TXT/MD: Plain text and markdown files
- MP4/MKV/WEBM: Video files (requires whisper or faster-whisper)

Usage:
    from knowledge.importer import KnowledgeImporter

    importer = KnowledgeImporter()
    importer.import_file("book.epub", agent="azure-architecture", tags=["networking", "vnet"])
    importer.import_file("tutorial.mp4", agent="kubernetes", tags=["aks", "deployment"])
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
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
    MP4 = "mp4"
    MKV = "mkv"
    WEBM = "webm"
    WAV = "wav"
    MP3 = "mp3"
    WEB = "web"  # Web documentation


class AgentDomain(Enum):
    """Available agent domains for knowledge mapping."""
    # Existing domains
    PLATFORM_ENGINEERING = "platform-engineering"
    AZURE_ARCHITECTURE = "azure-architecture"
    AZURE_NETWORKING = "azure-networking"
    AZURE_SECURITY = "azure-security"
    SBOM_ANALYSIS = "sbom-analysis"
    CSHARP_ENGINEERING = "csharp-engineering"
    ARGOCD = "argocd"
    KUBERNETES = "kubernetes"
    # New domains
    SECURITY_OFFENSIVE = "security-offensive"
    PROGRAMMING = "programming"
    PYTHON_ENGINEERING = "python-engineering"
    JAVASCRIPT_ENGINEERING = "javascript-engineering"
    GO_ENGINEERING = "go-engineering"
    RUBY_ENGINEERING = "ruby-engineering"
    CPP_ENGINEERING = "cpp-engineering"
    DATA_SCIENCE = "data-science"
    LINUX_ADMINISTRATION = "linux-administration"
    SOFTWARE_ARCHITECTURE = "software-architecture"
    CLOUD_ARCHITECTURE = "cloud-architecture"
    CRYPTOGRAPHY = "cryptography"
    REVERSE_ENGINEERING = "reverse-engineering"
    DATA_ENGINEERING = "data-engineering"
    # Platform tools
    KRATIX = "kratix"
    DAGGER = "dagger"
    RADIUS = "radius"
    # Internal platforms
    TRAPI = "trapi"
    TRAPI_BATCH = "trapi-batch"
    TRAPI_PYTHON_LIB = "trapi-python-lib"
    MSR_ENGINEERING = "msr-engineering"
    # DevOps
    DEVOPS = "devops"


# Video/audio formats that require transcription
MEDIA_FORMATS = {SourceFormat.MP4, SourceFormat.MKV, SourceFormat.WEBM, SourceFormat.WAV, SourceFormat.MP3}


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
    duration_seconds: Optional[float] = None  # For video/audio
    transcription_model: Optional[str] = None  # For video/audio
    custom_metadata: Dict[str, Any] = field(default_factory=dict)
    # Web documentation fields
    source_url: Optional[str] = None  # Original URL for web docs
    ttl_days: Optional[int] = None  # Time-to-live in days before refresh needed
    expires_at: Optional[str] = None  # ISO timestamp when content expires

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
    timestamp_start: Optional[float] = None  # For video/audio
    timestamp_end: Optional[float] = None    # For video/audio


@dataclass
class TranscriptionResult:
    """Result from video/audio transcription."""
    text: str
    segments: List[Dict[str, Any]]
    duration: float
    model: str
    language: Optional[str] = None


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
        whisper_model: str = "base",
        language: Optional[str] = None,
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
            whisper_model: Whisper model for transcription (tiny, base, small, medium, large)
            language: Language hint for transcription (e.g., "en", "es")

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
        if source_format in MEDIA_FORMATS:
            transcription = self._extract_media(file_path, whisper_model, language)
            content = transcription.text
            extracted_title = None
            extracted_author = None
            duration = transcription.duration
            trans_model = transcription.model
        else:
            content, extracted_title, extracted_author = self._extract_content(
                file_path, source_format
            )
            duration = None
            trans_model = None

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
            duration_seconds=duration,
            transcription_model=trans_model,
            custom_metadata=custom_metadata or {},
        )

        # Chunk content
        if source_format in MEDIA_FORMATS:
            chunks = self._chunk_transcription(
                transcription, knowledge_id, chunk_size, chunk_overlap
            )
        else:
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

    def _extract_media(
        self,
        file_path: Path,
        model: str = "base",
        language: Optional[str] = None,
    ) -> TranscriptionResult:
        """Extract content from video/audio file via transcription.

        Supports multiple transcription backends:
        1. faster-whisper (recommended, faster)
        2. openai-whisper (original)
        3. whisper.cpp via CLI

        Args:
            file_path: Path to media file
            model: Whisper model size (tiny, base, small, medium, large)
            language: Language hint (e.g., "en")

        Returns:
            TranscriptionResult with text, segments, and metadata
        """
        # Try faster-whisper first (recommended)
        try:
            return self._transcribe_faster_whisper(file_path, model, language)
        except ImportError:
            pass

        # Try openai-whisper
        try:
            return self._transcribe_openai_whisper(file_path, model, language)
        except ImportError:
            pass

        # Try whisper.cpp CLI
        try:
            return self._transcribe_whisper_cpp(file_path, model, language)
        except (FileNotFoundError, subprocess.CalledProcessError):
            pass

        raise ImportError(
            "Video/audio transcription requires one of:\n"
            "  pip install faster-whisper  (recommended)\n"
            "  pip install openai-whisper\n"
            "  Or whisper.cpp installed and in PATH"
        )

    def _transcribe_faster_whisper(
        self,
        file_path: Path,
        model: str,
        language: Optional[str],
    ) -> TranscriptionResult:
        """Transcribe using faster-whisper."""
        from faster_whisper import WhisperModel

        # Load model (uses CTranslate2, much faster)
        whisper_model = WhisperModel(model, device="auto", compute_type="auto")

        # Transcribe
        segments_iter, info = whisper_model.transcribe(
            str(file_path),
            language=language,
            beam_size=5,
            vad_filter=True,  # Filter out silence
        )

        # Collect segments
        segments = []
        text_parts = []
        for segment in segments_iter:
            segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
            })
            text_parts.append(segment.text.strip())

        return TranscriptionResult(
            text="\n".join(text_parts),
            segments=segments,
            duration=info.duration,
            model=f"faster-whisper-{model}",
            language=info.language,
        )

    def _transcribe_openai_whisper(
        self,
        file_path: Path,
        model: str,
        language: Optional[str],
    ) -> TranscriptionResult:
        """Transcribe using openai-whisper."""
        import whisper

        # Load model
        whisper_model = whisper.load_model(model)

        # Transcribe
        result = whisper_model.transcribe(
            str(file_path),
            language=language,
        )

        # Extract segments
        segments = []
        for seg in result.get("segments", []):
            segments.append({
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip(),
            })

        # Calculate duration from last segment
        duration = segments[-1]["end"] if segments else 0.0

        return TranscriptionResult(
            text=result["text"],
            segments=segments,
            duration=duration,
            model=f"openai-whisper-{model}",
            language=result.get("language"),
        )

    def _transcribe_whisper_cpp(
        self,
        file_path: Path,
        model: str,
        language: Optional[str],
    ) -> TranscriptionResult:
        """Transcribe using whisper.cpp CLI."""
        # Check for whisper.cpp binary
        whisper_bin = "whisper" if os.name != "nt" else "whisper.exe"

        # Convert to WAV if needed (whisper.cpp prefers WAV)
        if file_path.suffix.lower() not in [".wav"]:
            wav_path = self._convert_to_wav(file_path)
        else:
            wav_path = file_path

        try:
            # Run whisper.cpp
            cmd = [
                whisper_bin,
                "-m", f"ggml-{model}.bin",
                "-f", str(wav_path),
                "-oj",  # Output JSON
            ]
            if language:
                cmd.extend(["-l", language])

            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = json.loads(result.stdout)

            # Parse output
            segments = []
            text_parts = []
            for seg in output.get("transcription", []):
                segments.append({
                    "start": seg["timestamps"]["from"] / 1000,
                    "end": seg["timestamps"]["to"] / 1000,
                    "text": seg["text"].strip(),
                })
                text_parts.append(seg["text"].strip())

            return TranscriptionResult(
                text="\n".join(text_parts),
                segments=segments,
                duration=segments[-1]["end"] if segments else 0.0,
                model=f"whisper-cpp-{model}",
                language=language,
            )
        finally:
            # Clean up temp WAV if we created it
            if wav_path != file_path and wav_path.exists():
                wav_path.unlink()

    def _convert_to_wav(self, file_path: Path) -> Path:
        """Convert media file to WAV using ffmpeg."""
        wav_path = Path(tempfile.mktemp(suffix=".wav"))

        try:
            subprocess.run([
                "ffmpeg", "-i", str(file_path),
                "-ar", "16000",  # 16kHz sample rate
                "-ac", "1",      # Mono
                "-y",            # Overwrite
                str(wav_path)
            ], check=True, capture_output=True)
        except FileNotFoundError:
            raise ImportError("ffmpeg required for video conversion. Install from https://ffmpeg.org")

        return wav_path

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

    def _chunk_transcription(
        self,
        transcription: TranscriptionResult,
        knowledge_id: str,
        chunk_size: int,
        overlap: int,
    ) -> List[KnowledgeChunk]:
        """Split transcription into chunks with timestamp metadata."""
        chunks = []
        current_chunk_text = []
        current_chunk_start = 0.0
        current_char_count = 0
        index = 0

        for segment in transcription.segments:
            segment_text = segment["text"]
            segment_chars = len(segment_text)

            # Check if adding this segment would exceed chunk size
            if current_char_count + segment_chars > chunk_size and current_chunk_text:
                # Save current chunk
                chunk_content = "\n".join(current_chunk_text)
                chunk_id = f"{knowledge_id}_chunk_{index:04d}"

                chunks.append(KnowledgeChunk(
                    id=chunk_id,
                    knowledge_id=knowledge_id,
                    index=index,
                    content=chunk_content,
                    start_pos=0,  # Not applicable for transcriptions
                    end_pos=len(chunk_content),
                    timestamp_start=current_chunk_start,
                    timestamp_end=segment["start"],
                ))

                index += 1
                current_chunk_text = []
                current_chunk_start = segment["start"]
                current_char_count = 0

            current_chunk_text.append(segment_text)
            current_char_count += segment_chars

        # Don't forget the last chunk
        if current_chunk_text:
            chunk_content = "\n".join(current_chunk_text)
            chunk_id = f"{knowledge_id}_chunk_{index:04d}"

            chunks.append(KnowledgeChunk(
                id=chunk_id,
                knowledge_id=knowledge_id,
                index=index,
                content=chunk_content,
                start_pos=0,
                end_pos=len(chunk_content),
                timestamp_start=current_chunk_start,
                timestamp_end=transcription.duration,
            ))

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
        content_path.write_text(content, encoding="utf-8")

        # Save chunks
        chunks_dir = knowledge_dir / "chunks"
        chunks_dir.mkdir(exist_ok=True)

        for chunk in chunks:
            chunk_path = chunks_dir / f"{chunk.id}.txt"
            chunk_path.write_text(chunk.content, encoding="utf-8")

            # Save chunk metadata if it has timestamps
            if chunk.timestamp_start is not None:
                chunk_meta = {
                    "id": chunk.id,
                    "index": chunk.index,
                    "timestamp_start": chunk.timestamp_start,
                    "timestamp_end": chunk.timestamp_end,
                }
                meta_path = chunks_dir / f"{chunk.id}.json"
                meta_path.write_text(json.dumps(chunk_meta, indent=2))

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

    def import_web_docs(
        self,
        url: str,
        content: str,
        agent: str | AgentDomain,
        title: str,
        tags: Optional[List[str]] = None,
        ttl_days: int = 30,
        chunk_size: int = 200000,
        chunk_overlap: int = 1000,
    ) -> KnowledgeMetadata:
        """Import web documentation with TTL tracking.

        Args:
            url: Source URL of the documentation
            content: Pre-fetched content (markdown/text)
            agent: Target agent domain
            title: Title for the documentation
            tags: Optional tags for categorization
            ttl_days: Days until content should be refreshed (default 30)
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks

        Returns:
            KnowledgeMetadata for the imported content
        """
        # Normalize agent domain
        if isinstance(agent, str):
            try:
                agent = AgentDomain(agent)
            except ValueError:
                raise ValueError(f"Unknown agent domain: {agent}")

        # Generate ID from URL
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        knowledge_id = f"{agent.value}_web_{url_hash}"

        # Calculate expiration
        expires_at = (datetime.now() + __import__('datetime').timedelta(days=ttl_days)).isoformat()

        # Create metadata
        metadata = KnowledgeMetadata(
            id=knowledge_id,
            source_file=url,
            source_format=SourceFormat.WEB.value,
            title=title,
            agent_domain=agent.value,
            tags=tags or [],
            char_count=len(content),
            checksum=hashlib.sha256(content.encode()).hexdigest(),
            source_url=url,
            ttl_days=ttl_days,
            expires_at=expires_at,
        )

        # Chunk content
        chunks = self._chunk_content(content, knowledge_id, chunk_size, chunk_overlap)
        metadata.chunk_count = len(chunks)

        # Save processed content
        self._save_knowledge(metadata, content, chunks)

        return metadata

    def get_expired_knowledge(self, agent: Optional[str | AgentDomain] = None) -> List[KnowledgeMetadata]:
        """Get list of knowledge entries that have expired TTL.

        Args:
            agent: Optional agent domain to filter by

        Returns:
            List of expired KnowledgeMetadata entries
        """
        all_knowledge = self.list_knowledge(agent)
        now = datetime.now()
        expired = []

        for k in all_knowledge:
            if k.expires_at:
                try:
                    expires = datetime.fromisoformat(k.expires_at)
                    if now > expires:
                        expired.append(k)
                except ValueError:
                    pass  # Invalid date format, skip

        return expired

    def delete_knowledge(self, knowledge_id: str) -> bool:
        """Delete a knowledge entry by ID.

        Args:
            knowledge_id: The knowledge ID to delete

        Returns:
            True if deleted, False if not found
        """
        # Parse domain from ID (format: domain_name_hash)
        parts = knowledge_id.split("_")
        if len(parts) < 2:
            return False

        # Find the knowledge directory
        for agent_dir in self.processed_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            knowledge_dir = agent_dir / knowledge_id
            if knowledge_dir.exists():
                import shutil
                shutil.rmtree(knowledge_dir)
                return True

        return False


# Convenience function for CLI usage
def import_knowledge(
    file_path: str,
    agent: str,
    tags: Optional[str] = None,
    title: Optional[str] = None,
    whisper_model: str = "base",
) -> None:
    """CLI-friendly import function."""
    importer = KnowledgeImporter()
    tag_list = tags.split(",") if tags else []
    metadata = importer.import_file(
        file_path, agent, title=title, tags=tag_list, whisper_model=whisper_model
    )
    print(f"Imported: {metadata.title}")
    print(f"  ID: {metadata.id}")
    print(f"  Format: {metadata.source_format}")
    print(f"  Chunks: {metadata.chunk_count}")
    print(f"  Characters: {metadata.char_count}")
    if metadata.duration_seconds:
        mins = int(metadata.duration_seconds // 60)
        secs = int(metadata.duration_seconds % 60)
        print(f"  Duration: {mins}m {secs}s")
        print(f"  Transcription model: {metadata.transcription_model}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python importer.py <file_path> <agent> [tags] [title] [whisper_model]")
        print("\nAgents:", ", ".join(a.value for a in AgentDomain))
        print("\nSupported formats:", ", ".join(f.value for f in SourceFormat))
        print("\nWhisper models: tiny, base, small, medium, large")
        sys.exit(1)

    import_knowledge(
        sys.argv[1],
        sys.argv[2],
        sys.argv[3] if len(sys.argv) > 3 else None,
        sys.argv[4] if len(sys.argv) > 4 else None,
        sys.argv[5] if len(sys.argv) > 5 else "base",
    )
