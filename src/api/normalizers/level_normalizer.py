from __future__ import annotations

from typing import Any


class LevelNormalizer:
    """
    API boundary level input değerini normalize eder.
    """

    @staticmethod
    def normalize(
        value: Any,
    ) -> Any:
        if isinstance(value, str):
            return value.strip().upper()

        return value