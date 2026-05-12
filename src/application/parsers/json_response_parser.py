from __future__ import annotations

import json
from typing import Any


class JsonResponseParser:
    """
    Raw JSON text'i Python dict payload'a çevirir.

    Bu sınıf sadece JSON parsing sorumluluğuna sahiptir.
    EvaluationResult, metadata veya field validation bilmez.
    """

    @staticmethod
    def parse_object(raw_text: str) -> dict[str, Any]:
        if not isinstance(raw_text, str):
            raise TypeError("raw_text must be a string.")

        if not raw_text.strip():
            raise ValueError("raw_text cannot be empty.")

        try:
            payload = json.loads(raw_text)

        except json.JSONDecodeError as error:
            raise ValueError(
                "Failed to parse response as JSON."
            ) from error

        if not isinstance(payload, dict):
            raise TypeError(
                "Parsed JSON payload must be an object."
            )

        return payload