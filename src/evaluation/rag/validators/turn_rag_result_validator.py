from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.turn_rag_result_schema import (
    TURN_RAG_RESULT_SCHEMA,
)


class TurnRAGResultValidator:
    """
    TurnRAGResult validation service.
    """

    @staticmethod
    def validate(
        *,
        turn_index: int,
        faithfulness_score: float,
        answer_relevancy_score: float,
        context_precision_score: float,
        overall_score: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "turn_index": turn_index,
                "faithfulness_score": faithfulness_score,
                "answer_relevancy_score": (
                    answer_relevancy_score
                ),
                "context_precision_score": (
                    context_precision_score
                ),
                "overall_score": overall_score,
            },
            schema=TURN_RAG_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )