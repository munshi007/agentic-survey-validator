"""A minimal, strictly-configured logger."""

import logging

def get_logger(name: str) -> logging.Logger:
    """Returns a configured logger instance."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        sh = logging.StreamHandler()
        formatter = logging.Formatter('[%(levelname)s] %(name)s - %(message)s')
        sh.setFormatter(formatter)
        logger.addHandler(sh)
    return logger
