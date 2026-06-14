from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.rag.validators.conversation_turn_validator import (
    ConversationTurnValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ConversationTurn:
    """
    Immutable conversation turn.

    Represents a single user-assistant interaction
    used in conversational RAG evaluation.
    """

    turn_id: str

    conversation_id: str

    turn_index: int

    user_message: str

    assistant_message: str

    created_at: datetime

    retrieved_context: str | None = None

    model_name: str | None = None

    retriever_name: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        ConversationTurnValidator.validate(
            turn_id=self.turn_id,
            conversation_id=self.conversation_id,
            turn_index=self.turn_index,
            user_message=self.user_message,
            assistant_message=self.assistant_message,
            created_at=self.created_at,
            retrieved_context=self.retrieved_context,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            notes=self.notes,
        )

    @property
    def has_retrieved_context(
        self,
    ) -> bool:
        return self.retrieved_context is not None

    @property
    def has_model(
        self,
    ) -> bool:
        return self.model_name is not None

    @property
    def has_retriever(
        self,
    ) -> bool:
        return self.retriever_name is not None