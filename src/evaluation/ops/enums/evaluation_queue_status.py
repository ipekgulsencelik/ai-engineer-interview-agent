from __future__ import annotations

from enum import StrEnum


class EvaluationQueueStatus(StrEnum):
    """
    Evaluation queue lifecycle status.
    """

    QUEUED = "queued"

    SCHEDULED = "scheduled"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"
