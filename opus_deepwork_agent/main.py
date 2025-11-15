"""
Main entry point for Opus Deepwork Agent.
"""

import logging
import traceback

import sys
from pathlib import Path

# Add src directory to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from opus_agent_base.cli.cli import create_cli_app
from src.opus_deepwork_agent.deepwork_agent_runner import run_deepwork_agent

logger = logging.getLogger(__name__)


def main():
    """Entry point for the Opus Agents CLI."""
    try:
        app = create_cli_app(
            agent_name="Opus Deepwork Agent",
            agent_description="Deepwork Scheduling Agent",
            agent_version="0.1.0",
            agent_runner=run_deepwork_agent,
        )
        app()
    except Exception as e:
        logger.error(f"Fatal error in main: {type(e).__name__}: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()
