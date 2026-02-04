"""Gemini CLI provider for RLM subcalls.

Uses Google's Gemini CLI (https://github.com/google-gemini/gemini-cli).
Free tier: 60 requests/minute, 1000 requests/day with personal Google account.

Installation: npm install -g @google/gemini-cli
Authentication: gemini (interactive login on first use)
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

from .base import BaseProvider, ProviderConfig


class GeminiProvider(BaseProvider):
    """Provider for Google's Gemini CLI.

    Gemini CLI features:
    - Free tier with generous limits (60 req/min, 1000/day)
    - 1M token context window (great for large chunks)
    - Built-in tools: search, file ops, shell commands
    - MCP support for extensibility

    No API key needed - uses OAuth via browser login.
    """

    @classmethod
    def provider_name(cls) -> str:
        return "gemini"

    @classmethod
    def default_config(cls) -> ProviderConfig:
        return ProviderConfig(
            name="gemini",
            command="gemini",
            model=None,  # Uses default model (Gemini 3 Flash)
            timeout_seconds=300,
            extra_args=[],
        )

    def build_command(self, prompt: str, context: str | None = None) -> list[str]:
        """Build Gemini CLI command.

        Gemini CLI accepts prompts via:
        - Direct argument: gemini "prompt"
        - Stdin: echo "prompt" | gemini
        - File: gemini -f prompt.txt

        For long prompts (with context), we use a temp file.
        """
        cmd = [self.config.command]

        # Add model if specified
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        # Add any extra args
        cmd.extend(self.config.extra_args)

        # For non-interactive mode (important for automation)
        cmd.append("--non-interactive")

        # Add the prompt - for long prompts, use stdin approach
        # Gemini CLI reads from positional arg or stdin
        cmd.append(prompt)

        return cmd

    async def check_auth(self) -> tuple[bool, str]:
        """Check if Gemini CLI is authenticated."""
        if not self.is_available():
            return False, (
                "Gemini CLI not found. Install with: npm install -g @google/gemini-cli\n"
                "Then authenticate with: gemini (follow browser prompts)"
            )

        # Try a simple command to check auth
        try:
            result = await self._execute_command([self.config.command, "--version"])
            return True, f"Gemini CLI available: {result.strip()}"
        except Exception as e:
            return False, f"Gemini CLI found but may need authentication: {e}"

    async def subcall(
        self,
        prompt: str,
        context: str | None = None,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> "ProviderResult":
        """Execute Gemini CLI subcall.

        For large contexts, we write to a temp file and use -f flag.
        """
        from .base import ProviderResult
        import time

        start_time = time.monotonic()

        # Build full prompt
        full_prompt = self._build_full_prompt(prompt, context, chunk_index, total_chunks)

        # For prompts > 10KB, use file-based input
        if len(full_prompt) > 10240:
            temp_path = await self._write_temp_file(full_prompt, suffix=".md")
            try:
                cmd = [
                    self.config.command,
                    "--non-interactive",
                    "-f", str(temp_path),
                ]
                if self.config.model:
                    cmd.extend(["--model", self.config.model])
                cmd.extend(self.config.extra_args)

                result = await self._execute_command(cmd)
                duration = time.monotonic() - start_time

                return ProviderResult(
                    success=True,
                    output=result,
                    provider=self.provider_name(),
                    model=self.config.model or "gemini-3-flash",
                    duration_seconds=duration,
                )
            finally:
                # Clean up temp file
                try:
                    temp_path.unlink()
                except Exception:
                    pass
        else:
            # Use parent class implementation for shorter prompts
            return await super().subcall(prompt, context, chunk_index, total_chunks)
