from __future__ import annotations

from typing import Any


class SafeIntParser:
    """
    Safe integer parser with fallback.
    """

    @staticmethod
    def parse(
        *,
        value: Any,
        default: int,
    ) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default