#!/usr/bin/env python3
"""RLM MCP Server - Provider-agnostic Recursive Language Model implementation.

This MCP server enables processing documents that exceed typical context window
limits by orchestrating subcalls to various CLI tools (Gemini CLI, OpenCode,
Claude Code, GitHub Copilot CLI, etc.) without requiring API pay-as-you-go billing.

Usage:
    rlm-mcp                    # Run server (stdio transport)
    python -m rlm_mcp.server   # Alternative invocation

MCP Tools:
    - rlm_init: Load a document into state
    - rlm_status: Show current state
    - rlm_peek: Preview document content
    - rlm_grep: Search document content
    - rlm_chunk: Split document into chunks
    - rlm_subcall: Process a chunk with an LLM
    - rlm_subcall_all: Process all chunks
    - rlm_synthesize: Combine results
    - rlm_set_provider: Configure provider
    - rlm_list_providers: Show available providers
"""

from __future__ import annotations

import asyncio
import json
import re
from enum import Enum
from pathlib import Path
from typing import Any, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field, ConfigDict, field_validator

from .state import StateManager, ChunkResult
from .providers import PROVIDERS, BaseProvider, ProviderConfig

# Initialize MCP server
mcp = FastMCP("rlm_mcp")

# Global state manager
_state_manager: StateManager | None = None


def get_state_manager() -> StateManager:
    """Get or create the global state manager."""
    global _state_manager
    if _state_manager is None:
        _state_manager = StateManager()
    return _state_manager


def get_provider(name: str | None = None, model: str | None = None) -> BaseProvider:
    """Get a provider instance by name."""
    sm = get_state_manager()

    if name is None:
        name, model = sm.get_provider()

    if name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {name}. Available: {list(PROVIDERS.keys())}")

    provider_cls = PROVIDERS[name]
    config = provider_cls.default_config()

    if model:
        config.model = model

    return provider_cls(config)


# ============================================================================
# Input Models
# ============================================================================


class InitInput(BaseModel):
    """Input for initializing RLM with a document."""

    model_config = ConfigDict(str_strip_whitespace=True)

    path: str = Field(
        ...,
        description="Path to the document file to load (e.g., '/path/to/document.txt')",
        min_length=1,
    )
    max_bytes: Optional[int] = Field(
        default=None,
        description="Optional maximum bytes to read (default: read entire file)",
        ge=1,
    )


class PeekInput(BaseModel):
    """Input for peeking at document content."""

    start: int = Field(
        default=0,
        description="Start character position (default: 0)",
        ge=0,
    )
    end: int = Field(
        default=2000,
        description="End character position (default: 2000)",
        ge=1,
    )


class GrepInput(BaseModel):
    """Input for searching document content."""

    model_config = ConfigDict(str_strip_whitespace=True)

    pattern: str = Field(
        ...,
        description="Regex pattern to search for (e.g., 'TODO', 'error.*line')",
        min_length=1,
    )
    max_matches: int = Field(
        default=20,
        description="Maximum matches to return",
        ge=1,
        le=100,
    )
    window: int = Field(
        default=120,
        description="Characters of context around each match",
        ge=0,
        le=1000,
    )
    case_insensitive: bool = Field(
        default=False,
        description="Make search case-insensitive",
    )


class ChunkInput(BaseModel):
    """Input for chunking the document."""

    size: int = Field(
        default=200000,
        description="Chunk size in characters (default: 200000 ~50K tokens)",
        ge=1000,
        le=1000000,
    )
    overlap: int = Field(
        default=0,
        description="Character overlap between chunks (default: 0)",
        ge=0,
    )

    @field_validator("overlap")
    @classmethod
    def validate_overlap(cls, v: int, info) -> int:
        # Note: Can't easily access 'size' here, validated at runtime
        return v


class SubcallInput(BaseModel):
    """Input for making a subcall to process a chunk."""

    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(
        ...,
        description="Instruction for the LLM (e.g., 'Summarize the key points')",
        min_length=1,
    )
    chunk_index: int = Field(
        ...,
        description="Which chunk to process (0-indexed)",
        ge=0,
    )
    provider: Optional[str] = Field(
        default=None,
        description="Provider to use (default: use configured provider)",
    )
    model: Optional[str] = Field(
        default=None,
        description="Model override for this call",
    )


class SubcallAllInput(BaseModel):
    """Input for processing all chunks."""

    model_config = ConfigDict(str_strip_whitespace=True)

    prompt: str = Field(
        ...,
        description="Instruction to apply to each chunk",
        min_length=1,
    )
    provider: Optional[str] = Field(
        default=None,
        description="Provider to use (default: use configured provider)",
    )
    model: Optional[str] = Field(
        default=None,
        description="Model override",
    )
    parallel: int = Field(
        default=1,
        description="Number of parallel subcalls (default: 1, sequential)",
        ge=1,
        le=10,
    )


class SetProviderInput(BaseModel):
    """Input for setting the active provider."""

    model_config = ConfigDict(str_strip_whitespace=True)

    provider: str = Field(
        ...,
        description="Provider name: 'gemini', 'opencode', 'claude', or 'copilot'",
    )
    model: Optional[str] = Field(
        default=None,
        description="Model to use (provider-specific)",
    )

    @field_validator("provider")
    @classmethod
    def validate_provider(cls, v: str) -> str:
        if v not in PROVIDERS:
            raise ValueError(f"Unknown provider: {v}. Available: {list(PROVIDERS.keys())}")
        return v


class AddBufferInput(BaseModel):
    """Input for adding text to buffers."""

    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(
        ...,
        description="Text to add to buffers",
    )


# ============================================================================
# MCP Tools
# ============================================================================


@mcp.tool(
    name="rlm_init",
    annotations={
        "title": "Initialize RLM",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def rlm_init(params: InitInput) -> str:
    """Load a document into RLM state for processing.

    This is the first step in an RLM workflow. It loads the document content
    into memory and prepares it for chunking and analysis.

    Args:
        params (InitInput): Contains:
            - path (str): Path to the document file
            - max_bytes (Optional[int]): Maximum bytes to read

    Returns:
        str: JSON with document info including path, char_count, line_count

    Example:
        Load a large SEC filing:
        {"path": "./documents/10k_filing.txt"}
    """
    sm = get_state_manager()

    try:
        ctx = sm.load_document(params.path, params.max_bytes)

        result = {
            "success": True,
            "document": {
                "path": ctx.path,
                "char_count": ctx.char_count,
                "line_count": ctx.line_count,
                "loaded_at": ctx.loaded_at,
            },
            "next_steps": [
                "Use rlm_peek to preview content",
                "Use rlm_chunk to split into processable chunks",
                "Use rlm_set_provider to configure which CLI to use",
            ],
        }
        return json.dumps(result, indent=2)

    except FileNotFoundError as e:
        return json.dumps({"success": False, "error": str(e)})
    except Exception as e:
        return json.dumps({"success": False, "error": f"Failed to load document: {e}"})


@mcp.tool(
    name="rlm_status",
    annotations={
        "title": "RLM Status",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_status() -> str:
    """Show current RLM state including document, chunks, and results.

    Returns:
        str: JSON with complete state information
    """
    sm = get_state_manager()
    state = sm.state

    # Document info
    doc_info = None
    if state.context:
        doc_info = {
            "path": state.context.path,
            "char_count": state.context.char_count,
            "line_count": state.context.line_count,
        }

    # Chunk info
    chunk_info = {
        "count": len(state.chunks),
        "boundaries": state.chunks[:5] if state.chunks else [],  # First 5
        "has_more": len(state.chunks) > 5,
    }

    # Results info
    results_info = {
        "count": len(state.results),
        "successful": sum(1 for r in state.results if r.success),
        "failed": sum(1 for r in state.results if not r.success),
    }

    # Provider info
    provider, model = sm.get_provider()
    provider_cls = PROVIDERS.get(provider)
    provider_info = {
        "active": provider,
        "model": model,
        "available": provider_cls.is_available() if provider_cls else False,
    }

    result = {
        "document": doc_info,
        "chunks": chunk_info,
        "results": results_info,
        "buffers": len(state.buffers),
        "provider": provider_info,
    }

    return json.dumps(result, indent=2)


@mcp.tool(
    name="rlm_peek",
    annotations={
        "title": "Peek at Document",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_peek(params: PeekInput) -> str:
    """Preview a portion of the loaded document.

    Use this to scout the document structure before chunking.

    Args:
        params (PeekInput): Contains:
            - start (int): Start position (default: 0)
            - end (int): End position (default: 2000)

    Returns:
        str: The requested portion of document content
    """
    sm = get_state_manager()
    content = sm.peek(params.start, params.end)

    result = {
        "start": params.start,
        "end": min(params.end, params.start + len(content)),
        "length": len(content),
        "content": content,
    }

    return json.dumps(result, indent=2)


@mcp.tool(
    name="rlm_grep",
    annotations={
        "title": "Search Document",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_grep(params: GrepInput) -> str:
    """Search for a pattern in the loaded document.

    Args:
        params (GrepInput): Contains:
            - pattern (str): Regex pattern to search
            - max_matches (int): Maximum matches (default: 20)
            - window (int): Context characters (default: 120)
            - case_insensitive (bool): Case-insensitive search

    Returns:
        str: JSON with matches including snippets and positions
    """
    sm = get_state_manager()

    flags = re.IGNORECASE if params.case_insensitive else 0

    try:
        matches = sm.grep(
            params.pattern,
            max_matches=params.max_matches,
            window=params.window,
            flags=flags,
        )

        result = {
            "pattern": params.pattern,
            "match_count": len(matches),
            "matches": matches,
        }
        return json.dumps(result, indent=2)

    except re.error as e:
        return json.dumps({"error": f"Invalid regex pattern: {e}"})


@mcp.tool(
    name="rlm_chunk",
    annotations={
        "title": "Chunk Document",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_chunk(params: ChunkInput) -> str:
    """Split the document into chunks for processing.

    Each chunk will be small enough to fit in an LLM's context window.
    Chunks can optionally overlap to preserve context at boundaries.

    Args:
        params (ChunkInput): Contains:
            - size (int): Chunk size in chars (default: 200000)
            - overlap (int): Overlap between chunks (default: 0)

    Returns:
        str: JSON with chunk count and boundaries
    """
    sm = get_state_manager()

    if params.overlap >= params.size:
        return json.dumps({"error": "Overlap must be less than chunk size"})

    try:
        chunks = sm.chunk_indices(params.size, params.overlap)

        result = {
            "success": True,
            "chunk_count": len(chunks),
            "chunk_size": params.size,
            "overlap": params.overlap,
            "chunks": [
                {"index": i, "start": s, "end": e, "length": e - s}
                for i, (s, e) in enumerate(chunks)
            ],
        }
        return json.dumps(result, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool(
    name="rlm_subcall",
    annotations={
        "title": "Process Chunk",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def rlm_subcall(params: SubcallInput) -> str:
    """Process a single chunk with an LLM via CLI.

    This calls out to the configured CLI tool (Gemini, OpenCode, etc.)
    to analyze the chunk content.

    Args:
        params (SubcallInput): Contains:
            - prompt (str): Instruction for the LLM
            - chunk_index (int): Which chunk to process
            - provider (Optional[str]): Provider override
            - model (Optional[str]): Model override

    Returns:
        str: JSON with the LLM's response and metadata
    """
    sm = get_state_manager()

    # Get chunk content
    chunk_content = sm.get_chunk_content(params.chunk_index)
    if chunk_content is None:
        return json.dumps({
            "error": f"Invalid chunk index: {params.chunk_index}. "
                     f"Run rlm_chunk first, or check chunk count with rlm_status."
        })

    # Get provider
    try:
        provider = get_provider(params.provider, params.model)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    # Check availability
    available, msg = await provider.check_auth()
    if not available:
        return json.dumps({"error": f"Provider not available: {msg}"})

    # Execute subcall
    total_chunks = len(sm.state.chunks)
    result = await provider.subcall(
        params.prompt,
        context=chunk_content,
        chunk_index=params.chunk_index,
        total_chunks=total_chunks,
    )

    # Store result
    chunk_start, chunk_end = sm.state.chunks[params.chunk_index]
    chunk_result = ChunkResult(
        chunk_index=params.chunk_index,
        start_pos=chunk_start,
        end_pos=chunk_end,
        provider=result.provider,
        output=result.output,
        success=result.success,
        error=result.error,
        duration_seconds=result.duration_seconds,
    )
    sm.add_result(chunk_result)

    return json.dumps({
        "success": result.success,
        "chunk_index": params.chunk_index,
        "provider": result.provider,
        "model": result.model,
        "duration_seconds": round(result.duration_seconds, 2),
        "output": result.output if result.success else None,
        "error": result.error,
    }, indent=2)


@mcp.tool(
    name="rlm_subcall_all",
    annotations={
        "title": "Process All Chunks",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": True,
    },
)
async def rlm_subcall_all(params: SubcallAllInput) -> str:
    """Process all chunks with an LLM via CLI.

    This iterates through all chunks and calls the LLM for each one.
    Can run in parallel for faster processing.

    Args:
        params (SubcallAllInput): Contains:
            - prompt (str): Instruction for each chunk
            - provider (Optional[str]): Provider override
            - model (Optional[str]): Model override
            - parallel (int): Parallel calls (default: 1)

    Returns:
        str: JSON with summary of all results
    """
    sm = get_state_manager()

    if not sm.state.chunks:
        return json.dumps({
            "error": "No chunks defined. Run rlm_chunk first."
        })

    # Get provider
    try:
        provider = get_provider(params.provider, params.model)
    except ValueError as e:
        return json.dumps({"error": str(e)})

    # Check availability
    available, msg = await provider.check_auth()
    if not available:
        return json.dumps({"error": f"Provider not available: {msg}"})

    total_chunks = len(sm.state.chunks)
    results_summary = {
        "total": total_chunks,
        "successful": 0,
        "failed": 0,
        "total_duration": 0.0,
    }

    # Process chunks
    async def process_chunk(idx: int):
        chunk_content = sm.get_chunk_content(idx)
        result = await provider.subcall(
            params.prompt,
            context=chunk_content,
            chunk_index=idx,
            total_chunks=total_chunks,
        )

        chunk_start, chunk_end = sm.state.chunks[idx]
        chunk_result = ChunkResult(
            chunk_index=idx,
            start_pos=chunk_start,
            end_pos=chunk_end,
            provider=result.provider,
            output=result.output,
            success=result.success,
            error=result.error,
            duration_seconds=result.duration_seconds,
        )
        sm.add_result(chunk_result)
        return result

    if params.parallel > 1:
        # Parallel processing with semaphore
        semaphore = asyncio.Semaphore(params.parallel)

        async def process_with_semaphore(idx: int):
            async with semaphore:
                return await process_chunk(idx)

        tasks = [process_with_semaphore(i) for i in range(total_chunks)]
        results = await asyncio.gather(*tasks)
    else:
        # Sequential processing
        results = []
        for i in range(total_chunks):
            results.append(await process_chunk(i))

    # Summarize
    for r in results:
        if r.success:
            results_summary["successful"] += 1
        else:
            results_summary["failed"] += 1
        results_summary["total_duration"] += r.duration_seconds

    results_summary["total_duration"] = round(results_summary["total_duration"], 2)

    return json.dumps({
        "success": results_summary["failed"] == 0,
        "summary": results_summary,
        "next_step": "Use rlm_synthesize to combine results",
    }, indent=2)


@mcp.tool(
    name="rlm_synthesize",
    annotations={
        "title": "Synthesize Results",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_synthesize() -> str:
    """Combine all chunk results into a single output.

    This gathers all successful chunk results and combines them
    in order for final synthesis.

    Returns:
        str: Combined text from all successful chunk results
    """
    sm = get_state_manager()

    combined = sm.synthesize_results()

    if not combined:
        return json.dumps({
            "error": "No results to synthesize. Run rlm_subcall or rlm_subcall_all first."
        })

    return json.dumps({
        "success": True,
        "result_count": len([r for r in sm.state.results if r.success]),
        "combined_output": combined,
    }, indent=2)


@mcp.tool(
    name="rlm_set_provider",
    annotations={
        "title": "Set Provider",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_set_provider(params: SetProviderInput) -> str:
    """Set the active CLI provider for subcalls.

    Available providers (no API billing - use CLI auth):
    - gemini: Google Gemini CLI (free tier: 60 req/min)
    - opencode: OpenCode (75+ provider configs)
    - claude: Claude Code CLI (uses subscription)
    - copilot: GitHub Copilot CLI (uses subscription)

    Args:
        params (SetProviderInput): Contains:
            - provider (str): Provider name
            - model (Optional[str]): Model override

    Returns:
        str: Confirmation with provider availability status
    """
    sm = get_state_manager()

    # Get provider class
    provider_cls = PROVIDERS[params.provider]

    # Check if available
    is_available = provider_cls.is_available()

    # Set in state
    sm.set_provider(params.provider, params.model)

    # Get auth status
    provider_instance = provider_cls()
    auth_ok, auth_msg = await provider_instance.check_auth()

    return json.dumps({
        "success": True,
        "provider": params.provider,
        "model": params.model,
        "cli_available": is_available,
        "auth_status": auth_msg,
    }, indent=2)


@mcp.tool(
    name="rlm_list_providers",
    annotations={
        "title": "List Providers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_list_providers() -> str:
    """List all available CLI providers and their status.

    Returns availability and authentication status for each provider.
    All providers use CLI tools - no API pay-as-you-go billing.

    Returns:
        str: JSON with all providers and their status
    """
    providers_info = []

    for name, cls in PROVIDERS.items():
        instance = cls()
        is_available = cls.is_available()

        auth_ok, auth_msg = await instance.check_auth()

        config = cls.default_config()

        providers_info.append({
            "name": name,
            "command": config.command,
            "available": is_available,
            "auth_ok": auth_ok,
            "auth_message": auth_msg,
            "default_model": config.model,
        })

    # Get current provider
    sm = get_state_manager()
    current, current_model = sm.get_provider()

    return json.dumps({
        "current_provider": current,
        "current_model": current_model,
        "providers": providers_info,
    }, indent=2)


@mcp.tool(
    name="rlm_add_buffer",
    annotations={
        "title": "Add to Buffer",
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    },
)
async def rlm_add_buffer(params: AddBufferInput) -> str:
    """Add text to the intermediate buffers.

    Buffers are useful for storing intermediate results
    during multi-step analysis.

    Args:
        params (AddBufferInput): Contains:
            - text (str): Text to add

    Returns:
        str: Confirmation with buffer index
    """
    sm = get_state_manager()
    idx = sm.add_buffer(params.text)

    return json.dumps({
        "success": True,
        "buffer_index": idx,
        "total_buffers": len(sm.state.buffers),
    }, indent=2)


@mcp.tool(
    name="rlm_get_buffers",
    annotations={
        "title": "Get Buffers",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_get_buffers() -> str:
    """Get all intermediate buffers.

    Returns:
        str: JSON with all buffer contents
    """
    sm = get_state_manager()
    buffers = sm.get_buffers()

    return json.dumps({
        "count": len(buffers),
        "buffers": buffers,
    }, indent=2)


@mcp.tool(
    name="rlm_reset",
    annotations={
        "title": "Reset State",
        "readOnlyHint": False,
        "destructiveHint": True,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_reset() -> str:
    """Reset all RLM state (document, chunks, results, buffers).

    WARNING: This clears all data. Make sure to export results first
    if you need them.

    Returns:
        str: Confirmation of reset
    """
    sm = get_state_manager()
    sm.reset()

    return json.dumps({
        "success": True,
        "message": "All RLM state has been reset",
    }, indent=2)


@mcp.tool(
    name="rlm_export_results",
    annotations={
        "title": "Export Results",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False,
    },
)
async def rlm_export_results() -> str:
    """Export all chunk processing results as JSON.

    Returns:
        str: JSON array of all results with metadata
    """
    sm = get_state_manager()
    return sm.export_results_json()


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    """Run the RLM MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
