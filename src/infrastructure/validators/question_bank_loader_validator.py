from __future__ import annotations

from typing import Any


class QuestionBankLoaderValidator:
    """Validation utilities for JSON-backed question repository payloads."""

    @staticmethod
    def validate_payload(data: Any) -> None:
        if not isinstance(data, list):
            raise ValueError("Question bank JSON root must be a list.")

        for index, item in enumerate(data):
            if not isinstance(item, dict):
                raise ValueError(
                    "Each question record must be an object. "
                    f"Invalid item type at index {index}: {type(item).__name__}"
                )