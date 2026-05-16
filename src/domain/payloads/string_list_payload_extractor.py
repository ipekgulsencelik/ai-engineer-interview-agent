from __future__ import annotations

from typing import Any

from src.domain.errors.question_validation_error import (
    QuestionValidationError,
)
from src.domain.payloads.payload_value_reader import (
    PayloadValueReader,
)


class StringListPayloadExtractor:
    """
    String list payload extraction and normalization helper.
    """

    @staticmethod
    def get_string_list(
        *,
        payload: dict[str, Any],
        key: str,
        default: list[str],
    ) -> list[str]:
        value = PayloadValueReader.read_optional(
            payload=payload,
            key=key,
            default=default,
        )

        if not isinstance(value, list):
            raise QuestionValidationError(
                f"{key} must be a list of strings."
            )

        normalized_items: list[str] = []

        for item in value:
            if not isinstance(item, str):
                raise QuestionValidationError(
                    f"{key} must contain only strings."
                )

            normalized_item = item.strip()

            if not normalized_item:
                raise QuestionValidationError(
                    f"{key} cannot contain empty strings."
                )

            normalized_items.append(
                normalized_item,
            )

        return normalized_items