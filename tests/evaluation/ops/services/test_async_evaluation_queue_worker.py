from __future__ import annotations

import asyncio
from datetime import datetime, timezone

import pytest

from src.evaluation.ops.entities.queued_evaluation_run import QueuedEvaluationRun
from src.evaluation.ops.enums.evaluation_queue_status import EvaluationQueueStatus
from src.evaluation.ops.services.async_evaluation_queue import AsyncEvaluationQueue
from src.evaluation.ops.services.async_evaluation_queue_worker import (
    AsyncEvaluationQueueWorker,
)


def _run() -> QueuedEvaluationRun:
    return QueuedEvaluationRun(
        queue_id="queue-1",
        run_id="run-1",
        benchmark_id="benchmark-1",
        benchmark_name="AI Engineer Benchmark",
        benchmark_version="1.0.0",
        experiment_id="experiment-1",
        model_name="gpt-5",
        priority=1,
        status=EvaluationQueueStatus.QUEUED,
        requested_by="ci-pipeline",
        queued_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def test_async_evaluation_queue_worker_should_process_next_run() -> None:
    async def scenario() -> None:
        queue = AsyncEvaluationQueue()
        processed: list[str] = []

        async def handler(run: QueuedEvaluationRun) -> None:
            processed.append(run.run_id)

        await queue.enqueue(run=_run())

        await AsyncEvaluationQueueWorker(queue=queue, handler=handler).process_next()
        await queue.wait_until_empty()

        assert processed == ["run-1"]
        assert queue.is_empty is True

    asyncio.run(scenario())


def test_async_evaluation_queue_worker_should_mark_task_done_when_handler_fails() -> (
    None
):
    async def scenario() -> None:
        queue = AsyncEvaluationQueue()

        async def handler(run: QueuedEvaluationRun) -> None:
            _ = run
            raise RuntimeError("handler failed")

        await queue.enqueue(run=_run())

        with pytest.raises(RuntimeError, match="handler failed"):
            await AsyncEvaluationQueueWorker(
                queue=queue, handler=handler
            ).process_next()

        await queue.wait_until_empty()
        assert queue.is_empty is True

    asyncio.run(scenario())
