from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.semantic_similarity_request_schema import (
    SEMANTIC_SIMILARITY_REQUEST_SCHEMA,
)


class SemanticSimilarityRequestValidator:
    """
    SemanticSimilarityRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        reference_text: str,
        candidate_text: str,
        model_name: str | None,
        evaluator_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "reference_text": reference_text,
                "candidate_text": candidate_text,
                "model_name": model_name,
                "evaluator_name": evaluator_name,
                "notes": notes,
            },
            schema=SEMANTIC_SIMILARITY_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )