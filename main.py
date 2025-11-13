import logging
import traceback
from opus_agent_base.cli.cli import create_cli_app


logger = logging.getLogger(__name__)


def main():
    """Entry point for the Opus Agents CLI."""
    try:
        app = create_cli_app(
            agent_name="Opus Deepwork Agent",
            agent_description="Deepwork Agent for Opus AI",
            agent_version="0.1.0",
        )
        app()
    except Exception as e:
        logger.error(f"Fatal error in main: {type(e).__name__}: {e}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")
        raise


if __name__ == "__main__":
    main()