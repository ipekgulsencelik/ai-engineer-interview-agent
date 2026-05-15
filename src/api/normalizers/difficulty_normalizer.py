from __future__ import annotations

from typing import Any

from src.api.constants.difficulty import (
    DIFFICULTY_ALIASES,
)


class DifficultyNormalizer:
    """
    API boundary difficulty input değerini normalize eder.
    """

    @classmethod
    def normalize(
        cls,
        value: Any,
    ) -> Any:
        if not isinstance(value, str):
            return value

        normalized = value.strip().lower()

        if normalized.isdigit():
            return int(normalized)

        return DIFFICULTY_ALIASES.get(
            normalized,
            value,
        )