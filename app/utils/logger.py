import logging
import os
from logging.handlers import RotatingFileHandler

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = "app/logs"
LOG_FILE = f"{LOG_DIR}/app.log"


def get_logger(name: str) -> logging.Logger:
    """
    Create or return a configured logger
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # Prevent duplicate handlers

    logger.setLevel(LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler (CloudWatch / Docker logs)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (Local only)
    if not os.getenv("AWS_LAMBDA_FUNCTION_NAME"):
        os.makedirs(LOG_DIR, exist_ok=True)

        file_handler = RotatingFileHandler(
            LOG_FILE, maxBytes=5_000_000, backupCount=3
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger
