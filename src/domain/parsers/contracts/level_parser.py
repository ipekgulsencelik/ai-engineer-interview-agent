from __future__ import annotations

from typing import Protocol

from src.domain.enums.level import Level


class LevelParser(Protocol):
    def parse(
        self,
        value: Level | str,
    ) -> Level:
        ...