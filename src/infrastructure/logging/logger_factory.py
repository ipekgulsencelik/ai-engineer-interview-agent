from __future__ import annotations

import logging
import sys

from src.infrastructure.logging.json_formatter import (
    JsonFormatter,
)


class LoggerFactory:
    """
    Centralized structured logger factory.
    """

    @staticmethod
    def create_logger(
        name: str,
    ) -> logging.Logger:
        logger = logging.getLogger(
            name,
        )

        if logger.hasHandlers():
            return logger

        logger.setLevel(
            logging.INFO,
        )

        handler = logging.StreamHandler(
            sys.stdout,
        )

        handler.setFormatter(
            JsonFormatter(),
        )

        logger.addHandler(
            handler,
        )

        logger.propagate = False

        return logger