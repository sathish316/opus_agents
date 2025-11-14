"""
Opus Deepwork Agent - Deep work scheduling and management agent.
"""

from opus_agent_base.cli.cli import create_cli_app
from opus_deepwork_agent.deepwork_agent_runner import run_deepwork_agent

__version__ = "0.1.0"


def main() -> None:
    """Entry point for opus-deepwork-agent CLI."""
    app = create_cli_app(
        agent_name="Opus Deepwork Agent",
        agent_description="Deepwork Scheduling Agent",
        agent_version=__version__,
        agent_runner=run_deepwork_agent,
    )
    app()


__all__ = ["main", "__version__", "run_deepwork_agent"]
