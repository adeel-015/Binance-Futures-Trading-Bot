"""Logging configuration for trading bot."""

import logging
import logging.handlers
from pathlib import Path


def get_logger(name):
    """
    Get a configured logger instance for a module.

    Args:
        name: Logger name (typically __name__ from calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if not logger.handlers:
        _configure_logging(logger)

    return logger


def _configure_logging(logger):
    """
    Configure logging with file and console handlers.

    Args:
        logger: Logger instance to configure
    """
    # Create logs directory if it doesn't exist
    logs_dir = Path(__file__).parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "trading_bot.log"

    # Set logger level
    logger.setLevel(logging.DEBUG)

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # File handler with rotation (5MB per file, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler for INFO level
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
