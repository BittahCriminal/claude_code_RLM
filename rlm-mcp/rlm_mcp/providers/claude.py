"""Claude Code CLI provider for RLM subcalls.

Uses Anthropic's Claude Code CLI for subcalls.
Works with existing Claude subscription (Max plan, Enterprise, etc.).

Installation: npm install -g @anthropic-ai/claude-code
Authentication: claude login (uses existing Anthropic account)
"""

from __future__ import annotations

from .base import BaseProvider, ProviderConfig


class ClaudeCodeProvider(BaseProvider):
    """Provider for Claude Code CLI.

    Claude Code features:
    - Access to Claude Opus 4.5, Sonnet 4.5, Haiku 4.5
    - Integrated with Claude subscription (no separate API billing)
    - Supports MCP tools and skills
    - Agentic capabilities

    Uses existing Claude subscription - no pay-as-you-go API needed.
    """

    @classmethod
    def provider_name(cls) -> str:
        return "claude"

    @classmethod
    def default_config(cls) -> ProviderConfig:
        return ProviderConfig(
            name="claude",
            command="claude",
            model="haiku",  # Use Haiku for fast, cost-effective subcalls
            timeout_seconds=300,
            extra_args=[],
        )

    def build_command(self, prompt: str, context: str | None = None) -> list[str]:
        """Build Claude Code CLI command.

        Claude Code CLI usage:
        - claude "prompt"
        - claude --model haiku "prompt"
        - echo "prompt" | claude --print

        --print flag outputs response directly without interactive UI.
        """
        cmd = [self.config.command]

        # Print mode for non-interactive output
        cmd.append("--print")

        # Add model if specified
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        # Disable tools for simple subcalls (faster)
        cmd.append("--no-tools")

        # Add any extra args
        cmd.extend(self.config.extra_args)

        # Add prompt as positional argument
        cmd.append(prompt)

        return cmd

    async def check_auth(self) -> tuple[bool, str]:
        """Check if Claude Code is available and authenticated."""
        if not self.is_available():
            return False, (
                "Claude Code CLI not found. Install with: npm install -g @anthropic-ai/claude-code\n"
                "Then authenticate with: claude login"
            )

        try:
            # Check version
            result = await self._execute_command([self.config.command, "--version"])
            return True, f"Claude Code available: {result.strip()}"
        except Exception as e:
            return False, f"Claude Code found but may need authentication: {e}"

    async def subcall(
        self,
        prompt: str,
        context: str | None = None,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> "ProviderResult":
        """Execute Claude Code subcall.

        For RLM subcalls, we use --print --no-tools for fast, direct responses.
        """
        from .base import ProviderResult
        import time

        start_time = time.monotonic()

        # Build full prompt
        full_prompt = self._build_full_prompt(prompt, context, chunk_index, total_chunks)

        # Claude Code handles long prompts well, but for very large ones use file
        if len(full_prompt) > 50000:  # Claude has large context, higher threshold
            temp_path = await self._write_temp_file(full_prompt, suffix=".md")
            try:
                # Read file content into prompt via shell
                cmd = [
                    self.config.command,
                    "--print",
                    "--no-tools",
                ]
                if self.config.model:
                    cmd.extend(["--model", self.config.model])
                cmd.extend(self.config.extra_args)
                cmd.extend(["--file", str(temp_path)])

                result = await self._execute_command(cmd)
                duration = time.monotonic() - start_time

                return ProviderResult(
                    success=True,
                    output=result,
                    provider=self.provider_name(),
                    model=self.config.model or "haiku",
                    duration_seconds=duration,
                )
            finally:
                try:
                    temp_path.unlink()
                except Exception:
                    pass
        else:
            return await super().subcall(prompt, context, chunk_index, total_chunks)
