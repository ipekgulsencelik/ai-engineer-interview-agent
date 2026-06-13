from __future__ import annotations

from src.api.schemas.evaluation.regression_summary_response import (
    RegressionSummaryResponse,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class RegressionSummaryResponseMapper:
    """
    Maps regression detection result.
    """

    @staticmethod
    def map(
        *,
        regression_result: RegressionDetectionResult,
    ) -> RegressionSummaryResponse:
        return RegressionSummaryResponse(
            regression_detected=(
                regression_result.regression_detected
            ),
            score_delta=(
                regression_result.score_delta
            ),
            interpretation=(
                regression_result.interpretation
            ),
        )