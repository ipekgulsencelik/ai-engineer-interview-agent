from __future__ import annotations

import json
from typing import Any

from src.application.validators.json_response_validator import (
    JsonResponseValidator,
)


class JsonResponseParser:
    """
    Raw JSON text -> Python dict parser.
    """

    @staticmethod
    def parse_object(
        *,
        raw_text: str,
    ) -> dict[str, Any]:
        JsonResponseValidator.validate_raw_text(
            raw_text=raw_text,
        )

        try:
            payload = json.loads(
                raw_text,
            )

        except json.JSONDecodeError as exc:
            raise ValueError(
                "Failed to parse response as JSON."
            ) from exc

        JsonResponseValidator.validate_payload(
            payload=payload,
        )

        return payload