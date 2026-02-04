"""RLM MCP Server - Provider-agnostic Recursive Language Model implementation.

This MCP server enables processing documents that exceed typical context window
limits by orchestrating subcalls to various CLI tools (Gemini CLI, OpenCode,
Claude Code, GitHub Copilot CLI, etc.) without requiring API pay-as-you-go billing.
"""

__version__ = "0.1.0"
