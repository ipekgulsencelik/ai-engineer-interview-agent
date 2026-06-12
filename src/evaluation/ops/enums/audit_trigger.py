from __future__ import annotations

from enum import StrEnum


class AuditTrigger(StrEnum):
    SYSTEM = "system"
    USER = "user"
    CI_PIPELINE = "ci_pipeline"
    SCHEDULED_JOB = "scheduled_job"