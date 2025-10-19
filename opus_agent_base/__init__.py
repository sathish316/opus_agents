"""
Opus Agent Base - Framework for building AI agents with common building blocks for:
* Agent definition
* Model management
* MCP server integrations
* Custom tools and Higher order tools that enhance MCP servers
* Config management
* Prompt library
* CLI
* Security features using Local models
"""

__version__ = "0.1.0"

# Import main modules for convenient access
from . import agent, cli, common, config, model, prompt, tools

__all__ = [
    "__version__",
    "agent",
    "cli",
    "common",
    "config",
    "model",
    "prompt",
    "tools",
]
