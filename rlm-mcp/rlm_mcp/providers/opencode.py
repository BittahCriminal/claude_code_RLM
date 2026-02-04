"""OpenCode CLI provider for RLM subcalls.

Uses OpenCode (https://github.com/opencode-ai/opencode) - supports 75+ providers.
Works with existing provider configs (AWS Bedrock, Azure, local models, etc.).

Installation: Various (npm, brew, cargo, go, binary)
Authentication: Configured per-provider in ~/.opencode/config
"""

from __future__ import annotations

from .base import BaseProvider, ProviderConfig


class OpenCodeProvider(BaseProvider):
    """Provider for OpenCode CLI.

    OpenCode features:
    - Supports 75+ LLM providers
    - Works with existing auth configs (Bedrock, Azure, etc.)
    - Local model support (Ollama, LMStudio)
    - Session management

    No direct API billing - uses your existing provider configurations.
    """

    @classmethod
    def provider_name(cls) -> str:
        return "opencode"

    @classmethod
    def default_config(cls) -> ProviderConfig:
        return ProviderConfig(
            name="opencode",
            command="opencode",
            model=None,  # Uses configured default
            timeout_seconds=300,
            extra_args=[],
        )

    def build_command(self, prompt: str, context: str | None = None) -> list[str]:
        """Build OpenCode CLI command.

        OpenCode CLI usage:
        - opencode "prompt"
        - opencode --model gpt-4 "prompt"
        - echo "prompt" | opencode

        For non-interactive (headless) mode, we use appropriate flags.
        """
        cmd = [self.config.command]

        # Non-interactive mode
        cmd.append("--non-interactive")

        # Add model if specified
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        # Add any extra args (e.g., --provider for specific backend)
        cmd.extend(self.config.extra_args)

        # Add prompt as positional argument
        cmd.append(prompt)

        return cmd

    async def check_auth(self) -> tuple[bool, str]:
        """Check if OpenCode is available and configured."""
        if not self.is_available():
            return False, (
                "OpenCode CLI not found. Install from: https://github.com/opencode-ai/opencode\n"
                "Then configure providers in ~/.opencode/config"
            )

        try:
            result = await self._execute_command([self.config.command, "--version"])
            return True, f"OpenCode available: {result.strip()}"
        except Exception as e:
            return False, f"OpenCode found but error checking version: {e}"

    async def subcall(
        self,
        prompt: str,
        context: str | None = None,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> "ProviderResult":
        """Execute OpenCode subcall with file-based input for large contexts."""
        from .base import ProviderResult
        import time

        start_time = time.monotonic()

        # Build full prompt
        full_prompt = self._build_full_prompt(prompt, context, chunk_index, total_chunks)

        # For large prompts, use file input
        if len(full_prompt) > 10240:
            temp_path = await self._write_temp_file(full_prompt, suffix=".md")
            try:
                cmd = [
                    self.config.command,
                    "--non-interactive",
                    "--file", str(temp_path),
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
                    model=self.config.model,
                    duration_seconds=duration,
                )
            finally:
                try:
                    temp_path.unlink()
                except Exception:
                    pass
        else:
            return await super().subcall(prompt, context, chunk_index, total_chunks)
