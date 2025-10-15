import logging
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    Setup logging configuration to write to /var/log/opus_todo_agent_<timestamp>.log
    with fallback to user home directory if /var/log is not writable
    """
    # Create timestamp for log file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Try to write to /var/log first
    primary_log_path = f"/var/log/opus_todo_agent_{timestamp}.log"
    fallback_log_path = Path.home() / "logs" / f"opus_todo_agent_{timestamp}.log"
    
    log_file_path = None
    
    # Test if we can write to /var/log
    try:
        # Try to create/touch the file to test permissions
        test_path = Path(primary_log_path)
        test_path.touch()
        log_file_path = primary_log_path
        print(f"✅ Logging to system location: {log_file_path}")
    except (PermissionError, OSError) as e:
        # Fallback to user home directory
        print(f"⚠️  Cannot write to /var/log: {e}")
        print(f"📁 Falling back to user logs directory...")
        
        # Create user logs directory
        fallback_log_path.parent.mkdir(parents=True, exist_ok=True)
        log_file_path = str(fallback_log_path)
        print(f"✅ Logging to: {log_file_path}")
    
    # Configure logging with both console and file output
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),  # Console output
            logging.FileHandler(log_file_path, mode='a')  # File output
        ]
    )
    
    # Set specific log levels for noisy modules
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    
    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("🚀 OPUS TODO AGENT - STARTUP")
    logger.info(f"📝 Log file: {log_file_path}")
    logger.info(f"🐍 Python: {sys.version}")
    logger.info(f"📁 Working directory: {os.getcwd()}")
    logger.info("=" * 60)
    
    return log_file_path


def get_current_log_file():
    """Get the path to the current log file if logging is configured"""
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return handler.baseFilename
    return None


def setup_debug_logging():
    """Setup debug level logging for troubleshooting"""
    return setup_logging(log_level=logging.DEBUG)


# Convenience function for quick setup
def quick_setup():
    """Quick logging setup with system info"""
    log_file = setup_logging()
    return log_file 