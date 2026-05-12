from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.scoring_weights_validator import (
    ScoringWeightsValidator,
)


@dataclass(frozen=True)
class ScoringWeights:
    """
    Scoring engine içinde kullanılacak ağırlık değerlerini temsil eder.

    Bu model custom_weights dict kullanımının yerine geçer.

    Neden ayrı model?
        - string typo riskini azaltır
        - IDE autocomplete sağlar
        - validation daha net olur
        - domain dili daha explicit hale gelir
    """

    level_weight: float = 1.0
    market_weight: float = 1.0
    cv_gap_weight: float = 1.0
    difficulty_weight: float = 1.0
    diversity_weight: float = 1.0
    fatigue_weight: float = 1.0
    semantic_relevance_weight: float = 1.0

    def __post_init__(self) -> None:
        ScoringWeightsValidator.validate(self)