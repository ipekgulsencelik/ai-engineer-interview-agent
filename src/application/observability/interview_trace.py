from __future__ import annotations

from dataclasses import dataclass

from src.application.validators.interview_trace_validator import (
    InterviewTraceValidator,
)


@dataclass(frozen=True)
class InterviewTrace:
    """
    Interview retrieval execution trace.
    """

    query: str

    retrieved_candidates: int

    selected_question_id: str

    retrieval_latency_seconds: float

    ranking_latency_seconds: float

    total_latency_seconds: float

    def __post_init__(
        self,
    ) -> None:
        InterviewTraceValidator.validate(
            self,
        )