from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.enums.level import Level


@runtime_checkable
class LevelParser(Protocol):
    def parse(self, value: Level | str) -> Level:
        """Parse input value into canonical `Level` enum."""