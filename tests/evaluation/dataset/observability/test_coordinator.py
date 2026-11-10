"""Dependency inversion and failure isolation at the application boundary."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.evaluation.dataset.observability import (
    DatasetObservabilityCoordinator,
    DatasetObservabilityMonitor,
    MonitoringPolicy,
    MonitoringStatus,
)
from src.evaluation.dataset.quality.models import QualityReport
from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)


class FixedClock:
    def now(self) -> datetime:
        return datetime(2026, 11, 10, tzinfo=UTC)


class StoreSpy:
    def __init__(self, *, fail: bool = False) -> None:
        self.calls = 0
        self.fail = fail

    def save(self, *, snapshot) -> bool:
        self.calls += 1
        if self.fail:
            raise OSError("disk unavailable")
        return True


def _report(run_id: str, *, accepted: bool = True) -> QualityReport:
    return QualityReport(
        run_id=run_id,
        dataset_id="benchmark",
        dataset_version="1.0.0",
        checked_at=datetime(2026, 11, 10, tzinfo=UTC),
        record_count=2,
        total_checks=2,
        passed_checks=2,
        failed_checks=0,
        error_count=0,
        warning_count=0,
        failed_record_count=0,
        pass_rate=1.0,
        accepted=accepted,
        issues=(),
    )


def _distribution() -> DatasetDistributionSnapshot:
    return DatasetDistributionSnapshot(
        dataset_id="benchmark",
        sample_count=2,
        category_distribution={"RAG": 2},
        level_distribution={"MID": 2},
        split_distribution={"UNSPLIT": 2},
    )


def test_coordinator_uses_monitor_and_store_ports() -> None:
    store = StoreSpy()
    monitor = DatasetObservabilityMonitor(
        policy=MonitoringPolicy(),
        clock=FixedClock(),
        id_factory=lambda: "monitoring-run",
    )
    snapshot = DatasetObservabilityCoordinator(
        monitor=monitor, store=store
    ).evaluate_and_store(
        baseline_distribution=_distribution(),
        comparison_distribution=_distribution(),
        baseline_quality=_report("baseline"),
        comparison_quality=_report("comparison"),
    )
    assert store.calls == 1
    assert snapshot.monitor_run_id == "monitoring-run"
    assert snapshot.status is MonitoringStatus.HEALTHY


def test_coordinator_propagates_failed_durable_write() -> None:
    store = StoreSpy(fail=True)
    with pytest.raises(OSError, match="disk unavailable"):
        DatasetObservabilityCoordinator(
            monitor=DatasetObservabilityMonitor(
                clock=FixedClock(), id_factory=lambda: "run"
            ),
            store=store,
        ).evaluate_and_store(
            baseline_distribution=_distribution(),
            comparison_distribution=_distribution(),
            baseline_quality=_report("baseline"),
            comparison_quality=_report("comparison"),
        )
    assert store.calls == 1
