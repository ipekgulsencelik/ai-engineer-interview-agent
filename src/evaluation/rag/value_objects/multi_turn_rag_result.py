from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.multi_turn_rag_result_validator import (
    MultiTurnRAGResultValidator,
)
from src.evaluation.rag.value_objects.turn_rag_result import (
    TurnRAGResult,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class MultiTurnRAGResult:
    """
    Immutable multi-turn RAG evaluation result.
    """

    conversation_id: str

    turn_results: tuple[
        TurnRAGResult,
        ...,
    ]

    average_faithfulness_score: float

    average_answer_relevancy_score: float

    average_context_precision_score: float

    overall_score: float

    interpretation: str

    notes: str | None = None

    @property
    def turn_count(
        self,
    ) -> int:
        return len(
            self.turn_results,
        )

    def __post_init__(
        self,
    ) -> None:
        MultiTurnRAGResultValidator.validate(
            conversation_id=self.conversation_id,
            turn_results=self.turn_results,
            average_faithfulness_score=(
                self.average_faithfulness_score
            ),
            average_answer_relevancy_score=(
                self.average_answer_relevancy_score
            ),
            average_context_precision_score=(
                self.average_context_precision_score
            ),
            overall_score=self.overall_score,
            interpretation=self.interpretation,
            notes=self.notes,
        )