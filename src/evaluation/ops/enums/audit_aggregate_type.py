from __future__ import annotations

from enum import StrEnum


class AuditAggregateType(StrEnum):
    EXPERIMENT = "experiment"
    BENCHMARK = "benchmark"
    EVALUATION_RUN = "evaluation_run"
    CI_POLICY = "ci_policy"