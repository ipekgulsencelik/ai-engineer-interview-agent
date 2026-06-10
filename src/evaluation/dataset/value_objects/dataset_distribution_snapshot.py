from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.validators.dataset_distribution_snapshot_validator import (
    DatasetDistributionSnapshotValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DatasetDistributionSnapshot:
    """
    Immutable dataset distribution snapshot.

    Bu value object:
        - category distribution
        - level distribution
        - sample statistics

    bilgilerini temsil eder.
    """

    dataset_id: str
    sample_count: int

    category_distribution: dict[str, int]
    level_distribution: dict[str, int]
    split_distribution: dict[str, int]

    def __post_init__(self) -> None:
        DatasetDistributionSnapshotValidator.validate(
            dataset_id=self.dataset_id,
            sample_count=self.sample_count,
            category_distribution=self.category_distribution,
            level_distribution=self.level_distribution,
            split_distribution=self.split_distribution,
        )

    @property
    def category_count(self) -> int:
        return len(self.category_distribution)

    @property
    def level_count(self) -> int:
        return len(self.level_distribution)

    @property
    def split_count(self) -> int:
        return len(self.split_distribution)