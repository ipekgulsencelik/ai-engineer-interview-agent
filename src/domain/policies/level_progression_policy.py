from __future__ import annotations

from src.domain.constants.levels import (
    LEVEL_ORDER,
)
from src.domain.enums.level import Level
from src.domain.errors.level_transition_error import (
    LevelTransitionError,
)


class LevelProgressionPolicy:
    """
    Level progression boundary policy.
    """

    @classmethod
    def upgrade(
        cls,
        *,
        current_level: Level,
    ) -> Level:
        current_index = cls._get_current_index(
            current_level=current_level,
        )

        if current_index >= len(LEVEL_ORDER) - 1:
            return current_level

        return LEVEL_ORDER[current_index + 1]

    @classmethod
    def downgrade(
        cls,
        *,
        current_level: Level,
    ) -> Level:
        current_index = cls._get_current_index(
            current_level=current_level,
        )

        if current_index <= 0:
            return current_level

        return LEVEL_ORDER[current_index - 1]

    @staticmethod
    def _get_current_index(
        *,
        current_level: Level,
    ) -> int:
        try:
            return LEVEL_ORDER.index(
                current_level,
            )

        except ValueError as exc:
            raise LevelTransitionError(
                f"Unknown level: {current_level}."
            ) from exc