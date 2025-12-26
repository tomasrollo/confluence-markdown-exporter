"""Logging configuration utilities."""

import logging
import sys
from datetime import datetime
from pathlib import Path


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application.
    
    Args:
        verbose: If True, outputs logs to console with INFO level.
                 If False, only WARNING and above are shown.
    """
    # Get the root logger for the package
    logger = logging.getLogger("confluence_markdown_exporter")

    # Remove any existing handlers to avoid duplicates
    logger.handlers.clear()

    # Set the logger level to INFO to capture all info-level logs
    logger.setLevel(logging.INFO)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    if verbose:
        console_level = logging.INFO
    else:
        console_level = logging.WARNING
    console_handler.setLevel(console_level)

    # Create formatter for console
    if verbose:
        # Detailed format for verbose mode
        console_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        # Simpler format for non-verbose mode
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Create file handler with timestamp
    log_dir = Path.cwd() / "logs"
    log_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"confluence_export_{timestamp}.log"

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Detailed format for file logs
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Log the file location
    logger.info(f"Logging to file: {log_file}")

    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
