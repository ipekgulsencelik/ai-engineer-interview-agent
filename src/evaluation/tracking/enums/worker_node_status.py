from __future__ import annotations

from enum import StrEnum


class WorkerNodeStatus(
    StrEnum,
):
    """
    Worker node lifecycle status.
    """

    ACTIVE = "active"

    IDLE = "idle"

    DRAINING = "draining"

    OFFLINE = "offline"

    FAILED = "failed"