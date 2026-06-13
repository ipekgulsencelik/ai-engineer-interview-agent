from __future__ import annotations

import asyncio
from datetime import datetime, timezone

from src.evaluation.ops.entities.queued_evaluation_run import QueuedEvaluationRun
from src.evaluation.ops.enums.evaluation_queue_status import EvaluationQueueStatus
from src.evaluation.ops.services.async_evaluation_queue import AsyncEvaluationQueue


def _run(*, run_id: str, priority: int) -> QueuedEvaluationRun:
    return QueuedEvaluationRun(
        queue_id=f"queue-{run_id}",
        run_id=run_id,
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id=f"experiment-{run_id}",
        model_name="gpt-5",
        priority=priority,
        status=EvaluationQueueStatus.QUEUED,
        requested_by="ci-pipeline",
        queued_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def test_async_evaluation_queue_should_dequeue_lowest_priority_first() -> None:
    async def scenario() -> None:
        queue = AsyncEvaluationQueue()

        await queue.enqueue(run=_run(run_id="low", priority=10))
        await queue.enqueue(run=_run(run_id="high", priority=1))

        assert queue.size == 2
        assert queue.is_empty is False

        first = await queue.dequeue()
        queue.task_done()
        second = await queue.dequeue()
        queue.task_done()

        assert first.run_id == "high"
        assert second.run_id == "low"
        await queue.wait_until_empty()
        assert queue.is_empty is True

    asyncio.run(scenario())
