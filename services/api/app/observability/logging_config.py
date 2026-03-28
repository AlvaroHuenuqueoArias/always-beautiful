from __future__ import annotations

import logging
import sys

LOGGER_NAME = "always-beautiful-api"
_LOGGER: logging.Logger | None = None


def configure_logging() -> logging.Logger:
    """
    Configura una única instancia del logger principal del backend.
    """

    global _LOGGER

    if _LOGGER is not None:
        return _LOGGER

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    _LOGGER = logger
    return logger