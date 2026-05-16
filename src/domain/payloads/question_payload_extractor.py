from __future__ import annotations

from typing import Any

from src.domain.payloads.payload_validator import PayloadValidator
from src.domain.payloads.primitive_payload_extractor import (
    PrimitivePayloadExtractor,
)
from src.domain.payloads.required_payload_value_extractor import (
    RequiredPayloadValueExtractor,
)
from src.domain.payloads.string_list_payload_extractor import (
    StringListPayloadExtractor,
)


class QuestionPayloadExtractor:
    """
    Question payload extraction facade.
    """

    def validate_payload(
        self,
        *,
        payload: object,
    ) -> None:
        PayloadValidator.validate_dict_payload(
            payload=payload,
        )

    def get_required_value(
        self,
        *,
        payload: dict[str, Any],
        key: str,
    ) -> Any:
        return RequiredPayloadValueExtractor.get_required_value(
            payload=payload,
            key=key,
        )

    def get_required_string(
        self,
        *,
        payload: dict[str, Any],
        key: str,
    ) -> str:
        return PrimitivePayloadExtractor.get_required_string(
            payload=payload,
            key=key,
        )

    def get_required_int(
        self,
        *,
        payload: dict[str, Any],
        key: str,
    ) -> int:
        return PrimitivePayloadExtractor.get_required_int(
            payload=payload,
            key=key,
        )

    def get_optional_string(
        self,
        *,
        payload: dict[str, Any],
        key: str,
        default: str | None,
    ) -> str | None:
        return PrimitivePayloadExtractor.get_optional_string(
            payload=payload,
            key=key,
            default=default,
        )

    def get_optional_float(
        self,
        *,
        payload: dict[str, Any],
        key: str,
        default: float,
    ) -> float:
        return PrimitivePayloadExtractor.get_optional_float(
            payload=payload,
            key=key,
            default=default,
        )

    def get_optional_bool(
        self,
        *,
        payload: dict[str, Any],
        key: str,
        default: bool,
    ) -> bool:
        return PrimitivePayloadExtractor.get_optional_bool(
            payload=payload,
            key=key,
            default=default,
        )

    def get_optional_string_list(
        self,
        *,
        payload: dict[str, Any],
        key: str,
        default: list[str],
    ) -> list[str]:
        return StringListPayloadExtractor.get_string_list(
            payload=payload,
            key=key,
            default=default,
        )