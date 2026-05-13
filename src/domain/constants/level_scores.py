from src.domain.constants.scoring.aliases import (
    LevelRank,
    Score,
)
from src.domain.enums.level import Level

EXACT_LEVEL_MATCH_SCORE: Score = 1.0
ONE_LEVEL_DISTANCE_SCORE: Score = 0.6
TWO_LEVEL_DISTANCE_SCORE: Score = 0.2

LEVEL_RANKS: dict[Level, LevelRank] = {
    Level.JR: 1,
    Level.MID: 2,
    Level.SENIOR: 3,
}