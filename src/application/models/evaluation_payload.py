from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class EvaluationPayload:
    """
    Raw evaluator output after JSON parsing, before domain validation.

    Every field is optional because LLM responses may omit or mistype keys;
    EvaluationResultFactory applies defaults and bounds.
    """

    score: float | None = None
    feedback: str | None = None
    technical_accuracy: float | None = None
    depth: float | None = None
    communication: float | None = None
    missing_keywords: tuple[str, ...] = ()
    follow_up_question: str | None = None
    confidence: float | None = None
    rubric_version: str | None = None
