from __future__ import annotations

from src.domain.constants.scoring import (
    MAX_SCORE,
    MIN_SCORE,
)
from src.domain.entities.question import Question
from src.domain.validators.scoring_policy_input_validator import (
    ScoringPolicyInputValidator,
)
from src.domain.scoring.scoring_context import (
    ScoringContext,
)


class MarketScorePolicy:
    """
    Question market relevance score policy.
    """

    def compute(
        self,
        *,
        question: Question,
        context: ScoringContext,
    ) -> float:
        ScoringPolicyInputValidator.validate(
            question=question,
            context=context,
        )
        
        market_weight = self._normalize_market_weight(
            question.market_weight,
        )

        return self._clamp_score(
            market_weight,
        )

    @staticmethod
    def _normalize_market_weight(
        market_weight: float,
    ) -> float:
        return float(
            market_weight,
        )

    @staticmethod
    def _clamp_score(
        score: float,
    ) -> float:
        return max(
            MIN_SCORE,
            min(
                MAX_SCORE,
                score,
            ),
        )