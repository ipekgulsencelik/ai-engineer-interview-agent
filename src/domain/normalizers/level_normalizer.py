from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.enums.level import Level


@runtime_checkable
class LevelNormalizer(Protocol):
    def normalize(self, value: Level | str) -> Level:
        """Normalize input level into canonical `Level` enum."""


class DefaultLevelNormalizer:
    def normalize(self, value: Level | str) -> Level:
        if isinstance(value, Level):
            return value

        normalized = value.strip() if isinstance(value, str) else value

        try:
            return Level(normalized)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"Invalid current level: {value}") from exc