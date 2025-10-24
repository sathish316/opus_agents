"""
Opus TODO Agent - Productivity and TODO management agent.
"""

import asyncio
from opus_agent_base.cli.cli import create_cli_app
from opus_todo_agent.todo_agent_runner import run_todo_agent

__version__ = "0.1.0"


def main() -> None:
    """Entry point for opus-todo-agent CLI."""
    app = create_cli_app(
        agent_name="Opus TODO Agent",
        agent_description="Productivity and TODO Agent for Opus AI",
        agent_version=__version__,
    )
    app()


__all__ = ["main", "__version__", "run_todo_agent"]

