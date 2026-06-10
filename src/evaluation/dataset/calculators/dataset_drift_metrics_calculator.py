from __future__ import annotations

from src.evaluation.dataset.value_objects.dataset_drift_snapshot import (
    DatasetDriftSnapshot,
)


class DatasetDriftMetricsCalculator:
    """
    Derived dataset drift metric calculator.
    """

    @staticmethod
    def max_category_drift(
        *,
        snapshot: DatasetDriftSnapshot,
    ) -> float:
        return DatasetDriftMetricsCalculator._max_drift(
            drift=snapshot.category_drift,
        )

    @staticmethod
    def max_level_drift(
        *,
        snapshot: DatasetDriftSnapshot,
    ) -> float:
        return DatasetDriftMetricsCalculator._max_drift(
            drift=snapshot.level_drift,
        )

    @staticmethod
    def max_split_drift(
        *,
        snapshot: DatasetDriftSnapshot,
    ) -> float:
        return DatasetDriftMetricsCalculator._max_drift(
            drift=snapshot.split_drift,
        )

    @staticmethod
    def _max_drift(
        *,
        drift: dict[str, float],
    ) -> float:
        if not drift:
            return 0.0

        return max(
            drift.values(),
        )