from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.enums.dataset_stage import (
    DatasetStage,
)
from src.evaluation.dataset.validators.dataset_version_validator import (
    DatasetVersionValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DatasetVersion:
    """
    Immutable dataset version snapshot.
    """

    version: str
    stage: DatasetStage
    created_by: str
    description: str

    def __post_init__(self) -> None:
        DatasetVersionValidator.validate(
            version=self.version,
            stage=self.stage,
            created_by=self.created_by,
            description=self.description,
        )