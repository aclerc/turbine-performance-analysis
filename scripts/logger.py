"""Logging utilities."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def setup_logger(log_fpath: Path, level: int = logging.INFO) -> None:
    """Set up a logger with a file handler and a console handler."""
    log_formatter_file = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    root_logger = logging.getLogger()

    # clear out any existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    root_logger.setLevel(level)

    log_fpath.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.FileHandler(log_fpath, mode="w")
    file_handler.setFormatter(log_formatter_file)
    root_logger.addHandler(file_handler)

    log_formatter_console = logging.Formatter("%(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter_console)
    root_logger.addHandler(console_handler)
