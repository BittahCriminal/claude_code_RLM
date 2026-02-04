"""State management for RLM MCP server.

Provides persistent state storage for:
- Loaded document context
- Chunk processing results
- Intermediate buffers
- Provider configuration

Based on the original rlm_repl.py state management approach.
"""

from __future__ import annotations

import json
import pickle
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


DEFAULT_STATE_DIR = Path(".rlm_mcp_state")


@dataclass
class DocumentContext:
    """Represents a loaded document for RLM processing."""

    path: str
    """Original file path."""

    content: str
    """Full document content."""

    loaded_at: float
    """Unix timestamp when loaded."""

    char_count: int = 0
    """Character count."""

    line_count: int = 0
    """Line count."""

    def __post_init__(self):
        self.char_count = len(self.content)
        self.line_count = self.content.count("\n") + 1


@dataclass
class ChunkResult:
    """Result from processing a single chunk."""

    chunk_index: int
    """Which chunk this is (0-indexed)."""

    start_pos: int
    """Start character position in original document."""

    end_pos: int
    """End character position in original document."""

    provider: str
    """Which provider processed this chunk."""

    output: str
    """The LLM's response for this chunk."""

    success: bool
    """Whether processing succeeded."""

    error: str | None = None
    """Error message if failed."""

    duration_seconds: float = 0.0
    """How long processing took."""

    processed_at: float = field(default_factory=time.time)
    """Unix timestamp when processed."""


@dataclass
class RlmState:
    """Complete state for an RLM session."""

    version: int = 1
    """State format version."""

    context: DocumentContext | None = None
    """Loaded document context."""

    chunks: list[tuple[int, int]] = field(default_factory=list)
    """List of (start, end) chunk boundaries."""

    results: list[ChunkResult] = field(default_factory=list)
    """Results from chunk processing."""

    buffers: list[str] = field(default_factory=list)
    """Intermediate text buffers."""

    provider: str = "gemini"
    """Active provider for subcalls."""

    provider_model: str | None = None
    """Model override for the provider."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional metadata."""


class StateManager:
    """Manages persistent RLM state."""

    def __init__(self, state_dir: Path | str = DEFAULT_STATE_DIR):
        self.state_dir = Path(state_dir)
        self.state_file = self.state_dir / "state.pkl"
        self._state: RlmState | None = None

    def ensure_dir(self) -> None:
        """Create state directory if needed."""
        self.state_dir.mkdir(parents=True, exist_ok=True)

    @property
    def state(self) -> RlmState:
        """Get current state, loading from disk if needed."""
        if self._state is None:
            self._state = self.load()
        return self._state

    def load(self) -> RlmState:
        """Load state from disk, or create new if none exists."""
        if not self.state_file.exists():
            return RlmState()

        try:
            with self.state_file.open("rb") as f:
                data = pickle.load(f)
                if isinstance(data, RlmState):
                    return data
                # Handle legacy dict format
                if isinstance(data, dict):
                    return self._migrate_dict_state(data)
        except Exception as e:
            # Corrupted state, start fresh
            print(f"Warning: Could not load state ({e}), starting fresh")

        return RlmState()

    def save(self) -> None:
        """Save current state to disk."""
        self.ensure_dir()
        tmp_path = self.state_file.with_suffix(".pkl.tmp")
        with tmp_path.open("wb") as f:
            pickle.dump(self.state, f, protocol=pickle.HIGHEST_PROTOCOL)
        tmp_path.replace(self.state_file)

    def reset(self) -> None:
        """Reset to empty state."""
        self._state = RlmState()
        if self.state_file.exists():
            self.state_file.unlink()

    def _migrate_dict_state(self, data: dict) -> RlmState:
        """Migrate from old dict-based state format."""
        state = RlmState()

        # Migrate context
        if "context" in data and isinstance(data["context"], dict):
            ctx = data["context"]
            state.context = DocumentContext(
                path=ctx.get("path", "unknown"),
                content=ctx.get("content", ""),
                loaded_at=ctx.get("loaded_at", time.time()),
            )

        # Migrate buffers
        if "buffers" in data and isinstance(data["buffers"], list):
            state.buffers = data["buffers"]

        return state

    # Document operations

    def load_document(self, path: str | Path, max_bytes: int | None = None) -> DocumentContext:
        """Load a document into state."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Document not found: {path}")

        # Read content
        with path.open("rb") as f:
            data = f.read() if max_bytes is None else f.read(max_bytes)

        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            content = data.decode("utf-8", errors="replace")

        # Create context
        ctx = DocumentContext(
            path=str(path.absolute()),
            content=content,
            loaded_at=time.time(),
        )

        # Update state
        self.state.context = ctx
        self.state.chunks = []
        self.state.results = []
        self.save()

        return ctx

    # Helper operations (from original REPL)

    def peek(self, start: int = 0, end: int = 1000) -> str:
        """Preview a portion of the document content."""
        if not self.state.context:
            return "[No document loaded]"
        content = self.state.context.content
        return content[start:end]

    def grep(
        self,
        pattern: str,
        max_matches: int = 20,
        window: int = 120,
        flags: int = 0,
    ) -> list[dict[str, Any]]:
        """Search for pattern in document content."""
        if not self.state.context:
            return []

        content = self.state.context.content
        results = []

        for m in re.finditer(pattern, content, flags):
            start, end = m.span()
            snippet_start = max(0, start - window)
            snippet_end = min(len(content), end + window)

            results.append({
                "match": m.group(0),
                "span": [start, end],
                "snippet": content[snippet_start:snippet_end],
            })

            if len(results) >= max_matches:
                break

        return results

    def chunk_indices(
        self,
        size: int = 200_000,
        overlap: int = 0,
    ) -> list[tuple[int, int]]:
        """Calculate chunk boundaries for the document."""
        if not self.state.context:
            return []

        if size <= 0:
            raise ValueError("size must be > 0")
        if overlap < 0:
            raise ValueError("overlap must be >= 0")
        if overlap >= size:
            raise ValueError("overlap must be < size")

        content = self.state.context.content
        n = len(content)
        spans = []
        step = size - overlap

        for start in range(0, n, step):
            end = min(n, start + size)
            spans.append((start, end))
            if end >= n:
                break

        # Store in state
        self.state.chunks = spans
        self.save()

        return spans

    def get_chunk_content(self, chunk_index: int) -> str | None:
        """Get the content of a specific chunk."""
        if not self.state.context or not self.state.chunks:
            return None

        if chunk_index < 0 or chunk_index >= len(self.state.chunks):
            return None

        start, end = self.state.chunks[chunk_index]
        return self.state.context.content[start:end]

    # Buffer operations

    def add_buffer(self, text: str) -> int:
        """Add text to buffers, return buffer index."""
        self.state.buffers.append(str(text))
        self.save()
        return len(self.state.buffers) - 1

    def get_buffers(self) -> list[str]:
        """Get all buffers."""
        return list(self.state.buffers)

    def clear_buffers(self) -> None:
        """Clear all buffers."""
        self.state.buffers = []
        self.save()

    # Result operations

    def add_result(self, result: ChunkResult) -> None:
        """Add a chunk processing result."""
        self.state.results.append(result)
        self.save()

    def get_results(self) -> list[ChunkResult]:
        """Get all chunk results."""
        return list(self.state.results)

    def clear_results(self) -> None:
        """Clear all results."""
        self.state.results = []
        self.save()

    # Provider operations

    def set_provider(self, provider: str, model: str | None = None) -> None:
        """Set the active provider for subcalls."""
        self.state.provider = provider
        self.state.provider_model = model
        self.save()

    def get_provider(self) -> tuple[str, str | None]:
        """Get the active provider and model."""
        return self.state.provider, self.state.provider_model

    # Export operations

    def export_results_json(self) -> str:
        """Export all results as JSON."""
        results_data = []
        for r in self.state.results:
            results_data.append({
                "chunk_index": r.chunk_index,
                "start_pos": r.start_pos,
                "end_pos": r.end_pos,
                "provider": r.provider,
                "output": r.output,
                "success": r.success,
                "error": r.error,
                "duration_seconds": r.duration_seconds,
                "processed_at": r.processed_at,
            })
        return json.dumps(results_data, indent=2)

    def export_buffers_text(self) -> str:
        """Export all buffers as text."""
        return "\n\n---\n\n".join(self.state.buffers)

    def synthesize_results(self) -> str:
        """Combine all successful results into one text."""
        successful = [r for r in self.state.results if r.success]
        successful.sort(key=lambda r: r.chunk_index)

        parts = []
        for r in successful:
            parts.append(f"=== Chunk {r.chunk_index + 1} ===")
            parts.append(r.output)
            parts.append("")

        return "\n".join(parts)
