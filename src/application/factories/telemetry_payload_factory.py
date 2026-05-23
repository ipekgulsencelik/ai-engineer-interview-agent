from __future__ import annotations

from src.application.observability.evaluation_trace import (
    EvaluationTrace,
)
from src.application.observability.interview_trace import (
    InterviewTrace,
)


class TelemetryPayloadFactory:
    """
    Telemetry payload serialization factory.
    """

    @staticmethod
    def build_interview_payload(
        *,
        trace: InterviewTrace,
    ) -> dict[str, object]:
        return {
            "query": trace.query,
            "retrieved_candidates": (
                trace.retrieved_candidates
            ),
            "selected_question_id": (
                trace.selected_question_id
            ),
            "retrieval_latency_seconds": (
                trace.retrieval_latency_seconds
            ),
            "ranking_latency_seconds": (
                trace.ranking_latency_seconds
            ),
            "total_latency_seconds": (
                trace.total_latency_seconds
            ),
        }

    @staticmethod
    def build_evaluation_payload(
        *,
        trace: EvaluationTrace,
    ) -> dict[str, object]:
        return {
            "question_id": (
                trace.question_id
            ),
            "model_name": (
                trace.model_name
            ),
            "tokens_used": (
                trace.tokens_used
            ),
            "latency_seconds": (
                trace.latency_seconds
            ),
            "score": trace.score,
        }