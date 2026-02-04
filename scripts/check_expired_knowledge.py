#!/usr/bin/env python3
"""Check for expired knowledge entries that need refreshing.

Usage:
    python scripts/check_expired_knowledge.py [agent]

Example:
    python scripts/check_expired_knowledge.py          # Check all agents
    python scripts/check_expired_knowledge.py argocd   # Check specific agent
"""

import sys
from datetime import datetime
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from knowledge.importer import KnowledgeImporter


def main():
    agent = sys.argv[1] if len(sys.argv) > 1 else None

    importer = KnowledgeImporter()

    print("Checking for expired knowledge...")
    print("=" * 60)

    expired = importer.get_expired_knowledge(agent)

    if not expired:
        print("No expired knowledge entries found.")
        return

    print(f"Found {len(expired)} expired entries:\n")

    for k in expired:
        days_expired = (datetime.now() - datetime.fromisoformat(k.expires_at)).days
        print(f"  [{k.agent_domain}] {k.title}")
        print(f"    ID: {k.id}")
        print(f"    Source: {k.source_url or k.source_file}")
        print(f"    Expired: {days_expired} days ago")
        print(f"    TTL: {k.ttl_days} days")
        print()

    print("\nTo refresh web documentation, run:")
    print("  python scripts/import_web_docs.py <url> <agent> <title> [ttl_days] [tags]")
    print("\nTo delete expired entries, use:")
    print("  from knowledge.importer import KnowledgeImporter")
    print("  importer = KnowledgeImporter()")
    print("  importer.delete_knowledge('<knowledge_id>')")


if __name__ == "__main__":
    main()
