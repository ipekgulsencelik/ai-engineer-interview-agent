from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.evaluation.ops.value_objects.online_evaluation_result import (
    OnlineEvaluationResult,
)


class OnlineEvaluationResultFactory:
    """
    Factory for creating online evaluation results.
    """

    @staticmethod
    def create(
        *,
        request_id: str,
        benchmark_id: str,
        benchmark_name: str,
        model_name: str,
        evaluator_name: str,
        metric_name: str,
        metric_value: float,
        passed: bool,
        latency_ms: float,
        session_id: str | None = None,
        user_id: str | None = None,
        trace_id: str | None = None,
        experiment_id: str | None = None,
        interpretation: str | None = None,
        error_message: str | None = None,
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> OnlineEvaluationResult:
        return OnlineEvaluationResult(
            result_id=str(
                uuid4(),
            ),
            request_id=request_id,
            benchmark_id=benchmark_id,
            benchmark_name=benchmark_name,
            model_name=model_name,
            evaluator_name=evaluator_name,
            metric_name=metric_name,
            metric_value=metric_value,
            passed=passed,
            latency_ms=latency_ms,
            created_at=(
                created_at
                or datetime.now(UTC)
            ),
            session_id=session_id,
            user_id=user_id,
            trace_id=trace_id,
            experiment_id=experiment_id,
            interpretation=interpretation,
            error_message=error_message,
            notes=notes,
        )