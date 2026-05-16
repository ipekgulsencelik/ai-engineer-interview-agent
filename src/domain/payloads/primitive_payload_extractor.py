from __future__ import annotations

import math
from typing import Any

from src.domain.errors.question_validation_error import (
    QuestionValidationError,
)
from src.domain.payloads.required_payload_value_extractor import (
    RequiredPayloadValueExtractor,
)
from src.domain.payloads.payload_value_reader import (
    PayloadValueReader,
)


class PrimitivePayloadExtractor:
    """
    Primitive payload extraction and normalization helper.
    """

    @staticmethod
    def get_required_string(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> str:
        value = RequiredPayloadValueExtractor.get_required_value(
            payload=payload,
            key=key,
        )

        if not isinstance(value, str):
            raise QuestionValidationError(
                f"{key} must be a string."
            )

        normalized_value = value.strip()

        if not normalized_value:
            raise QuestionValidationError(
                f"{key} cannot be empty."
            )

        return normalized_value

    @staticmethod
    def get_required_int(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> int:
        value = RequiredPayloadValueExtractor.get_required_value(
            payload=payload,
            key=key,
        )

        if isinstance(value, bool) or not isinstance(value, int):
            raise QuestionValidationError(
                f"{key} must be an integer."
            )

        return value

    @staticmethod
    def get_optional_string(
        *,
        payload: dict[str, Any],
        key: str,
        default: str | None,
    ) -> str | None:
        value = PayloadValueReader.read_optional(
            payload=payload,
            key=key,
            default=default,
        )

        if value is None:
            return None

        if not isinstance(value, str):
            raise QuestionValidationError(
                f"{key} must be a string."
            )

        normalized_value = value.strip()

        if not normalized_value:
            raise QuestionValidationError(
                f"{key} cannot be empty."
            )

        return normalized_value

    @staticmethod
    def get_optional_float(
        *,
        payload: dict[str, Any],
        key: str,
        default: float,
    ) -> float:
        value = PayloadValueReader.read_optional(
            payload=payload,
            key=key,
            default=default,
        )

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise QuestionValidationError(
                f"{key} must be numeric."
            )

        normalized_value = float(value)

        if not math.isfinite(normalized_value):
            raise QuestionValidationError(
                f"{key} must be finite."
            )

        return normalized_value

    @staticmethod
    def get_optional_bool(
        *,
        payload: dict[str, Any],
        key: str,
        default: bool,
    ) -> bool:
        value = PayloadValueReader.read_optional(
            payload=payload,
            key=key,
            default=default,
        )

        if not isinstance(value, bool):
            raise QuestionValidationError(
                f"{key} must be a boolean."
            )

        return value