from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.context_precision_request_schema import (
    CONTEXT_PRECISION_REQUEST_SCHEMA,
)


class ContextPrecisionRequestValidator:
    """
    ContextPrecisionRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        generated_answer: str,
        retrieved_context: str,
        expected_answer: str | None,
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "generated_answer": generated_answer,
                "retrieved_context": retrieved_context,
                "expected_answer": expected_answer,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=CONTEXT_PRECISION_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )