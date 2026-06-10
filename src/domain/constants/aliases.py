from __future__ import annotations

from typing import TypeAlias

from src.domain.enums.difficulty import Difficulty

Score: TypeAlias = float
DifficultyScoreMap: TypeAlias = dict[Difficulty, Score]
LevelRank: TypeAlias = int