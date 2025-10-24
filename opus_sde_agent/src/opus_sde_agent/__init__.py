"""
Opus SDE Agent - Software Development Engineer Agent.
"""

import asyncio
from opus_agent_base.cli.cli import create_cli_app
from opus_sde_agent.sde_agent_runner import run_sde_agent

__version__ = "0.1.0"


def main() -> None:
    """Entry point for opus-sde-agent CLI."""
    app = create_cli_app(
        agent_name="Opus SDE Agent",
        agent_description="Software Development Engineer Agent for Opus AI",
        agent_version=__version__,
    )
    app()


__all__ = ["main", "__version__", "run_sde_agent"]

