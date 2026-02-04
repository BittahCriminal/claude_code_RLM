"""Copilot CLI Provider for RLM subcalls.

This branch is Copilot-exclusive with dynamic environment detection.
Supports PowerShell (pwsh 7+) and WSL on Windows.

No API billing - uses your existing GitHub Copilot subscription.
"""

from .base import BaseProvider, ProviderConfig, ProviderResult
from .copilot import (
    CopilotProvider,
    ExecutionEnvironment,
    EnvironmentInfo,
    detect_environment,
)

# Copilot is the only provider on this branch
PROVIDERS: dict[str, type[BaseProvider]] = {
    "copilot": CopilotProvider,
}

# Default provider for this branch
DEFAULT_PROVIDER = "copilot"


def get_default_provider() -> CopilotProvider:
    """Get a configured instance of the default (Copilot) provider."""
    return CopilotProvider()


def check_environment() -> EnvironmentInfo:
    """Check the current execution environment for Copilot CLI.

    Returns:
        EnvironmentInfo with environment type, copilot path, and setup notes
    """
    return detect_environment()


__all__ = [
    # Base classes
    "BaseProvider",
    "ProviderConfig",
    "ProviderResult",
    # Copilot provider
    "CopilotProvider",
    # Environment detection
    "ExecutionEnvironment",
    "EnvironmentInfo",
    "detect_environment",
    "check_environment",
    # Registry
    "PROVIDERS",
    "DEFAULT_PROVIDER",
    "get_default_provider",
]
