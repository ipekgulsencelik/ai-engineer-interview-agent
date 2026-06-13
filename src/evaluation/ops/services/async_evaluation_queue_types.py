from __future__ import annotations

from collections.abc import Awaitable, Callable

from src.evaluation.ops.entities.queued_evaluation_run import (
    QueuedEvaluationRun,
)


EvaluationRunHandler = Callable[
    [QueuedEvaluationRun],
    Awaitable[None],
]