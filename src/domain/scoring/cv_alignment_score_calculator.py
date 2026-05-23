from __future__ import annotations

import math

from src.domain.constants.scoring import (
    CV_ALIGNMENT_SCORE_PRECISION,
    DEFAULT_ALIGNMENT_SCORE,
)


class CVAlignmentScoreCalculator:
    """
    CV alignment score calculator.
    """

    @staticmethod
    def calculate(
        *,
        matched_count: int,
        required_count: int,
    ) -> float:
        if not isinstance(
            matched_count,
            int,
        ):
            raise TypeError(
                "matched_count must be an integer."
            )

        if not isinstance(
            required_count,
            int,
        ):
            raise TypeError(
                "required_count must be an integer."
            )

        if matched_count < 0:
            raise ValueError(
                "matched_count cannot be negative."
            )

        if required_count < 0:
            raise ValueError(
                "required_count cannot be negative."
            )

        if required_count == 0:
            return DEFAULT_ALIGNMENT_SCORE

        score = (
            matched_count
            / required_count
        )

        if not math.isfinite(score):
            raise ValueError(
                "Calculated score must be finite."
            )

        return round(
            score,
            CV_ALIGNMENT_SCORE_PRECISION,
        )