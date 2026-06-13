from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.enums.drift_severity import (
    DriftSeverity,
)
from src.evaluation.ops.validators.drift_alert_validator import (
    DriftAlertValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DriftAlert:
    """
    Immutable drift alert.

    Represents an operational alert emitted when
    evaluation drift exceeds an accepted threshold.
    """

    alert_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    experiment_id: str

    model_name: str

    baseline_score: float

    current_score: float

    drift_delta: float

    drift_threshold: float

    alert_triggered: bool

    severity: DriftSeverity

    interpretation: str

    created_at: datetime

    acknowledged: bool = False

    acknowledged_by: str | None = None

    acknowledged_at: datetime | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        DriftAlertValidator.validate(
            alert_id=self.alert_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            experiment_id=self.experiment_id,
            model_name=self.model_name,
            baseline_score=self.baseline_score,
            current_score=self.current_score,
            drift_delta=self.drift_delta,
            drift_threshold=self.drift_threshold,
            alert_triggered=self.alert_triggered,
            severity=self.severity,
            interpretation=self.interpretation,
            created_at=self.created_at,
            acknowledged=self.acknowledged,
            acknowledged_by=self.acknowledged_by,
            acknowledged_at=self.acknowledged_at,
            notes=self.notes,
        )

    @property
    def is_acknowledged(
        self,
    ) -> bool:
        return self.acknowledged

    @property
    def requires_attention(
        self,
    ) -> bool:
        return (
            self.alert_triggered
            and not self.acknowledged
        )

    @property
    def drift_magnitude(
        self,
    ) -> float:
        return abs(
            self.drift_delta,
        )

    @property
    def is_regression_drift(
        self,
    ) -> bool:
        return (
            self.drift_delta < 0
        )

    @property
    def is_improvement_drift(
        self,
    ) -> bool:
        return (
            self.drift_delta > 0
        )