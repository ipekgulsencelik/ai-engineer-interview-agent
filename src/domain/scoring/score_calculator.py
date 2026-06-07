from __future__ import annotations

from dataclasses import dataclass

from src.constants.scoring import (
    CV_GAP_SCORE_WEIGHT,
    DIFFICULTY_SCORE_WEIGHT,
    DIVERSITY_SCORE_WEIGHT,
    FATIGUE_SCORE_WEIGHT,
    LEVEL_SCORE_WEIGHT,
    MARKET_SCORE_WEIGHT,
    MAX_SCORE,
    MIN_SCORE,
    SEMANTIC_SCORE_WEIGHT,
    Score,
)
from src.domain.scoring.calculators.score_calculator_validator import (
    ScoreCalculatorValidator,
)


@dataclass(frozen=True)
class ScoreCalculator:
    """
    Weighted final score hesaplamasını yapan domain calculator.

    Bu sınıf yalnızca ara skorları ağırlıklandırır.
    Policy hesaplamaz, question seçmez, orchestration yapmaz.
    """

    level_weight: Score = LEVEL_SCORE_WEIGHT
    semantic_weight: Score = SEMANTIC_SCORE_WEIGHT
    market_weight: Score = MARKET_SCORE_WEIGHT
    cv_gap_weight: Score = CV_GAP_SCORE_WEIGHT
    difficulty_weight: Score = DIFFICULTY_SCORE_WEIGHT
    diversity_weight: Score = DIVERSITY_SCORE_WEIGHT
    fatigue_weight: Score = FATIGUE_SCORE_WEIGHT

    def __post_init__(self) -> None:
        ScoreCalculatorValidator.validate(self)

    def calculate(
        self,
        *,
        level_score: Score,
        semantic_score: Score,
        market_score: Score,
        cv_gap_score: Score,
        difficulty_score: Score,
        diversity_score: Score,
        fatigue_score: Score,
    ) -> Score:
        """
        Weighted final score üretir.
        """

        ScoreCalculatorValidator.validate_input_scores(
            level_score=level_score,
            semantic_score=semantic_score,
            market_score=market_score,
            cv_gap_score=cv_gap_score,
            difficulty_score=difficulty_score,
            diversity_score=diversity_score,
            fatigue_score=fatigue_score,
        )

        weighted_score = (
            level_score * self.level_weight
            + semantic_score * self.semantic_weight
            + market_score * self.market_weight
            + cv_gap_score * self.cv_gap_weight
            + difficulty_score * self.difficulty_weight
            + diversity_score * self.diversity_weight
            + fatigue_score * self.fatigue_weight
        )

        return self._clamp_score(weighted_score)

    @staticmethod
    def _clamp_score(
        value: Score,
    ) -> Score:
        return min(
            MAX_SCORE,
            max(
                MIN_SCORE,
                float(value),
            ),
        )