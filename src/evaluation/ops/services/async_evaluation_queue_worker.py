from __future__ import annotations

from src.evaluation.ops.services.async_evaluation_queue import (
    AsyncEvaluationQueue,
)
from src.evaluation.ops.services.async_evaluation_queue_types import (
    EvaluationRunHandler,
)


class AsyncEvaluationQueueWorker:
    """
    Async worker for processing queued evaluation runs.
    """

    def __init__(
        self,
        *,
        queue: AsyncEvaluationQueue,
        handler: EvaluationRunHandler,
    ) -> None:
        self._queue = queue
        self._handler = handler

    async def process_next(
        self,
    ) -> None:
        run = await self._queue.dequeue()

        try:
            await self._handler(
                run,
            )
        finally:
            self._queue.task_done()

    async def run_forever(
        self,
    ) -> None:
        while True:
            await self.process_next()