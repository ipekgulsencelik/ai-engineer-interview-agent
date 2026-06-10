from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.validators.dataset_drift_snapshot_validator import (
    DatasetDriftSnapshotValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DatasetDriftSnapshot:
    """
    Immutable dataset drift snapshot.

    Captures drift metrics between a baseline dataset
    and a comparison dataset.
    """

    baseline_dataset_id: str
    comparison_dataset_id: str

    sample_count_delta: int

    category_drift: dict[str, float]
    level_drift: dict[str, float]
    split_drift: dict[str, float]

    overall_drift_score: float
    drift_detected: bool

    notes: str | None = None

    def __post_init__(self) -> None:
        DatasetDriftSnapshotValidator.validate(
            baseline_dataset_id=self.baseline_dataset_id,
            comparison_dataset_id=self.comparison_dataset_id,
            sample_count_delta=self.sample_count_delta,
            category_drift=self.category_drift,
            level_drift=self.level_drift,
            split_drift=self.split_drift,
            overall_drift_score=self.overall_drift_score,
            drift_detected=self.drift_detected,
            notes=self.notes,
        )

    @property
    def category_count(self) -> int:
        return len(self.category_drift)

    @property
    def level_count(self) -> int:
        return len(self.level_drift)

    @property
    def split_count(self) -> int:
        return len(self.split_drift)