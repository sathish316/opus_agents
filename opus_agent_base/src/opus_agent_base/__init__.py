"""
Opus Agent Base - Core framework for building AI agents.
"""

from opus_agent_base.cli.cli import create_cli_app

__version__ = "0.1.0"


def main() -> None:
    """Entry point for opus-agent-base CLI."""
    app = create_cli_app(
        agent_name="Opus Agent Base",
        agent_description="Base framework for Opus AI Agents",
        agent_version=__version__,
    )
    app()


__all__ = ["main", "__version__"]
