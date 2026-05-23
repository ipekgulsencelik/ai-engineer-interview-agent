from __future__ import annotations

from typing import Any

from src.application.validators.payload_field_validator import (
    PayloadFieldValidator,
)


class PayloadFieldExtractor:
    """
    JSON payload içinden primitive field access yapar.
    """

    @staticmethod
    def get_required_string(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> str:
        return PayloadFieldValidator.validate_required_string(
            value=payload.get(key),
            key=key,
        )

    @staticmethod
    def get_optional_string(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> str | None:
        return PayloadFieldValidator.validate_optional_string(
            value=payload.get(key),
            key=key,
        )

    @staticmethod
    def get_required_float(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> float:
        return PayloadFieldValidator.validate_required_float(
            value=payload.get(key),
            key=key,
        )

    @classmethod
    def get_optional_float(
        cls,
        *,
        payload: dict[str, Any],
        key: str,
    ) -> float | None:
        value = payload.get(key)

        if value is None:
            return None

        return PayloadFieldValidator.validate_required_float(
            value=value,
            key=key,
        )

    @staticmethod
    def get_optional_string_tuple(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> tuple[str, ...] | None:
        return PayloadFieldValidator.validate_optional_string_tuple(
            value=payload.get(key),
            key=key,
        )