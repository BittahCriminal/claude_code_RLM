"""GitHub Copilot CLI provider for RLM subcalls.

Copilot-exclusive provider with dynamic environment detection.
Supports both PowerShell (pwsh) and WSL environments on Windows.

Installation: npm install -g @github/copilot
Authentication: copilot (follow /login prompts)

Environment Detection:
- Native Linux/macOS: Direct copilot command
- PowerShell (pwsh): Direct copilot command (requires pwsh 7+)
- WSL: Direct copilot command (runs inside WSL)
- CMD calling WSL: wsl copilot wrapper
"""

from __future__ import annotations

import asyncio
import os
import sys
import shutil
import tempfile
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from .base import BaseProvider, ProviderConfig, ProviderResult


class ExecutionEnvironment(Enum):
    """Detected execution environment."""
    NATIVE_UNIX = "native_unix"      # Linux/macOS - direct copilot
    POWERSHELL = "powershell"         # Windows PowerShell 7+ - direct copilot
    WSL_INSIDE = "wsl_inside"         # Running inside WSL - direct copilot
    CMD_VIA_WSL = "cmd_via_wsl"       # Windows CMD - call via wsl wrapper
    UNSUPPORTED = "unsupported"       # No viable execution path


@dataclass
class EnvironmentInfo:
    """Information about the detected environment."""
    env_type: ExecutionEnvironment
    copilot_path: Optional[str]
    shell_name: str
    requires_wsl_wrapper: bool
    notes: str


def detect_environment() -> EnvironmentInfo:
    """Detect the current execution environment and best Copilot execution strategy.

    Returns:
        EnvironmentInfo with details about how to run Copilot CLI
    """
    # Check if we're on Unix-like system (Linux/macOS)
    if sys.platform in ("linux", "darwin"):
        # Check if we're inside WSL
        is_wsl = _is_running_in_wsl()

        copilot_path = shutil.which("copilot")
        if copilot_path:
            env_type = ExecutionEnvironment.WSL_INSIDE if is_wsl else ExecutionEnvironment.NATIVE_UNIX
            return EnvironmentInfo(
                env_type=env_type,
                copilot_path=copilot_path,
                shell_name="wsl" if is_wsl else ("zsh" if sys.platform == "darwin" else "bash"),
                requires_wsl_wrapper=False,
                notes="Direct copilot execution"
            )
        else:
            return EnvironmentInfo(
                env_type=ExecutionEnvironment.UNSUPPORTED,
                copilot_path=None,
                shell_name="unknown",
                requires_wsl_wrapper=False,
                notes="Copilot CLI not found. Install with: npm install -g @github/copilot"
            )

    # Windows detection
    if sys.platform == "win32":
        return _detect_windows_environment()

    # Unknown platform
    return EnvironmentInfo(
        env_type=ExecutionEnvironment.UNSUPPORTED,
        copilot_path=None,
        shell_name="unknown",
        requires_wsl_wrapper=False,
        notes=f"Unsupported platform: {sys.platform}"
    )


def _is_running_in_wsl() -> bool:
    """Check if currently running inside WSL."""
    # Check for WSL-specific indicators
    if os.path.exists("/proc/version"):
        try:
            with open("/proc/version", "r") as f:
                version_info = f.read().lower()
                return "microsoft" in version_info or "wsl" in version_info
        except Exception:
            pass

    # Check for WSL environment variables
    return bool(os.environ.get("WSL_DISTRO_NAME") or os.environ.get("WSLENV"))


def _detect_windows_environment() -> EnvironmentInfo:
    """Detect the best execution environment on Windows."""

    # Check if running in PowerShell
    is_powershell = _is_running_in_powershell()

    # Check for native copilot (works in pwsh 7+)
    copilot_path = shutil.which("copilot")

    if copilot_path and is_powershell:
        # PowerShell with native copilot - best case for Windows
        return EnvironmentInfo(
            env_type=ExecutionEnvironment.POWERSHELL,
            copilot_path=copilot_path,
            shell_name="pwsh",
            requires_wsl_wrapper=False,
            notes="PowerShell with native Copilot CLI"
        )

    # Check for WSL availability
    wsl_path = shutil.which("wsl")
    if wsl_path:
        # Check if copilot is available in WSL
        copilot_in_wsl = _check_copilot_in_wsl()
        if copilot_in_wsl:
            return EnvironmentInfo(
                env_type=ExecutionEnvironment.CMD_VIA_WSL,
                copilot_path="wsl copilot",
                shell_name="cmd/wsl",
                requires_wsl_wrapper=True,
                notes="Using WSL wrapper for Copilot CLI"
            )

    # Native copilot exists but not in PowerShell (might work, experimental)
    if copilot_path:
        return EnvironmentInfo(
            env_type=ExecutionEnvironment.POWERSHELL,  # Try it anyway
            copilot_path=copilot_path,
            shell_name="cmd",
            requires_wsl_wrapper=False,
            notes="Native Copilot CLI (experimental in non-pwsh)"
        )

    return EnvironmentInfo(
        env_type=ExecutionEnvironment.UNSUPPORTED,
        copilot_path=None,
        shell_name="unknown",
        requires_wsl_wrapper=False,
        notes="No Copilot CLI found. Install in WSL or PowerShell 7+"
    )


def _is_running_in_powershell() -> bool:
    """Check if currently running inside PowerShell."""
    # Check for PowerShell-specific environment variables
    if os.environ.get("PSModulePath"):
        return True

    # Check parent process name (less reliable)
    ppid_name = os.environ.get("_", "")
    if "pwsh" in ppid_name.lower() or "powershell" in ppid_name.lower():
        return True

    # Check for PSVersionTable indicator
    return bool(os.environ.get("POWERSHELL_DISTRIBUTION_CHANNEL"))


def _check_copilot_in_wsl() -> bool:
    """Check if copilot is available inside WSL."""
    try:
        result = os.popen("wsl which copilot 2>/dev/null").read().strip()
        return bool(result)
    except Exception:
        return False


class CopilotProvider(BaseProvider):
    """Copilot CLI provider with dynamic environment detection.

    Automatically detects and adapts to:
    - PowerShell (pwsh 7+): Direct copilot command
    - WSL: Direct copilot command or wsl wrapper from CMD
    - Native Unix: Direct copilot command

    Features:
    - Multiple models (Claude Sonnet 4.5, GPT-5, GPT-5 mini, etc.)
    - Non-interactive mode via -p flag
    - Automatic tool approval for automation
    - Context via temp files for large documents
    """

    def __init__(self, config: ProviderConfig | None = None):
        """Initialize with environment detection."""
        self._env_info = detect_environment()
        super().__init__(config)

    @classmethod
    def provider_name(cls) -> str:
        return "copilot"

    @classmethod
    def default_config(cls) -> ProviderConfig:
        """Generate config based on detected environment."""
        env_info = detect_environment()

        return ProviderConfig(
            name="copilot",
            command="wsl" if env_info.requires_wsl_wrapper else "copilot",
            model=None,  # Default: Claude Sonnet 4.5
            timeout_seconds=300,
            extra_args=[],
        )

    @property
    def environment(self) -> EnvironmentInfo:
        """Get the detected environment info."""
        return self._env_info

    def build_command(self, prompt: str, context: str | None = None) -> list[str]:
        """Build Copilot CLI command based on environment.

        Command structure:
        - Direct: copilot -p "prompt" --allow-all-tools [--model X]
        - WSL wrapper: wsl copilot -p "prompt" --allow-all-tools [--model X]
        """
        cmd = []

        if self._env_info.requires_wsl_wrapper:
            cmd.append("wsl")

        cmd.append("copilot")

        # Non-interactive prompt mode
        cmd.extend(["-p", prompt])

        # Allow all tools for automation (no interactive prompts)
        cmd.append("--allow-all-tools")

        # Add model if specified
        if self.config.model:
            cmd.extend(["--model", self.config.model])

        # Add any extra args from config
        cmd.extend(self.config.extra_args)

        return cmd

    @classmethod
    def is_available(cls) -> bool:
        """Check if Copilot CLI is available in any supported environment."""
        env_info = detect_environment()
        return env_info.env_type != ExecutionEnvironment.UNSUPPORTED

    async def check_auth(self) -> tuple[bool, str]:
        """Check Copilot CLI availability and authentication status."""
        env = self._env_info

        if env.env_type == ExecutionEnvironment.UNSUPPORTED:
            return False, self._get_install_instructions()

        # Try to get version to verify installation
        try:
            cmd = ["wsl", "copilot", "--version"] if env.requires_wsl_wrapper else ["copilot", "--version"]
            result = await self._execute_command(cmd)
            version = result.strip().split('\n')[0] if result else "unknown"

            return True, (
                f"Copilot CLI ready\n"
                f"  Environment: {env.env_type.value}\n"
                f"  Version: {version}\n"
                f"  Shell: {env.shell_name}"
            )
        except Exception as e:
            return False, f"Copilot CLI check failed: {e}\n{self._get_install_instructions()}"

    def _get_install_instructions(self) -> str:
        """Get environment-specific install instructions."""
        if sys.platform == "win32":
            return (
                "Copilot CLI not available.\n\n"
                "Option 1 - PowerShell 7+ (recommended):\n"
                "  1. Install pwsh: winget install Microsoft.PowerShell\n"
                "  2. In pwsh: npm install -g @github/copilot\n"
                "  3. Authenticate: copilot (follow /login)\n\n"
                "Option 2 - WSL:\n"
                "  1. Install WSL: wsl --install\n"
                "  2. In WSL: npm install -g @github/copilot\n"
                "  3. Authenticate: copilot (follow /login)"
            )
        else:
            return (
                "Copilot CLI not found.\n"
                "Install: npm install -g @github/copilot\n"
                "Authenticate: copilot (follow /login prompts)"
            )

    async def subcall(
        self,
        prompt: str,
        context: str | None = None,
        chunk_index: int | None = None,
        total_chunks: int | None = None,
    ) -> ProviderResult:
        """Execute a Copilot CLI subcall.

        Handles:
        - Short prompts: Direct command line
        - Long prompts/context: Temp file with file reference
        - Path conversion for WSL when needed
        """
        import time
        start_time = time.monotonic()

        # Build the full prompt with context
        full_prompt = self._build_full_prompt(prompt, context, chunk_index, total_chunks)

        # Determine if we need to use temp file approach
        # Conservative limit for command line length
        max_inline_len = 4000

        try:
            if len(full_prompt) > max_inline_len:
                result = await self._subcall_with_file(prompt, context, chunk_index, total_chunks)
            else:
                cmd = self.build_command(full_prompt)
                result = await self._execute_command(cmd)

            duration = time.monotonic() - start_time

            return ProviderResult(
                success=True,
                output=result,
                provider=self.provider_name(),
                model=self.config.model or "copilot-default",
                duration_seconds=duration,
                metadata={
                    "environment": self._env_info.env_type.value,
                    "shell": self._env_info.shell_name,
                    "wsl_wrapper": self._env_info.requires_wsl_wrapper,
                },
            )
        except Exception as e:
            duration = time.monotonic() - start_time
            return ProviderResult(
                success=False,
                output="",
                error=str(e),
                provider=self.provider_name(),
                duration_seconds=duration,
                metadata={"environment": self._env_info.env_type.value},
            )

    async def _subcall_with_file(
        self,
        prompt: str,
        context: str | None,
        chunk_index: int | None,
        total_chunks: int | None,
    ) -> str:
        """Handle subcall with context in a temp file."""
        if context is None:
            cmd = self.build_command(prompt)
            return await self._execute_command(cmd)

        # Write context to temp file
        temp_path = await self._write_temp_file(context, suffix=".txt")

        try:
            chunk_info = ""
            if chunk_index is not None and total_chunks is not None:
                chunk_info = f"[Chunk {chunk_index + 1}/{total_chunks}] "

            # Convert path for WSL if needed
            file_ref = self._convert_path_for_env(temp_path)

            file_prompt = (
                f"{chunk_info}Analyze the content in: {file_ref}\n\n"
                f"Task: {prompt}"
            )

            cmd = self.build_command(file_prompt)
            return await self._execute_command(cmd)
        finally:
            try:
                temp_path.unlink()
            except Exception:
                pass

    def _convert_path_for_env(self, path: Path) -> str:
        """Convert file path based on execution environment."""
        path_str = str(path)

        # If using WSL wrapper from Windows, convert to WSL path
        if self._env_info.requires_wsl_wrapper and sys.platform == "win32":
            return self._windows_to_wsl_path(path_str)

        return path_str

    def _windows_to_wsl_path(self, path: str) -> str:
        """Convert Windows path to WSL path format.

        C:\\Users\\Name\\file.txt -> /mnt/c/Users/Name/file.txt
        """
        if len(path) >= 2 and path[1] == ':':
            drive = path[0].lower()
            rest = path[2:].replace('\\', '/')
            return f"/mnt/{drive}{rest}"
        return path.replace('\\', '/')


# Export environment detection for external use
__all__ = [
    "CopilotProvider",
    "ExecutionEnvironment",
    "EnvironmentInfo",
    "detect_environment",
]
