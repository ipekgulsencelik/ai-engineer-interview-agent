from __future__ import annotations

from dataclasses import dataclass

from src.domain.validators.evaluation_trace_validator import (
    EvaluationTraceValidator,
)


@dataclass(frozen=True)
class EvaluationTrace:
    """
    LLM evaluation execution trace.
    """

    question_id: str

    model_name: str

    tokens_used: int

    latency_seconds: float

    score: float

    def __post_init__(
        self,
    ) -> None:
        EvaluationTraceValidator.validate(
            self,
        )