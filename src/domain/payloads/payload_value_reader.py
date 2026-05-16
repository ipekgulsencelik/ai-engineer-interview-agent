from __future__ import annotations

from typing import Any


class PayloadValueReader:
    """
    Raw payload value access helper.
    """

    @staticmethod
    def read_required(
        *,
        payload: dict[str, Any],
        key: str,
    ) -> Any:
        return payload[key]

    @staticmethod
    def read_optional(
        *,
        payload: dict[str, Any],
        key: str,
        default: Any,
    ) -> Any:
        return payload.get(
            key,
            default,
        )