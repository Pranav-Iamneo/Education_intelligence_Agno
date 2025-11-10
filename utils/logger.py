"""
Logger configuration for Education Intelligence System
"""

import logging
import sys
from config import settings


def setup_logger(name: str = None) -> logging.Logger:
    """
    Setup and configure logger

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    logger_name = name or "education_intelligence"
    logger = logging.getLogger(logger_name)

    # Only add handlers if they don't exist
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger
