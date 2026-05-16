from __future__ import annotations

from typing import Any

from src.domain.payloads.payload_validator import PayloadValidator
from src.domain.payloads.payload_value_reader import PayloadValueReader


class RequiredPayloadValueExtractor:
    """
    Required payload value extraction helper.
    """

    @staticmethod
    def get_required_value(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> Any:
        PayloadValidator.validate_required_key(
            payload=payload,
            key=key,
        )

        return PayloadValueReader.read_required(
            payload=payload,
            key=key,
        )