from __future__ import annotations

from src.domain.scoring.normalized_score_clamper import (
    NormalizedScoreClamper,
)


class MarketScorePolicy:
    """
    Market weight -> normalized market score policy.
    """

    @staticmethod
    def calculate(
        *,
        market_weight: float,
    ) -> float:
        return NormalizedScoreClamper.clamp(
            score=market_weight,
        )