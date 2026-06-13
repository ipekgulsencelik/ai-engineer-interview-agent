from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.enums.drift_severity import (
    DriftSeverity,
)
from src.evaluation.ops.value_objects.drift_alert import (
    DriftAlert,
)


class DriftAlertFactory:
    """
    Creates drift alerts.
    """

    @staticmethod
    def create(
        *,
        baseline_snapshot: (
            ExperimentResultSnapshot
        ),
        current_snapshot: (
            ExperimentResultSnapshot
        ),
        drift_delta: float,
        drift_threshold: float,
        alert_triggered: bool,
        severity: DriftSeverity,
        interpretation: str,
        created_at: datetime | None = None,
        notes: str | None = None,
    ) -> DriftAlert:
        return DriftAlert(
            alert_id=str(uuid4()),
            benchmark_id=(
                current_snapshot.benchmark_id
            ),
            benchmark_name=(
                current_snapshot.benchmark_name
            ),
            benchmark_version=(
                current_snapshot.benchmark_version
            ),
            experiment_id=(
                current_snapshot.experiment_id
            ),
            model_name=(
                current_snapshot.model_name
            ),
            baseline_score=(
                baseline_snapshot.overall_score
            ),
            current_score=(
                current_snapshot.overall_score
            ),
            drift_delta=drift_delta,
            drift_threshold=drift_threshold,
            alert_triggered=alert_triggered,
            severity=severity,
            interpretation=interpretation,
            created_at=(
                created_at
                or datetime.now(UTC)
            ),
            notes=notes,
        )