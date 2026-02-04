#!/usr/bin/env python3
"""Import web documentation into knowledge base with TTL tracking.

Usage:
    python scripts/import_web_docs.py <base_url> <agent> <title> [ttl_days] [tags]

Example:
    python scripts/import_web_docs.py https://argo-workflows.readthedocs.io/en/latest/ argocd "Argo Workflows Documentation" 30 "argo,workflows,kubernetes"
"""

import hashlib
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Required: pip install requests beautifulsoup4")
    sys.exit(1)

from knowledge.importer import KnowledgeImporter


def fetch_page(url: str, session: requests.Session) -> Optional[str]:
    """Fetch a single page and return its HTML content."""
    try:
        resp = session.get(url, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def html_to_markdown(html: str, base_url: str) -> str:
    """Convert HTML to clean markdown-like text."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script, style, nav elements
    for tag in soup.find_all(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Find main content area (common patterns)
    main_content = (
        soup.find("main") or
        soup.find("article") or
        soup.find("div", class_=re.compile(r"(content|main|document|rst-content)")) or
        soup.find("div", role="main") or
        soup.body
    )

    if not main_content:
        return ""

    # Extract text with structure
    lines = []

    for element in main_content.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "p", "pre", "code", "li", "table"]):
        if element.name.startswith("h"):
            level = int(element.name[1])
            prefix = "#" * level
            lines.append(f"\n{prefix} {element.get_text(strip=True)}\n")
        elif element.name == "p":
            text = element.get_text(strip=True)
            if text:
                lines.append(text + "\n")
        elif element.name in ("pre", "code"):
            code = element.get_text()
            if code.strip():
                lines.append(f"\n```\n{code}\n```\n")
        elif element.name == "li":
            text = element.get_text(strip=True)
            if text:
                lines.append(f"- {text}")
        elif element.name == "table":
            # Simple table extraction
            lines.append("\n[Table content]\n")
            for row in element.find_all("tr"):
                cells = [cell.get_text(strip=True) for cell in row.find_all(["th", "td"])]
                lines.append("| " + " | ".join(cells) + " |")
            lines.append("")

    return "\n".join(lines)


def discover_pages(base_url: str, session: requests.Session, max_pages: int = 200) -> list[str]:
    """Discover all documentation pages from the base URL."""
    visited = set()
    to_visit = [base_url]
    pages = []

    parsed_base = urlparse(base_url)
    base_domain = parsed_base.netloc
    base_path = parsed_base.path.rstrip("/")

    print(f"Discovering pages from {base_url}...")

    while to_visit and len(pages) < max_pages:
        url = to_visit.pop(0)

        # Normalize URL
        url = url.split("#")[0]  # Remove anchors
        if url in visited:
            continue

        visited.add(url)

        # Only process pages under base path
        parsed = urlparse(url)
        if parsed.netloc != base_domain:
            continue
        if not parsed.path.startswith(base_path):
            continue

        # Skip non-HTML resources
        if any(url.endswith(ext) for ext in [".png", ".jpg", ".gif", ".css", ".js", ".pdf", ".zip"]):
            continue

        html = fetch_page(url, session)
        if not html:
            continue

        pages.append(url)
        print(f"  Found: {url} ({len(pages)}/{max_pages})")

        # Find links to other pages
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.find_all("a", href=True):
            href = link["href"]
            full_url = urljoin(url, href)
            if full_url not in visited:
                to_visit.append(full_url)

        # Be nice to the server
        time.sleep(0.2)

    return pages


def fetch_all_docs(base_url: str, max_pages: int = 200) -> tuple[str, list[str]]:
    """Fetch all documentation pages and combine into single document.

    Returns:
        Tuple of (combined_content, list_of_urls)
    """
    session = requests.Session()
    session.headers.update({
        "User-Agent": "KnowledgeImporter/1.0 (Documentation Indexer)"
    })

    # Discover pages
    pages = discover_pages(base_url, session, max_pages)

    print(f"\nFetching content from {len(pages)} pages...")

    # Fetch and combine content
    all_content = []
    for i, url in enumerate(pages):
        print(f"  [{i+1}/{len(pages)}] {url}")
        html = fetch_page(url, session)
        if html:
            markdown = html_to_markdown(html, url)
            if markdown.strip():
                all_content.append(f"\n\n---\n## Source: {url}\n---\n\n{markdown}")

        time.sleep(0.1)

    combined = "\n".join(all_content)
    return combined, pages


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print("\nAvailable agents:")
        from knowledge.importer import AgentDomain
        for a in AgentDomain:
            print(f"  - {a.value}")
        sys.exit(1)

    base_url = sys.argv[1]
    agent = sys.argv[2]
    title = sys.argv[3]
    ttl_days = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    tags = sys.argv[5].split(",") if len(sys.argv) > 5 else []

    print(f"Importing web documentation")
    print(f"  URL: {base_url}")
    print(f"  Agent: {agent}")
    print(f"  Title: {title}")
    print(f"  TTL: {ttl_days} days")
    print(f"  Tags: {tags}")
    print("=" * 60)

    # Fetch documentation
    content, urls = fetch_all_docs(base_url)

    if not content:
        print("ERROR: No content fetched")
        sys.exit(1)

    print(f"\nFetched {len(content)} characters from {len(urls)} pages")

    # Import into knowledge base
    importer = KnowledgeImporter()

    metadata = importer.import_web_docs(
        url=base_url,
        content=content,
        agent=agent,
        title=title,
        tags=tags,
        ttl_days=ttl_days,
    )

    print(f"\nImported successfully!")
    print(f"  ID: {metadata.id}")
    print(f"  Chunks: {metadata.chunk_count}")
    print(f"  Characters: {metadata.char_count}")
    print(f"  Expires: {metadata.expires_at}")


if __name__ == "__main__":
    main()
