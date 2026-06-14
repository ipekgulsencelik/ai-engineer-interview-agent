from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RAGEvaluationOutcome:
    """
    Final derived RAG evaluation outcome.
    """

    overall_score: float

    hallucination_detected: bool

    passed: bool

    interpretation: str