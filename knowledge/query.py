#!/usr/bin/env python3
"""Knowledge base query utilities for RLM workflows.

This module provides functions to search and retrieve knowledge chunks
from the processed knowledge base, enabling RLM agents to use imported
documentation and books.

Usage:
    # List available agents and their knowledge
    python knowledge/query.py list

    # List knowledge for specific agent
    python knowledge/query.py list kratix

    # Get all chunks for a knowledge entry
    python knowledge/query.py chunks <knowledge_id>

    # Search across an agent's knowledge
    python knowledge/query.py search <agent> <query>

    # Combine all agent knowledge into single context file
    python knowledge/query.py combine <agent> <output_path>
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge.importer import KnowledgeImporter, KnowledgeMetadata


class KnowledgeQuery:
    """Query and search the knowledge base."""

    def __init__(self, base_dir: Optional[Path] = None):
        self.importer = KnowledgeImporter(base_dir)
        self.processed_dir = self.importer.processed_dir

    def list_agents(self) -> list[str]:
        """List all agents with knowledge."""
        agents = []
        for d in self.processed_dir.iterdir():
            if d.is_dir() and d.name != ".gitkeep":
                agents.append(d.name)
        return sorted(agents)

    def list_knowledge(self, agent: Optional[str] = None) -> list[KnowledgeMetadata]:
        """List all knowledge entries, optionally filtered by agent."""
        return self.importer.list_knowledge(agent)

    def get_chunks_dir(self, knowledge_id: str) -> Optional[Path]:
        """Get the chunks directory for a knowledge entry."""
        # Search all agent dirs for this knowledge ID
        for agent_dir in self.processed_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            knowledge_dir = agent_dir / knowledge_id
            if knowledge_dir.exists():
                return knowledge_dir / "chunks"
        return None

    def get_chunk_paths(self, knowledge_id: str) -> list[Path]:
        """Get all chunk file paths for a knowledge entry."""
        chunks_dir = self.get_chunks_dir(knowledge_id)
        if not chunks_dir or not chunks_dir.exists():
            return []
        return sorted(chunks_dir.glob("*.txt"))

    def get_chunk_content(self, chunk_path: Path) -> str:
        """Read content from a chunk file."""
        return chunk_path.read_text(encoding="utf-8")

    def get_all_chunks_for_agent(self, agent: str) -> list[tuple[str, Path]]:
        """Get all chunk paths for an agent's knowledge base.

        Returns:
            List of (knowledge_id, chunk_path) tuples
        """
        chunks = []
        for k in self.list_knowledge(agent):
            for chunk_path in self.get_chunk_paths(k.id):
                chunks.append((k.id, chunk_path))
        return chunks

    def search_chunks(
        self,
        agent: str,
        query: str,
        max_results: int = 10,
        context_chars: int = 500,
    ) -> list[dict]:
        """Search for query terms across an agent's knowledge chunks.

        Args:
            agent: Agent domain to search
            query: Search query (supports simple word matching)
            max_results: Maximum results to return
            context_chars: Characters of context around matches

        Returns:
            List of match dicts with chunk_path, knowledge_id, matches, snippet
        """
        results = []
        # Simple word-based search
        words = query.lower().split()
        pattern = "|".join(re.escape(w) for w in words)

        for knowledge_id, chunk_path in self.get_all_chunks_for_agent(agent):
            content = self.get_chunk_content(chunk_path)
            content_lower = content.lower()

            # Count matches
            matches = len(re.findall(pattern, content_lower))
            if matches == 0:
                continue

            # Find best snippet
            first_match = re.search(pattern, content_lower)
            if first_match:
                start = max(0, first_match.start() - context_chars // 2)
                end = min(len(content), first_match.end() + context_chars // 2)
                snippet = content[start:end]
            else:
                snippet = content[:context_chars]

            results.append({
                "knowledge_id": knowledge_id,
                "chunk_path": str(chunk_path),
                "matches": matches,
                "snippet": snippet,
            })

        # Sort by match count descending
        results.sort(key=lambda x: x["matches"], reverse=True)
        return results[:max_results]

    def combine_agent_knowledge(self, agent: str, output_path: Path) -> int:
        """Combine all knowledge for an agent into a single file.

        Args:
            agent: Agent domain
            output_path: Path to write combined content

        Returns:
            Total character count
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        parts = []
        for k in self.list_knowledge(agent):
            # Read full content
            content_path = self.processed_dir / agent / k.id / "content.txt"
            if content_path.exists():
                parts.append(f"\n\n{'='*60}\n")
                parts.append(f"# {k.title}\n")
                parts.append(f"Source: {k.source_url or k.source_file}\n")
                parts.append(f"{'='*60}\n\n")
                parts.append(content_path.read_text(encoding="utf-8"))

        combined = "".join(parts)
        output_path.write_text(combined, encoding="utf-8")
        return len(combined)

    def get_agent_summary(self, agent: str) -> dict:
        """Get summary statistics for an agent's knowledge base."""
        knowledge = self.list_knowledge(agent)
        total_chars = 0
        total_chunks = 0
        sources = []

        for k in knowledge:
            total_chars += k.char_count
            total_chunks += k.chunk_count
            sources.append({
                "id": k.id,
                "title": k.title,
                "format": k.source_format,
                "chunks": k.chunk_count,
                "chars": k.char_count,
                "url": k.source_url,
                "expires": k.expires_at,
            })

        return {
            "agent": agent,
            "total_sources": len(knowledge),
            "total_chunks": total_chunks,
            "total_chars": total_chars,
            "sources": sources,
        }


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    query = KnowledgeQuery()

    if cmd == "list":
        agent = sys.argv[2] if len(sys.argv) > 2 else None
        if agent:
            summary = query.get_agent_summary(agent)
            print(f"\nAgent: {summary['agent']}")
            print(f"Sources: {summary['total_sources']}")
            print(f"Chunks: {summary['total_chunks']}")
            print(f"Characters: {summary['total_chars']:,}")
            print("\nKnowledge entries:")
            for s in summary["sources"]:
                exp = f" (expires: {s['expires'][:10]})" if s["expires"] else ""
                print(f"  [{s['format']}] {s['title']}: {s['chunks']} chunks{exp}")
                print(f"       ID: {s['id']}")
        else:
            agents = query.list_agents()
            print(f"\nAvailable agents with knowledge: {len(agents)}")
            for a in agents:
                k = query.list_knowledge(a)
                total_chunks = sum(x.chunk_count for x in k)
                print(f"  {a}: {len(k)} sources, {total_chunks} chunks")

    elif cmd == "chunks":
        if len(sys.argv) < 3:
            print("Usage: python query.py chunks <knowledge_id>")
            sys.exit(1)
        knowledge_id = sys.argv[2]
        paths = query.get_chunk_paths(knowledge_id)
        print(f"\nChunks for {knowledge_id}: {len(paths)}")
        for p in paths:
            size = p.stat().st_size
            print(f"  {p.name}: {size:,} bytes")

    elif cmd == "search":
        if len(sys.argv) < 4:
            print("Usage: python query.py search <agent> <query>")
            sys.exit(1)
        agent = sys.argv[2]
        search_query = " ".join(sys.argv[3:])
        results = query.search_chunks(agent, search_query)
        print(f"\nSearch results for '{search_query}' in {agent}: {len(results)} matches")
        for r in results:
            print(f"\n  [{r['matches']} matches] {r['knowledge_id']}")
            print(f"  Path: {r['chunk_path']}")
            print(f"  Snippet: {r['snippet'][:200]}...")

    elif cmd == "combine":
        if len(sys.argv) < 4:
            print("Usage: python query.py combine <agent> <output_path>")
            sys.exit(1)
        agent = sys.argv[2]
        output_path = Path(sys.argv[3])
        chars = query.combine_agent_knowledge(agent, output_path)
        print(f"Combined {agent} knowledge to {output_path} ({chars:,} chars)")

    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
