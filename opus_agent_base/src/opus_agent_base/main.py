import logging
import traceback

from opus_agent_base.cli import create_cli_app

logger = logging.getLogger(__name__)


def main():
    """Entry point for the CLI - now uses the new CLI module."""
    app = create_cli_app(
        "Opus Agent Base", "Base package for Opus AI Agents.", "0.1.0"
    )
    app()


if __name__ == "__main__":
    try:
        # For direct execution, run the CLI
        main()
    except Exception as e:
        logger.error(f"Fatal error in main: {type(e).__name__}: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise