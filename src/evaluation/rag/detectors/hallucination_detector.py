from __future__ import annotations

from src.evaluation.rag.constants.rag_thresholds import (
    MINIMUM_FAITHFULNESS_SCORE,
)


class HallucinationDetector:
    """
    Detects hallucination from faithfulness score.
    """

    @staticmethod
    def detect(
        *,
        faithfulness_score: float,
    ) -> bool:
        return (
            faithfulness_score
            < MINIMUM_FAITHFULNESS_SCORE
        )