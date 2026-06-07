from __future__ import annotations

from collections import Counter

from src.evaluation.dataset.entities.dataset_distribution_snapshot import (
    DatasetDistributionSnapshot,
)
from src.evaluation.dataset.entities.dataset_split import (
    DatasetSplit,
)
from src.evaluation.dataset.entities.evaluation_dataset import (
    EvaluationDataset,
)
from src.evaluation.dataset.validators.dataset_split_coverage_validator import (
    DatasetSplitCoverageValidator,
)


class DatasetDistributionAnalyzer:
    """
    Dataset distribution analyzer.

    Builds distribution snapshots for category, level,
    and split-level observability.
    """

    @classmethod
    def analyze(
        cls,
        *,
        dataset: EvaluationDataset,
        splits: tuple[DatasetSplit, ...] = (),
    ) -> DatasetDistributionSnapshot:
        if splits:
            DatasetSplitCoverageValidator.validate(
                dataset=dataset,
                splits=splits,
            )

        return DatasetDistributionSnapshot(
            dataset_id=dataset.dataset_id,
            sample_count=dataset.sample_count,
            category_distribution=cls._category_distribution(
                dataset=dataset,
            ),
            level_distribution=cls._level_distribution(
                dataset=dataset,
            ),
            split_distribution=cls._split_distribution(
                dataset=dataset,
                splits=splits,
            ),
        )

    @staticmethod
    def _category_distribution(
        *,
        dataset: EvaluationDataset,
    ) -> dict[str, int]:
        return dict(
            Counter(
                sample.category
                for sample in dataset.samples
            )
        )

    @staticmethod
    def _level_distribution(
        *,
        dataset: EvaluationDataset,
    ) -> dict[str, int]:
        return dict(
            Counter(
                sample.level.value
                for sample in dataset.samples
            )
        )

    @staticmethod
    def _split_distribution(
        *,
        dataset: EvaluationDataset,
        splits: tuple[DatasetSplit, ...],
    ) -> dict[str, int]:
        if not splits:
            return {
                "UNSPLIT": dataset.sample_count,
            }

        return {
            split.split_type.value: split.sample_count
            for split in splits
        }