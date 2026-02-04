#!/usr/bin/env python3
"""Run a simple RLM loop using a non-interactive CLI provider."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import textwrap
import os
from pathlib import Path
from typing import List


RLM_REPL = Path(".claude/skills/rlm/scripts/rlm_repl.py")
STATE_DIR = Path(".claude/rlm_state")
DEFAULT_CHUNK_DIR = STATE_DIR / "chunks"
DEFAULT_OUTPUT = STATE_DIR / "opencode_run.json"
DEFAULT_MODELS = {
    "opencode": "anthropic/claude-3-5-sonnet",
    "claude": "opus",
    "codex": "gpt-5.2-codex",
    "copilot": "claude-sonnet-4.5",
    "gemini": "gemini-3-pro-preview",
}
DOMAIN_MODELS = {
    "general": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-sonnet-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "software": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "gpt-5.2-codex",
        "gemini": "gemini-3-pro-preview",
    },
    "extra-thinking": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-opus-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "security": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-opus-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "cloud-architecture": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-sonnet-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "devops": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "gpt-5.2-codex",
        "gemini": "gemini-3-pro-preview",
    },
    "data-engineering": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "gpt-5.2-codex",
        "gemini": "gemini-3-pro-preview",
    },
    "ml-ai": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-opus-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "frontend": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-sonnet-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "backend": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "gpt-5.2-codex",
        "gemini": "gemini-3-pro-preview",
    },
    "testing": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "gpt-5.2-codex",
        "gemini": "gemini-3-pro-preview",
    },
    "code-review": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-opus-4.5",
        "gemini": "gemini-3-pro-preview",
    },
    "docs": {
        "opencode": "anthropic/claude-3-5-sonnet",
        "claude": "opus",
        "codex": "gpt-5.2-codex",
        "copilot": "claude-sonnet-4.5",
        "gemini": "gemini-3-pro-preview",
    },
}
MODEL_ENV_VARS = {
    "opencode": "OPENCODE_MODEL",
    "claude": "CLAUDE_MODEL",
    "codex": "CODEX_MODEL",
    "copilot": "COPILOT_MODEL",
    "gemini": "GEMINI_MODEL",
}


def run_command(cmd: List[str], input_text: str | None = None) -> str:
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        message = "\n".join(line for line in [stdout, stderr] if line)
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{message}")
    return result.stdout.strip()


def command_available(command: str) -> bool:
    result = subprocess.run(
        ["/usr/bin/env", "sh", "-c", f"command -v {command}"],
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


def init_repl(context_path: Path) -> None:
    run_command(["python3", str(RLM_REPL), "init", str(context_path)])


def write_chunks(chunk_dir: Path, size: int, overlap: int) -> List[Path]:
    code = textwrap.dedent(
        f"""
        paths = write_chunks('{chunk_dir.as_posix()}', size={size}, overlap={overlap})
        print('\\n'.join(paths))
        """
    ).lstrip()
    output = run_command(["python3", str(RLM_REPL), "exec"], input_text=code)
    return [Path(line) for line in output.splitlines() if line.strip()]


def build_chunk_prompt(query: str, chunk_id: str, chunk_text: str) -> str:
    return textwrap.dedent(
        f"""
        You are an RLM subcall. Use only the provided chunk to answer the query.
        Return JSON with: chunk_id, relevant_points (array of strings), missing (array), answer_if_complete.

        Query: {query}
        Chunk ID: {chunk_id}
        Chunk Content:
        {chunk_text}
        """
    ).strip()


def build_synthesis_prompt(query: str, analyses: List[dict]) -> str:
    return textwrap.dedent(
        f"""
        You are the root model. Synthesize a single concise answer to the query.
        Use only the chunk analyses provided below.

        Query: {query}

        Chunk Analyses (JSON):
        {json.dumps(analyses, indent=2)}
        """
    ).strip()


def provider_command(provider: str, prompt: str, model: str | None, agent: str | None) -> List[str]:
    if provider == "opencode":
        cmd = ["opencode", "run", prompt]
        if model:
            cmd.extend(["-m", model])
        if agent:
            cmd.extend(["--agent", agent])
        return cmd

    if provider == "claude":
        cmd = ["claude", "-p", prompt]
        if model:
            cmd.extend(["--model", model])
        if agent:
            cmd.extend(["--agent", agent])
        return cmd

    if provider == "codex":
        cmd = ["codex", "exec", prompt]
        if model:
            cmd.extend(["-m", model])
        return cmd

    if provider == "copilot":
        cmd = ["copilot", "-p", prompt, "--allow-all-tools"]
        if model:
            cmd.extend(["--model", model])
        return cmd

    if provider == "gemini":
        cmd = ["gemini"]
        if model:
            cmd.extend(["--model", model])
        cmd.append(prompt)
        return cmd

    raise ValueError(f"Unsupported provider: {provider}")


def run_provider(provider: str, prompt: str, model: str | None, agent: str | None) -> str:
    cmd = provider_command(provider, prompt, model, agent)
    return run_command(cmd)


def resolve_model(provider: str, model: str | None, domain: str | None) -> str | None:
    if model:
        return model
    if domain:
        domain_models = DOMAIN_MODELS.get(domain)
        if domain_models:
            domain_model = domain_models.get(provider)
            if domain_model:
                return domain_model
    env_key = MODEL_ENV_VARS.get(provider)
    env_value = os.environ.get(env_key) if env_key else None
    if env_value:
        return env_value
    return DEFAULT_MODELS.get(provider)


def resolve_provider(provider: str) -> str:
    if provider != "auto":
        return provider
    for candidate in ["opencode", "claude", "codex", "copilot", "gemini"]:
        if command_available(candidate):
            return candidate
    raise RuntimeError("No supported provider CLI found on PATH")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run an RLM loop using opencode/claude/codex/copoly non-interactive calls."
    )
    parser.add_argument("--context", required=True, help="Path to the context file")
    parser.add_argument("--query", required=True, help="User query")
    parser.add_argument(
        "--provider",
        default="opencode",
        choices=["opencode", "claude", "codex", "copilot", "gemini", "auto"],
        help="Provider CLI to run (use 'auto' to detect)",
    )
    parser.add_argument("--model", help="Model to use (provider/model or provider-specific)")
    parser.add_argument(
        "--domain",
        choices=sorted(DOMAIN_MODELS.keys()),
        help="Domain preset for provider model selection",
    )
    parser.add_argument("--agent", help="Agent to use (provider-specific)")
    parser.add_argument("--chunk-size", type=int, default=200000)
    parser.add_argument("--overlap", type=int, default=0)
    parser.add_argument(
        "--chunk-dir",
        default=str(DEFAULT_CHUNK_DIR),
        help="Directory to store chunk files",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Path to write JSON output",
    )

    args = parser.parse_args()

    context_path = Path(args.context)
    chunk_dir = Path(args.chunk_dir)
    output_path = Path(args.output)

    resolved_provider = resolve_provider(args.provider)
    resolved_model = resolve_model(resolved_provider, args.model, args.domain)

    init_repl(context_path)
    chunk_paths = write_chunks(chunk_dir, args.chunk_size, args.overlap)

    analyses = []
    for chunk_path in chunk_paths:
        chunk_text = chunk_path.read_text(encoding="utf-8")
        chunk_prompt = build_chunk_prompt(args.query, chunk_path.name, chunk_text)
        analysis_text = run_provider(resolved_provider, chunk_prompt, resolved_model, args.agent)
        analyses.append({
            "chunk": chunk_path.name,
            "response": analysis_text,
        })

    synthesis_prompt = build_synthesis_prompt(args.query, analyses)
    final_answer = run_provider(resolved_provider, synthesis_prompt, resolved_model, args.agent)

    payload = {
        "provider": resolved_provider,
        "model": resolved_model,
        "domain": args.domain,
        "agent": args.agent,
        "context": str(context_path),
        "query": args.query,
        "chunks": [str(p) for p in chunk_paths],
        "analyses": analyses,
        "final_answer": final_answer,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    sys.stdout.write(final_answer + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
