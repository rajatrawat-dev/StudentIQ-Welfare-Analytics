"""Standardized logging configuration for StudentIQ."""

import logging
import sys
from src.config.settings import settings

def get_logger(name: str = "StudentIQ") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO))
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logger.level)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        try:
            settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(settings.LOGS_DIR / "student_iq.log", encoding="utf-8")
            file_handler.setLevel(logger.level)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception:
            pass
    return logger