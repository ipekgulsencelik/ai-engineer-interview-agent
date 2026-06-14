from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.rag.validators.turn_rag_result_validator import (
    TurnRAGResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class TurnRAGResult:
    """
    Immutable turn-level RAG result.
    """

    turn_index: int

    faithfulness_score: float

    answer_relevancy_score: float

    context_precision_score: float

    overall_score: float

    def __post_init__(
        self,
    ) -> None:
        TurnRAGResultValidator.validate(
            turn_index=self.turn_index,
            faithfulness_score=self.faithfulness_score,
            answer_relevancy_score=self.answer_relevancy_score,
            context_precision_score=self.context_precision_score,
            overall_score=self.overall_score,
        )