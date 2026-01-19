#!/usr/bin/env python3
"""
RLM Helper for GitHub Copilot CLI

This script helps GitHub Copilot CLI orchestrate RLM workflows by:
1. Loading agent templates
2. Preparing chunk invocation commands  
3. Formatting results

Usage:
  python3 scripts/rlm_copilot_helper.py load-agent rlm-subcall
  python3 scripts/rlm_copilot_helper.py prepare-chunks <query> <chunk_dir>
  python3 scripts/rlm_copilot_helper.py format-results <results_json>
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_agent_template(agent_name: str) -> str:
    """Load agent template from .github/agent_templates/"""
    template_path = Path(f".github/agent_templates/{agent_name}.txt")
    
    if not template_path.exists():
        raise FileNotFoundError(f"Agent template not found: {template_path}")
    
    return template_path.read_text()


def prepare_chunk_invocations(query: str, chunk_dir: str) -> List[Dict[str, str]]:
    """
    Prepare invocation data for all chunks in a directory.
    Returns list of dicts with chunk_path and invocation details.
    """
    chunk_path = Path(chunk_dir)
    
    if not chunk_path.exists():
        raise FileNotFoundError(f"Chunk directory not found: {chunk_dir}")
    
    chunk_files = sorted(chunk_path.glob("chunk_*.txt"))
    
    if not chunk_files:
        raise ValueError(f"No chunk files found in {chunk_dir}")
    
    agent_template = load_agent_template("rlm-subcall")
    
    invocations = []
    for i, chunk_file in enumerate(chunk_files):
        invocations.append({
            "chunk_id": f"chunk_{i:04d}",
            "chunk_path": str(chunk_file),
            "query": query,
            "agent_template": agent_template,
            "task_description": f"Analyzing chunk {i+1}/{len(chunk_files)}"
        })
    
    return invocations


def main():
    parser = argparse.ArgumentParser(description="RLM Helper for GitHub Copilot CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # load-agent command
    load_parser = subparsers.add_parser("load-agent", help="Load agent template")
    load_parser.add_argument("agent_name", help="Name of agent (e.g., rlm-subcall)")
    
    # prepare-chunks command
    prep_parser = subparsers.add_parser("prepare-chunks", help="Prepare chunk invocations")
    prep_parser.add_argument("query", help="User query")
    prep_parser.add_argument("chunk_dir", help="Directory containing chunks")
    
    args = parser.parse_args()
    
    if args.command == "load-agent":
        template = load_agent_template(args.agent_name)
        print(template)
    
    elif args.command == "prepare-chunks":
        invocations = prepare_chunk_invocations(args.query, args.chunk_dir)
        print(json.dumps(invocations, indent=2))
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
