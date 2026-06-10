from __future__ import annotations

from src.evaluation.dataset.value_objects.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.dataset.value_objects.dataset_drift_snapshot import (
    DatasetDriftSnapshot,
)
from src.evaluation.dataset.calculators.distribution_drift_calculator import (
    DistributionDriftCalculator,
)
from src.evaluation.dataset.validators.dataset_drift_input_validator import (
    DatasetDriftInputValidator,
)


class DatasetDriftAnalyzer:
    """
    Dataset drift analyzer.
    """

    @classmethod
    def analyze(
        cls,
        *,
        baseline: DatasetDistributionSnapshot,
        comparison: DatasetDistributionSnapshot,
        drift_threshold: float = 0.10,
        notes: str | None = None,
    ) -> DatasetDriftSnapshot:
        DatasetDriftInputValidator.validate(
            baseline=baseline,
            comparison=comparison,
            drift_threshold=drift_threshold,
        )

        category_drift = DistributionDriftCalculator.calculate(
            baseline_distribution=baseline.category_distribution,
            comparison_distribution=comparison.category_distribution,
        )

        level_drift = DistributionDriftCalculator.calculate(
            baseline_distribution=baseline.level_distribution,
            comparison_distribution=comparison.level_distribution,
        )

        split_drift = DistributionDriftCalculator.calculate(
            baseline_distribution=baseline.split_distribution,
            comparison_distribution=comparison.split_distribution,
        )

        overall_drift_score = cls._calculate_overall_drift_score(
            category_drift=category_drift,
            level_drift=level_drift,
            split_drift=split_drift,
        )

        return DatasetDriftSnapshot(
            baseline_dataset_id=baseline.dataset_id,
            comparison_dataset_id=comparison.dataset_id,
            sample_count_delta=(
                comparison.sample_count
                - baseline.sample_count
            ),
            category_drift=category_drift,
            level_drift=level_drift,
            split_drift=split_drift,
            overall_drift_score=overall_drift_score,
            drift_detected=overall_drift_score >= drift_threshold,
            notes=notes,
        )

    @staticmethod
    def _calculate_overall_drift_score(
        *,
        category_drift: dict[str, float],
        level_drift: dict[str, float],
        split_drift: dict[str, float],
    ) -> float:
        all_scores = (
            tuple(category_drift.values())
            + tuple(level_drift.values())
            + tuple(split_drift.values())
        )

        if not all_scores:
            return 0.0

        return max(all_scores)