from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.faithfulness_evaluation_request_validator import (
    FaithfulnessEvaluationRequestValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class FaithfulnessEvaluationRequest:
    """
    Request model for faithfulness evaluation.

    Represents the inputs required to assess whether
    a generated answer is supported by the retrieved
    context.
    """

    question: str

    generated_answer: str

    retrieved_context: str

    model_name: str | None = None

    evaluator_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        FaithfulnessEvaluationRequestValidator.validate(
            question=self.question,
            generated_answer=self.generated_answer,
            retrieved_context=self.retrieved_context,
            model_name=self.model_name,
            evaluator_name=self.evaluator_name,
            notes=self.notes,
        )