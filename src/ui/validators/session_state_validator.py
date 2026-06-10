from __future__ import annotations

from src.ui.schemas.question_response import (
    QuestionResponse,
)


class SessionStateValidator:
    """
    Streamlit session state validation utilities.

    Bu sınıf:
        - session_state içinden gelen object değerlerini validate eder
        - beklenen UI schema tiplerini garanti altına alır
        - state manager sınıfını validation detaylarından izole eder
    """

    @staticmethod
    def validate_question_response(
        *,
        value: object,
    ) -> QuestionResponse:
        if not isinstance(
            value,
            QuestionResponse,
        ):
            raise TypeError(
                "current_question must be a QuestionResponse.",
            )

        return value