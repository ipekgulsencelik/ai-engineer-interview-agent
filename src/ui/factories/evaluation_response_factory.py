from __future__ import annotations

from typing import Any

from src.ui.schemas.evaluation_response import (
    EvaluationResponse,
)


class EvaluationResponseFactory:
    """
    EvaluationResponse factory.

    Bu sınıf:
        - raw API payload'u UI schema modeline dönüştürür
        - InterviewPage'i object construction detaylarından izole eder
    """

    @staticmethod
    def create(
        *,
        payload: dict[str, Any],
    ) -> EvaluationResponse:
        return EvaluationResponse(
            **payload,
        )