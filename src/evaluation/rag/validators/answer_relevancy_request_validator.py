from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.answer_relevancy_request_schema import (
    ANSWER_RELEVANCY_REQUEST_SCHEMA,
)


class AnswerRelevancyRequestValidator:
    """
    AnswerRelevancyRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        question: str,
        generated_answer: str,
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "question": question,
                "generated_answer": generated_answer,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=ANSWER_RELEVANCY_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )