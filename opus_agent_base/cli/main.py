import logging
import traceback

logger = logging.getLogger(__name__)

def main():
    """Entry point for the CLI - now uses the new CLI module."""
    from opus_agent_base.cli.cli import app
    app()

if __name__ == "__main__":
    try:
        # For direct execution, run the CLI
        main()
    except Exception as e:
        logger.error(f"Fatal error in main: {type(e).__name__}: {e}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise
