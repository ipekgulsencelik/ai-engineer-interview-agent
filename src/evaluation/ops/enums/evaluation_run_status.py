from enum import StrEnum


class EvaluationRunStatus(
    StrEnum,
):
    QUEUED = "queued"

    SCHEDULED = "scheduled"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"