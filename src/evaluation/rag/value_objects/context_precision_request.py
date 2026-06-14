from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.context_precision_request_validator import (
    ContextPrecisionRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ContextPrecisionRequest:
    """
    Request model for context precision evaluation.
    """

    question: str

    generated_answer: str

    retrieved_context: str

    expected_answer: str | None = None

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ContextPrecisionRequestValidator.validate(
            question=self.question,
            generated_answer=self.generated_answer,
            retrieved_context=self.retrieved_context,
            expected_answer=self.expected_answer,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )