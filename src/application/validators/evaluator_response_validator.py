from __future__ import annotations

from src.application.models.llm_response import (
    LLMResponse,
)


class EvaluatorResponseValidator:
    """
    EvaluatorResponseParser input validation kurallarını yönetir.
    """

    @staticmethod
    def validate(
        response: LLMResponse,
    ) -> None:
        if not isinstance(response, LLMResponse):
            raise TypeError(
                "response must be an LLMResponse instance."
            )