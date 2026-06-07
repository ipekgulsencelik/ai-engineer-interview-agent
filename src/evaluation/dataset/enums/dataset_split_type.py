from __future__ import annotations

from enum import Enum


class DatasetSplitType(str, Enum):
    """
    Dataset partition category.

    Defines how evaluation samples are allocated
    across the dataset lifecycle.
    """

    TRAIN = "TRAIN"
    VALIDATION = "VALIDATION"
    TEST = "TEST"

    @classmethod
    def values(
        cls,
    ) -> tuple[str, ...]:
        return tuple(
            member.value
            for member in cls
        )

    @classmethod
    def from_string(
        cls,
        value: str,
    ) -> "DatasetSplitType":
        return cls(
            value.strip().upper(),
        )

    @property
    def is_train(
        self,
    ) -> bool:
        return self is DatasetSplitType.TRAIN

    @property
    def is_validation(
        self,
    ) -> bool:
        return self is DatasetSplitType.VALIDATION

    @property
    def is_test(
        self,
    ) -> bool:
        return self is DatasetSplitType.TEST