from __future__ import annotations

import asyncio

from src.evaluation.ops.entities.queued_evaluation_run import (
    QueuedEvaluationRun,
)


class AsyncEvaluationQueue:
    """
    In-memory async priority queue for evaluation runs.
    """

    def __init__(
        self,
    ) -> None:
        self._queue: asyncio.PriorityQueue[
            tuple[
                int,
                str,
                QueuedEvaluationRun,
            ]
        ] = asyncio.PriorityQueue()

    async def enqueue(
        self,
        *,
        run: QueuedEvaluationRun,
    ) -> None:
        await self._queue.put(
            (
                run.priority,
                run.queued_at.isoformat(),
                run,
            )
        )

    async def dequeue(
        self,
    ) -> QueuedEvaluationRun:
        _, _, run = await self._queue.get()

        return run

    def task_done(
        self,
    ) -> None:
        self._queue.task_done()

    async def wait_until_empty(
        self,
    ) -> None:
        await self._queue.join()

    @property
    def size(
        self,
    ) -> int:
        return self._queue.qsize()

    @property
    def is_empty(
        self,
    ) -> bool:
        return self.size == 0