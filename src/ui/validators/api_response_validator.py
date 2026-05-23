from __future__ import annotations

from typing import Any


class APIResponseValidator:
    """
    API response validation utilities.
    """

    @staticmethod
    def validate_json_object(
        *,
        value: object,
    ) -> dict[str, Any]:
        if not isinstance(value, dict):
            raise TypeError(
                "API response must be a JSON object.",
            )

        return value