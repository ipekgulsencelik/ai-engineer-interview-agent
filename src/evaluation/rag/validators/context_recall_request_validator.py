from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.context_recall_request_schema import (
    CONTEXT_RECALL_REQUEST_SCHEMA,
)


class ContextRecallRequestValidator:
    """
    ContextRecallRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        expected_answer: str,
        expected_context: str,
        retrieved_context: str,
        generated_answer: str | None,
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "expected_answer": expected_answer,
                "expected_context": expected_context,
                "retrieved_context": retrieved_context,
                "generated_answer": generated_answer,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=CONTEXT_RECALL_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            expected_context.strip()
            == retrieved_context.strip()
        ):
            return

        if (
            len(expected_context.strip())
            == 0
        ):
            raise EvaluationValidationError(
                "expected_context cannot be empty."
            )

        if (
            len(retrieved_context.strip())
            == 0
        ):
            raise EvaluationValidationError(
                "retrieved_context cannot be empty."
            )