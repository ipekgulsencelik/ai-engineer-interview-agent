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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            return self.version == other
        if isinstance(other, DatasetVersion):
            return (
                self.version == other.version
                and self.stage is other.stage
                and self.created_by == other.created_by
                and self.description == other.description
            )
        return NotImplemented

    def __hash__(self) -> int:
        return hash((self.version, self.stage, self.created_by, self.description))

    def __post_init__(self) -> None:
        DatasetVersionValidator.validate(
            version=self.version,
            stage=self.stage,
            created_by=self.created_by,
            description=self.description,
        )