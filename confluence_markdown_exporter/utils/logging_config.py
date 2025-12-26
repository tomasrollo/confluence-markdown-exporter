"""Logging configuration utilities."""

import logging
import sys


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
    
    # Set the logger level
    if verbose:
        logger.setLevel(logging.INFO)
        console_level = logging.INFO
    else:
        logger.setLevel(logging.WARNING)
        console_level = logging.WARNING
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(console_level)
    
    # Create formatter
    if verbose:
        # Detailed format for verbose mode
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    else:
        # Simpler format for non-verbose mode
        formatter = logging.Formatter("%(levelname)s: %(message)s")
    
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Prevent propagation to avoid duplicate logs
    logger.propagate = False
