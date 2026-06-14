from __future__ import annotations

from enum import StrEnum


class ExperimentRunStatus(
    StrEnum,
):
    """
    Experiment execution lifecycle status.
    """

    PENDING = "pending"

    RUNNING = "running"

    COMPLETED = "completed"

    FAILED = "failed"

    CANCELLED = "cancelled"

    PAUSED = "paused"

    @classmethod
    def terminal_statuses(
        cls,
    ) -> tuple[
        "ExperimentRunStatus",
        ...,
    ]:
        return (
            cls.COMPLETED,
            cls.FAILED,
            cls.CANCELLED,
        )

    @classmethod
    def active_statuses(
        cls,
    ) -> tuple[
        "ExperimentRunStatus",
        ...,
    ]:
        return (
            cls.PENDING,
            cls.RUNNING,
            cls.PAUSED,
        )

    @property
    def is_terminal(
        self,
    ) -> bool:
        return (
            self
            in self.terminal_statuses()
        )

    @property
    def is_active(
        self,
    ) -> bool:
        return (
            self
            in self.active_statuses()
        )