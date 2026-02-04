"""Base provider interface for CLI-based LLM subcalls.

All providers execute CLI tools via subprocess - no direct API calls.
This ensures users leverage their existing CLI authentication and billing
(free tiers, subscriptions, enterprise plans) rather than pay-as-you-go APIs.
"""

from __future__ import annotations

import asyncio
import shutil
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class ProviderConfig:
    """Configuration for a CLI provider."""

    name: str
    """Provider identifier (e.g., 'gemini', 'opencode', 'claude', 'copilot')."""

    command: str
    """Base CLI command (e.g., 'gemini', 'opencode', 'claude', 'gh')."""

    model: str | None = None
    """Optional model override (provider-specific)."""

    timeout_seconds: int = 300
    """Maximum time to wait for CLI response (default: 5 minutes)."""

    extra_args: list[str] = field(default_factory=list)
    """Additional CLI arguments to pass."""

    env_vars: dict[str, str] = field(default_factory=dict)
    """Additional environment variables for the subprocess."""


@dataclass
class ProviderResult:
    """Result from a provider subcall."""

    success: bool
    """Whether the subcall completed successfully."""

    output: str
    """The response text from the LLM."""

    error: str | None = None
    """Error message if success is False."""

    provider: str = ""
    """Which provider was used."""

    model: str | None = None
    """Which model was used (if known)."""

    duration_seconds: float = 0.0
    """How long the subcall took."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Additional provider-specific metadata."""


class BaseProvider(ABC):
    """Abstract base class for CLI-based LLM providers.

    Each provider wraps a specific CLI tool and handles:
    - Checking if the CLI is available/authenticated
    - Formatting prompts appropriately for the CLI
    - Executing subcalls via subprocess
    - Parsing responses

    No direct API calls are made - all interactions go through CLI tools.
    """

    def __init__(self, config: ProviderConfig | None = None):
        """Initialize the provider with optional configuration."""
        self.config = config or self.default_config()

    @classmethod
    @abstractmethod
    def default_config(cls) -> ProviderConfig:
        """Return the default configuration for this provider."""
        ...

    @classmethod
    @abstractmethod
    def provider_name(cls) -> str:
        """Return the unique identifier for this provider."""
        ...

    @classmethod
    def is_available(cls) -> bool:
        """Check if the CLI tool is installed and accessible."""
        config = cls.default_config()
        return shutil.which(config.command) is not None

    @abstractmethod
    def build_command(self, prompt: str, context: str | None = None) -> list[str]:
        """Build the CLI command to execute.

        Args:
            prompt: The instruction/question to send to the LLM.
            context: Optional context (e.g., a chunk of document content).

        Returns:
            List of command arguments to pass to subprocess.
        """
        ...

    async def check_auth(self) -> tuple[bool, str]:
        """Check if the CLI tool is authenticated.

        Returns:
            Tuple of (is_authenticated, message).
        """
        if not self.is_available():
            return False, f"CLI tool '{self.config.command}' not found in PATH"
        return True, "CLI tool available (auth check varies by provider)"

    async def subcall(
        self,
        prompt: str,
        context: str | None = None,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> ProviderResult:
        """Execute a subcall to the LLM via CLI.

        Args:
            prompt: The instruction/question for this subcall.
            context: Optional context content (e.g., a document chunk).
            chunk_index: If processing chunks, the current chunk number.
            total_chunks: If processing chunks, the total number of chunks.

        Returns:
            ProviderResult with the LLM's response or error information.
        """
        import time

        start_time = time.monotonic()

        # Build the full prompt with context if provided
        full_prompt = self._build_full_prompt(prompt, context, chunk_index, total_chunks)

        # Build and execute the command
        cmd = self.build_command(full_prompt, context=None)  # Context already in prompt

        try:
            result = await self._execute_command(cmd)
            duration = time.monotonic() - start_time

            return ProviderResult(
                success=True,
                output=result,
                provider=self.provider_name(),
                model=self.config.model,
                duration_seconds=duration,
            )
        except asyncio.TimeoutError:
            duration = time.monotonic() - start_time
            return ProviderResult(
                success=False,
                output="",
                error=f"Timeout after {self.config.timeout_seconds} seconds",
                provider=self.provider_name(),
                duration_seconds=duration,
            )
        except subprocess.CalledProcessError as e:
            duration = time.monotonic() - start_time
            return ProviderResult(
                success=False,
                output=e.stdout or "",
                error=f"CLI error (exit code {e.returncode}): {e.stderr or 'Unknown error'}",
                provider=self.provider_name(),
                duration_seconds=duration,
            )
        except Exception as e:
            duration = time.monotonic() - start_time
            return ProviderResult(
                success=False,
                output="",
                error=f"Unexpected error: {type(e).__name__}: {e}",
                provider=self.provider_name(),
                duration_seconds=duration,
            )

    def _build_full_prompt(
        self,
        prompt: str,
        context: str | None,
        chunk_index: int | None,
        total_chunks: int | None,
    ) -> str:
        """Build the complete prompt including context and chunk info."""
        parts = []

        # Add chunk info if processing multiple chunks
        if chunk_index is not None and total_chunks is not None:
            parts.append(f"[Processing chunk {chunk_index + 1} of {total_chunks}]")
            parts.append("")

        # Add context if provided
        if context:
            parts.append("=== CONTENT START ===")
            parts.append(context)
            parts.append("=== CONTENT END ===")
            parts.append("")

        # Add the main prompt
        parts.append(prompt)

        return "\n".join(parts)

    async def _execute_command(self, cmd: list[str]) -> str:
        """Execute a CLI command asynchronously and return output."""
        import os

        # Merge environment variables
        env = os.environ.copy()
        env.update(self.config.env_vars)

        # Run the command
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=self.config.timeout_seconds,
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                cmd,
                stdout.decode("utf-8", errors="replace"),
                stderr.decode("utf-8", errors="replace"),
            )

        return stdout.decode("utf-8", errors="replace")

    async def _write_temp_file(self, content: str, suffix: str = ".txt") -> Path:
        """Write content to a temporary file and return the path."""
        import tempfile

        fd, path = tempfile.mkstemp(suffix=suffix, prefix="rlm_")
        try:
            with open(fd, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            import os
            os.close(fd)
            raise

        return Path(path)
