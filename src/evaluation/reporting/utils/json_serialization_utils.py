from __future__ import annotations

import json
from enum import StrEnum
from typing import Any


class JSONSerializationUtils:
    """
    Shared JSON serialization helpers.
    """

    @staticmethod
    def to_json(
        *,
        payload: dict[
            str,
            Any,
        ],
    ) -> str:
        return (
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2,
                default=JSONSerializationUtils.default,
            )
            + "\n"
        )

    @staticmethod
    def default(
        value: object,
    ) -> object:
        if isinstance(
            value,
            StrEnum,
        ):
            return str(
                value,
            )

        if hasattr(
            value,
            "isoformat",
        ):
            return value.isoformat()

        return str(
            value,
        )