from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.conversation_turn_schema import (
    CONVERSATION_TURN_SCHEMA,
)


class ConversationTurnValidator:
    """
    ConversationTurn validation service.
    """

    @staticmethod
    def validate(
        *,
        turn_id: str,
        conversation_id: str,
        turn_index: int,
        user_message: str,
        assistant_message: str,
        created_at: datetime,
        retrieved_context: str | None,
        model_name: str | None,
        retriever_name: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "turn_id": turn_id,
                "conversation_id": conversation_id,
                "turn_index": turn_index,
                "user_message": user_message,
                "assistant_message": assistant_message,
                "created_at": created_at,
                "retrieved_context": retrieved_context,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "notes": notes,
            },
            schema=CONVERSATION_TURN_SCHEMA,
            error_factory=EvaluationValidationError,
        )