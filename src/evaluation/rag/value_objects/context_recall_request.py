from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.context_recall_request_validator import (
    ContextRecallRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContextRecallRequest:
    """
    Request model for context recall evaluation.

    Represents the inputs required to assess whether
    retrieved context covers the expected answer.
    """

    question: str

    expected_answer: str

    expected_context: str

    retrieved_context: str

    generated_answer: str | None = None

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ContextRecallRequestValidator.validate(
            question=self.question,
            expected_answer=self.expected_answer,
            expected_context=self.expected_context,
            retrieved_context=self.retrieved_context,
            generated_answer=self.generated_answer,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )