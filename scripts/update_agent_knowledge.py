#!/usr/bin/env python3
"""Update agent.md files with knowledge_sources from processed knowledge."""

import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
AGENTS_DIR = PROJECT_ROOT / "agents"
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge" / "processed"


def get_knowledge_sources(domain: str) -> list[str]:
    """Get all knowledge source IDs for a domain."""
    domain_dir = KNOWLEDGE_DIR / domain
    if not domain_dir.exists():
        return []

    sources = []
    for knowledge_dir in sorted(domain_dir.iterdir()):
        if not knowledge_dir.is_dir():
            continue
        metadata_path = knowledge_dir / "metadata.json"
        if metadata_path.exists():
            data = json.loads(metadata_path.read_text())
            sources.append(data["id"])
    return sources


def update_agent_file(domain: str, sources: list[str]) -> bool:
    """Update an agent.md file with knowledge_sources."""
    agent_file = AGENTS_DIR / domain / "agent.md"
    if not agent_file.exists():
        print(f"  SKIP: No agent file for {domain}")
        return False

    content = agent_file.read_text()

    # Format the sources as YAML list
    if sources:
        sources_yaml = "\n".join(f"  - {s}" for s in sources)
        new_sources = f"knowledge_sources:\n{sources_yaml}"
    else:
        new_sources = "knowledge_sources: []"

    # Replace existing knowledge_sources line/block
    # Pattern matches knowledge_sources: [] or knowledge_sources:\n  - item\n  - item...
    pattern = r"knowledge_sources:\s*\[\]|knowledge_sources:\n(?:\s+-\s+[^\n]+\n?)+"

    if re.search(pattern, content):
        new_content = re.sub(pattern, new_sources, content)
    else:
        # If no knowledge_sources found, add before the closing ---
        # This shouldn't happen with our schema but handle it
        print(f"  WARNING: No knowledge_sources field found in {domain}")
        return False

    if new_content != content:
        agent_file.write_text(new_content)
        return True
    return False


def main():
    print("Updating agent knowledge sources...")
    print("=" * 60)

    # Get all domains that have knowledge
    domains_with_knowledge = set()
    if KNOWLEDGE_DIR.exists():
        for d in KNOWLEDGE_DIR.iterdir():
            if d.is_dir() and d.name != ".gitkeep":
                domains_with_knowledge.add(d.name)

    # Get all agent domains
    agent_domains = set()
    for d in AGENTS_DIR.iterdir():
        if d.is_dir() and (d / "agent.md").exists():
            agent_domains.add(d.name)

    updated = 0
    for domain in sorted(agent_domains):
        sources = get_knowledge_sources(domain)
        print(f"\n{domain}: {len(sources)} sources")

        if update_agent_file(domain, sources):
            updated += 1
            for s in sources[:3]:
                print(f"  + {s}")
            if len(sources) > 3:
                print(f"  ... and {len(sources) - 3} more")

    print("\n" + "=" * 60)
    print(f"Updated {updated} agent files")


if __name__ == "__main__":
    main()
