import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def _parse_log_level(log_level):
    """
    Parse log level from string or int to logging constant.

    Args:
        log_level: Can be string ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
                   or int (logging.DEBUG, logging.INFO, etc.)

    Returns:
        int: logging level constant
    """
    if isinstance(log_level, str):
        log_level_upper = log_level.upper()
        level_map = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "WARN": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
        if log_level_upper not in level_map:
            print(f"⚠️  Invalid log level '{log_level}', defaulting to ERROR")
            return logging.ERROR
        return level_map[log_level_upper]
    return log_level


def setup_logging(log_level=logging.ERROR, console_output=True):
    """
    Setup logging configuration to write to /var/log/opus_agent_<timestamp>.log
    with fallback to user home directory if /var/log is not writable

    Args:
        log_level: The logging level (default: logging.ERROR). Can be string or int.
        console_output: Whether to show concise console output (default: True)
    """
    # Parse log level (handles both string and int)
    log_level = _parse_log_level(log_level)

    # Create timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Try to write to /var/log first
    primary_log_path = f"/var/log/opus_agent_{timestamp}.log"
    fallback_log_path = Path.home() / "logs" / f"opus_agent_{timestamp}.log"

    log_file_path = None

    # Test if we can write to /var/log
    try:
        # Try to create/touch the file to test permissions
        test_path = Path(primary_log_path)
        test_path.touch()
        log_file_path = primary_log_path
    except (PermissionError, OSError) as e:
        # Fallback to user home directory
        fallback_log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file_path = str(fallback_log_path)

    # Show concise console output only if enabled
    if console_output:
        print(f"📝 Logging to: {log_file_path}")

    # Configure logging with both console and file output
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console output
            logging.FileHandler(log_file_path, mode="a"),  # File output
        ],
        force=True,  # Force reconfiguration if already configured
    )

    # Set specific log levels for noisy modules
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    # Log startup message to file only (at DEBUG level so it doesn't show in console with ERROR level)
    logger = logging.getLogger(__name__)
    logger.debug("=" * 60)
    logger.debug("🚀 OPUS AGENT - STARTUP")
    logger.debug(f"📝 Log file: {log_file_path}")
    logger.debug(f"🐍 Python: {sys.version}")
    logger.debug(f"📁 Working directory: {os.getcwd()}")
    logger.debug(f"🔧 Log level: {logging.getLevelName(log_level)}")
    logger.debug("=" * 60)

    return log_file_path


def get_current_log_file():
    """Get the path to the current log file if logging is configured"""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename
    return None


def get_current_log_level():
    """Get the current log level"""
    root_logger = logging.getLogger()
    return logging.getLevelName(root_logger.level)


def set_log_level(level: str):
    """
    Dynamically change the log level

    Args:
        level: Log level as string ('ERROR', 'WARN', 'INFO', 'DEBUG')

    Returns:
        Tuple of (success: bool, message: str)
    """
    level_upper = level.upper()
    level_map = {
        "ERROR": logging.ERROR,
        "WARN": logging.WARNING,
        "WARNING": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }

    if level_upper not in level_map:
        return (
            False,
            f"Invalid log level: {level}. Valid levels: ERROR, WARN, INFO, DEBUG",
        )

    root_logger = logging.getLogger()
    old_level = logging.getLevelName(root_logger.level)
    root_logger.setLevel(level_map[level_upper])

    # Also update all handlers
    for handler in root_logger.handlers:
        handler.setLevel(level_map[level_upper])

    return True, f"Log level changed from {old_level} to {level_upper}"


def setup_debug_logging():
    """Setup debug level logging for troubleshooting"""
    return setup_logging(log_level=logging.DEBUG)


# Convenience function for quick setup
def quick_setup(log_level=logging.ERROR):
    """
    Quick logging setup with ERROR level by default.

    Args:
        log_level: The logging level (default: logging.ERROR). Can be string or int.
    """
    log_file = setup_logging(log_level=log_level)
    return log_file


def console_log(message: str):
    """
    Print a concise console message without logging noise.
    Use this for important user-facing messages during startup.

    Args:
        message: The message to print to console
    """
    print(message)
