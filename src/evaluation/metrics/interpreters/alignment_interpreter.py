from __future__ import annotations

from src.evaluation.metrics.constants.alignment import (
    MODERATE_ALIGNMENT_INTERPRETATION,
    MODERATE_ALIGNMENT_THRESHOLD,
    STRONG_ALIGNMENT_INTERPRETATION,
    STRONG_ALIGNMENT_THRESHOLD,
    WEAK_ALIGNMENT_INTERPRETATION,
)


class AlignmentInterpreter:
    """
    Alignment strength interpretation service.
    """

    @staticmethod
    def interpret(
        *,
        alignment_score: float,
    ) -> str:
        if alignment_score >= STRONG_ALIGNMENT_THRESHOLD:
            return STRONG_ALIGNMENT_INTERPRETATION

        if alignment_score >= MODERATE_ALIGNMENT_THRESHOLD:
            return MODERATE_ALIGNMENT_INTERPRETATION

        return WEAK_ALIGNMENT_INTERPRETATION