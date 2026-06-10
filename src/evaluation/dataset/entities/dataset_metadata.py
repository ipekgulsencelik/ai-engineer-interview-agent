from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from src.evaluation.dataset.validators.dataset_metadata_validator import (
    DatasetMetadataValidator,
)


def _empty_extras() -> dict[str, object]:
    return {}


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class DatasetMetadata:
    """
    Dataset provenance metadata snapshot.
    """

    created_at: datetime
    rubric_version: str
    evaluator_version: str
    source: str
    notes: str | None = None
    extras: dict[str, object] = field(default_factory=_empty_extras)

    def __getitem__(self, key: str) -> object:
        if key in self.extras:
            return self.extras[key]
        return getattr(self, key)

    def __post_init__(self) -> None:
        DatasetMetadataValidator.validate(
            created_at=self.created_at,
            rubric_version=self.rubric_version,
            evaluator_version=self.evaluator_version,
            source=self.source,
            notes=self.notes,
        )
