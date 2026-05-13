from src.domain.constants.scoring.aliases import (
    DifficultyScoreMap,
)

from src.domain.enums.difficulty import Difficulty

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