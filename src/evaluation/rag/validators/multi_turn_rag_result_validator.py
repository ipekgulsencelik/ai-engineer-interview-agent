from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.multi_turn_rag_result_schema import (
    MULTI_TURN_RAG_RESULT_SCHEMA,
)
from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


class MultiTurnRAGResultValidator:
    """
    MultiTurnRAGResult validation service.
    """

    @staticmethod
    def validate(
        *,
        conversation_id: str,
        turn_results: tuple[
            TurnRAGResult,
            ...,
        ],
        average_faithfulness_score: float,
        average_answer_relevancy_score: float,
        average_context_precision_score: float,
        overall_score: float,
        interpretation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "conversation_id": conversation_id,
                "turn_results": turn_results,
                "average_faithfulness_score": (
                    average_faithfulness_score
                ),
                "average_answer_relevancy_score": (
                    average_answer_relevancy_score
                ),
                "average_context_precision_score": (
                    average_context_precision_score
                ),
                "overall_score": overall_score,
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=MULTI_TURN_RAG_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not turn_results:
            raise EvaluationValidationError(
                "turn_results cannot be empty."
            )

        for index, result in enumerate(
            turn_results,
        ):
            if not isinstance(
                result,
                TurnRAGResult,
            ):
                raise EvaluationValidationError(
                    f"turn_results[{index}] must be TurnRAGResult."
                )