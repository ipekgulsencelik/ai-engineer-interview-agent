from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.answer_relevancy_request_validator import (
    AnswerRelevancyRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AnswerRelevancyRequest:
    """
    Request model for answer relevancy evaluation.

    Represents the inputs required to assess whether
    a generated answer is relevant to the original
    question.
    """

    question: str

    generated_answer: str

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        AnswerRelevancyRequestValidator.validate(
            question=self.question,
            generated_answer=self.generated_answer,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )