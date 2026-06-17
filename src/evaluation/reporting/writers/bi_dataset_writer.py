from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from collections.abc import Mapping
from typing import Any

from src.evaluation.reporting.entities.bi_dataset import (
    BIDataset,
)


class BIDatasetWriter(
    ABC,
):
    """
    BI dataset writer port.
    """

    @abstractmethod
    def write_dataset(
        self,
        *,
        dataset: BIDataset,
        rows: tuple[
            Mapping[
                str,
                Any,
            ],
            ...,
        ],
    ) -> str:
        """
        Writes rows and returns the storage URI.
        """