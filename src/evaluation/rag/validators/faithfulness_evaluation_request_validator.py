from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.faithfulness_evaluation_request_schema import (
    FAITHFULNESS_EVALUATION_REQUEST_SCHEMA,
)


class FaithfulnessEvaluationRequestValidator:
    """
    FaithfulnessEvaluationRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        generated_answer: str,
        retrieved_context: str,
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "generated_answer": generated_answer,
                "retrieved_context": retrieved_context,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=FAITHFULNESS_EVALUATION_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )