from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.entities.queued_evaluation_run import QueuedEvaluationRun
from src.evaluation.ops.enums.evaluation_queue_status import EvaluationQueueStatus


def _queued_run(
    *,
    status: EvaluationQueueStatus = EvaluationQueueStatus.QUEUED,
    queued_at: datetime | None = None,
    scheduled_at: datetime | None = None,
    priority: int = 5,
) -> QueuedEvaluationRun:
    return QueuedEvaluationRun(
        queue_id="queue-1",
        run_id="run-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        priority=priority,
        status=status,
        requested_by="ci-pipeline",
        queued_at=queued_at or datetime(2026, 1, 1, tzinfo=timezone.utc),
        scheduled_at=scheduled_at,
        notes="queued evaluation",
    )


def test_queued_evaluation_run_should_expose_queue_state_helpers() -> None:
    run = _queued_run()

    assert run.is_queued is True
    assert run.is_scheduled is False
    assert run.waiting_for_execution is True


def test_scheduled_evaluation_run_should_require_schedule_timestamp() -> None:
    queued_at = datetime(2026, 1, 1, tzinfo=timezone.utc)
    scheduled_at = queued_at + timedelta(minutes=5)

    run = _queued_run(
        status=EvaluationQueueStatus.SCHEDULED,
        queued_at=queued_at,
        scheduled_at=scheduled_at,
    )

    assert run.is_queued is False
    assert run.is_scheduled is True
    assert run.waiting_for_execution is True


def test_queued_evaluation_run_should_reject_schedule_for_plain_queue() -> None:
    queued_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="scheduled_at must be None"):
        _queued_run(
            queued_at=queued_at,
            scheduled_at=queued_at + timedelta(minutes=5),
        )


def test_scheduled_evaluation_run_should_reject_schedule_before_queue_time() -> None:
    queued_at = datetime(2026, 1, 1, tzinfo=timezone.utc)

    with pytest.raises(EvaluationValidationError, match="earlier than queued_at"):
        _queued_run(
            status=EvaluationQueueStatus.SCHEDULED,
            queued_at=queued_at,
            scheduled_at=queued_at - timedelta(seconds=1),
        )
