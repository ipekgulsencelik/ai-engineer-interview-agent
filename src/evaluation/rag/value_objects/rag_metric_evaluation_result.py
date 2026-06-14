from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGMetricEvaluationResult:
    """
    Core generation-side RAG metric scores.
    """

    faithfulness_score: float

    answer_relevance_score: float

    context_precision_score: float

    @property
    def context_relevance_score(
        self,
    ) -> float:
        return self.context_precision_score

    @property
    def answer_correctness_score(
        self,
    ) -> float:
        return self.answer_relevance_score