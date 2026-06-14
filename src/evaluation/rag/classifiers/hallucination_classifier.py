from __future__ import annotations

from src.evaluation.rag.constants.hallucination_thresholds import (
    HIGH_HALLUCINATION_THRESHOLD,
    LOW_HALLUCINATION_THRESHOLD,
    MEDIUM_HALLUCINATION_THRESHOLD,
)
from src.evaluation.rag.enums.hallucination_label import (
    HallucinationLabel,
)


class HallucinationClassifier:
    """
    Classifies hallucination severity.
    """

    @staticmethod
    def classify(
        *,
        hallucination_score: float,
    ) -> HallucinationLabel:
        if hallucination_score <= 0.0:
            return HallucinationLabel.NONE

        if (
            hallucination_score
            < LOW_HALLUCINATION_THRESHOLD
        ):
            return HallucinationLabel.LOW

        if (
            hallucination_score
            < MEDIUM_HALLUCINATION_THRESHOLD
        ):
            return HallucinationLabel.MEDIUM

        if (
            hallucination_score
            < HIGH_HALLUCINATION_THRESHOLD
        ):
            return HallucinationLabel.HIGH

        return HallucinationLabel.CRITICAL