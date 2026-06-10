from __future__ import annotations


class JsonResponseValidator:
    """
    JSON response validation helper.
    """

    @staticmethod
    def validate_raw_text(
        *,
        raw_text: str,
    ) -> None:
        if not isinstance(raw_text, str):
            raise TypeError(
                "raw_text must be a string."
            )

        if not raw_text.strip():
            raise ValueError(
                "raw_text cannot be empty."
            )

    @staticmethod
    def validate_payload(
        *,
        payload: object,
    ) -> None:
        if not isinstance(payload, dict):
            raise TypeError(
                "Parsed JSON payload must be an object."
            )