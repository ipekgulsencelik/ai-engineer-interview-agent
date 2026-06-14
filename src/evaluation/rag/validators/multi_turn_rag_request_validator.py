from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.multi_turn_rag_request_schema import (
    MULTI_TURN_RAG_REQUEST_SCHEMA,
)
from src.evaluation.rag.value_objects.conversation_turn import (
    ConversationTurn,
)


class MultiTurnRAGRequestValidator:
    """
    MultiTurnRAGRequest validation service.
    """

    @staticmethod
    def validate(
        *,
        conversation_id: str,
        turns: tuple[
            ConversationTurn,
            ...,
        ],
        model_name: str | None,
        retriever_name: str | None,
        evaluator_name: str | None,
        expected_answer: str | None,
        expected_conversation_outcome: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "conversation_id": conversation_id,
                "turns": turns,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "expected_answer": expected_answer,
                "expected_conversation_outcome": (
                    expected_conversation_outcome
                ),
                "notes": notes,
            },
            schema=MULTI_TURN_RAG_REQUEST_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not turns:
            raise EvaluationValidationError(
                "turns cannot be empty."
            )

        for index, turn in enumerate(
            turns,
        ):
            if not isinstance(
                turn,
                ConversationTurn,
            ):
                raise EvaluationValidationError(
                    f"turns[{index}] must be ConversationTurn."
                )

        expected_turn_index = 0

        for turn in turns:
            if turn.turn_index != expected_turn_index:
                raise EvaluationValidationError(
                    "turn indices must be sequential."
                )

            expected_turn_index += 1