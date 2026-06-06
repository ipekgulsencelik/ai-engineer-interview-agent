from __future__ import annotations

from typing import Protocol

from src.domain.enums.level import Level


class LevelNormalizer(Protocol):
    """
    Level normalization contract.
    """

    def normalize(
        self,
        value: Level | str,
    ) -> Level:
        """
        Normalize a raw level value into a Level enum.
        """
        ...


class DefaultLevelNormalizer:
    """
    Default JR/MID/SENIOR level normalizer.
    """

    def normalize(
        self,
        value: Level | str,
    ) -> Level:
        """
        Normalize a Level or string value into a Level enum.
        """

        if isinstance(
            value,
            Level,
        ):
            return value

        normalized_value = (
            str(value)
            .strip()
            .upper()
        )

        return Level(
            normalized_value,
        )