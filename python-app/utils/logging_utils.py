"""Logging configuration and utilities."""

import logging


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure logging for the application."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)
