from __future__ import annotations

import json
import logging
from datetime import UTC
from datetime import datetime


class JsonFormatter(
    logging.Formatter,
):
    """
    Structured JSON log formatter.
    """

    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload = {
            "timestamp": (
                datetime.now(
                    UTC,
                ).isoformat()
            ),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        if hasattr(
            record,
            "extra",
        ):
            payload["extra"] = (
                record.extra
            )

        return json.dumps(
            payload,
            ensure_ascii=False,
        )