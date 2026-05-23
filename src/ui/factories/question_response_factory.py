from __future__ import annotations

from typing import Any

from src.ui.schemas.question_response import (
    QuestionResponse,
)


class QuestionResponseFactory:
    """
    QuestionResponse factory.

    Bu sınıf:
        - raw API payload'u UI schema modeline dönüştürür
        - payload normalization yapar
        - page katmanını object construction detaylarından izole eder
    """

    @staticmethod
    def create(
        *,
        payload: dict[str, Any],
    ) -> QuestionResponse:
        return QuestionResponse(
            id=str(payload["id"]),
            text=str(payload["text"]),
            category=str(payload["category"]),
            level=str(payload["level"]),
            question_type=str(
                payload["question_type"],
            ),
            difficulty=int(
                payload["difficulty"],
            ),
            final_score=float(
                payload["final_score"],
            ),
        )