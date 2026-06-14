from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.multi_turn_rag_request_validator import (
    MultiTurnRAGRequestValidator,
)
from src.evaluation.rag.value_objects.conversation_turn import (
    ConversationTurn,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class MultiTurnRAGRequest:
    """
    Request model for multi-turn RAG evaluation.

    Represents the inputs required to evaluate
    conversational RAG behavior across multiple
    conversation turns.
    """

    conversation_id: str

    turns: tuple[
        ConversationTurn,
        ...,
    ]

    model_name: str | None = None

    retriever_name: str | None = None

    evaluator_name: str | None = None

    expected_answer: str | None = None

    expected_conversation_outcome: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        MultiTurnRAGRequestValidator.validate(
            conversation_id=self.conversation_id,
            turns=self.turns,
            model_name=self.model_name,
            retriever_name=self.retriever_name,
            evaluator_name=self.evaluator_name,
            expected_answer=self.expected_answer,
            expected_conversation_outcome=self.expected_conversation_outcome,
            notes=self.notes,
        )

    @property
    def turn_count(
        self,
    ) -> int:
        return len(
            self.turns,
        )

    @property
    def has_turns(
        self,
    ) -> bool:
        return bool(
            self.turns,
        )