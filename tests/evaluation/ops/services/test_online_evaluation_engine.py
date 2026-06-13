from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.services.online_evaluation_engine import OnlineEvaluationEngine
from src.evaluation.ops.value_objects.online_evaluation_result import (
    OnlineEvaluationResult,
)


def test_online_evaluation_engine_should_build_passed_result() -> None:
    created_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    result = OnlineEvaluationEngine().evaluate(
        request_id="request-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        model_name="gpt-5",
        evaluator_name="rubric-evaluator",
        metric_name="alignment",
        metric_value=0.91,
        minimum_required_value=0.80,
        latency_ms=125.0,
        session_id="session-1",
        user_id="user-1",
        trace_id="trace-1",
        experiment_id="experiment-1",
        created_at=created_at,
        notes="online guardrail",
    )

    assert isinstance(result, OnlineEvaluationResult)
    assert result.passed is True
    assert result.failed is False
    assert result.interpretation == "online_evaluation_passed"
    assert result.has_session is True
    assert result.has_user is True
    assert result.has_trace is True
    assert result.has_experiment is True
    assert result.has_error is False
    assert result.created_at == created_at
    assert result.notes == "online guardrail"


def test_online_evaluation_engine_should_build_failed_result() -> None:
    result = OnlineEvaluationEngine().evaluate(
        request_id="request-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        model_name="gpt-5",
        evaluator_name="rubric-evaluator",
        metric_name="alignment",
        metric_value=0.70,
        minimum_required_value=0.80,
        latency_ms=125.0,
    )

    assert result.passed is False
    assert result.failed is True
    assert result.interpretation == "online_evaluation_failed"
