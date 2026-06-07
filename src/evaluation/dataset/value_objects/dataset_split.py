from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from src.evaluation.dataset.enums.dataset_split_type import (
    DatasetSplitType,
)
from src.evaluation.dataset.validators.dataset_split_validator import (
    DatasetSplitValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DatasetSplit:
    """
    Immutable dataset split snapshot.

    Represents a logical partition of dataset samples.
    """

    split_type: DatasetSplitType
    sample_ids: tuple[str, ...]

    def __post_init__(self) -> None:
        DatasetSplitValidator.validate(
            split_type=self.split_type,
            sample_ids=self.sample_ids,
        )

    @property
    def sample_count(self) -> int:
        return len(self.sample_ids)

    @cached_property
    def sample_id_set(self) -> frozenset[str]:
        return frozenset(self.sample_ids)

    def contains(
        self,
        *,
        sample_id: str,
    ) -> bool:
        return sample_id in self.sample_id_set