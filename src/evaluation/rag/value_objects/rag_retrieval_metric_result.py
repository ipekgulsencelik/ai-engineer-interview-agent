from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGRetrievalMetricResult:
    """
    Retrieval-side RAG metric scores.
    """

    retrieval_precision: float

    retrieval_recall: float