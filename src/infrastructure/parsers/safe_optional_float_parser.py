from __future__ import annotations

from typing import Any


class SafeOptionalFloatParser:
    """
    Safe optional float parser.
    """

    @staticmethod
    def parse(
        *,
        value: Any,
    ) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None