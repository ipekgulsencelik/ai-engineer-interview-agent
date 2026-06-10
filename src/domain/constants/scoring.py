from __future__ import annotations

from typing import TypeAlias, Final

from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level


Score: TypeAlias = float
LevelRank: TypeAlias = int
DifficultyScoreMap: TypeAlias = dict[Difficulty, Score]


MIN_SCORE: Score = 0.0
MAX_SCORE: Score = 1.0

MIN_NORMALIZED_SCORE: Score = 0.0
MAX_NORMALIZED_SCORE: Score = 1.0

MIN_FINAL_SELECTION_SCORE: Score = 0.0


LEVEL_SCORE_WEIGHT: Score = 0.25
MARKET_SCORE_WEIGHT: Score = 0.20
CV_GAP_SCORE_WEIGHT: Score = 0.20
DIFFICULTY_SCORE_WEIGHT: Score = 0.15
DIVERSITY_SCORE_WEIGHT: Score = 0.15
FATIGUE_SCORE_WEIGHT: Score = 0.05


CV_ALIGNMENT_SCORE_PRECISION: Final[int] = 2


EXACT_LEVEL_MATCH_SCORE: Score = 1.0
ONE_LEVEL_DISTANCE_SCORE: Score = 0.6
TWO_LEVEL_DISTANCE_SCORE: Score = 0.2


LEVEL_RANKS: dict[Level, LevelRank] = {
    Level.JR: 1,
    Level.MID: 2,
    Level.SENIOR: 3,
}


HIGH_PERFORMANCE_THRESHOLD: Score = 8.0
LOW_PERFORMANCE_THRESHOLD: Score = 4.0


DEFAULT_DIFFICULTY_SCORE: Score = 0.7
DEFAULT_FATIGUE_SCORE: Score = 1.0
DEFAULT_ALIGNMENT_SCORE: Final[float] = 0.0


KNOWN_SKILL_GAP_SCORE: Score = 0.2
UNKNOWN_SKILL_GAP_SCORE: Score = 1.0


ASKED_QUESTION_DIVERSITY_SCORE: Score = 0.0
UNASKED_QUESTION_DIVERSITY_SCORE: Score = 1.0


HIGH_PERFORMANCE_DIFFICULTY_SCORES: DifficultyScoreMap = {
    Difficulty.EASY: 0.5,
    Difficulty.MEDIUM: 0.8,
    Difficulty.HARD: 1.0,
}


MID_PERFORMANCE_DIFFICULTY_SCORES: DifficultyScoreMap = {
    Difficulty.EASY: 0.8,
    Difficulty.MEDIUM: 1.0,
    Difficulty.HARD: 0.7,
}


LOW_PERFORMANCE_DIFFICULTY_SCORES: DifficultyScoreMap = {
    Difficulty.EASY: 1.0,
    Difficulty.MEDIUM: 0.6,
    Difficulty.HARD: 0.3,
}


TOTAL_SCORE_WEIGHT: Score = (
    LEVEL_SCORE_WEIGHT
    + MARKET_SCORE_WEIGHT
    + CV_GAP_SCORE_WEIGHT
    + DIFFICULTY_SCORE_WEIGHT
    + DIVERSITY_SCORE_WEIGHT
    + FATIGUE_SCORE_WEIGHT
)