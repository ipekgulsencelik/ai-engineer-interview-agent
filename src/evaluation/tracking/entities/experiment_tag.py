from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.tracking.validators.experiment_tag_validator import (
    ExperimentTagValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ExperimentTag:
    """
    Immutable experiment tag.

    Represents a searchable metadata tag attached
    to experiments, runs, datasets, benchmarks,
    artifacts, dashboards, and reports.
    """

    tag_id: str

    key: str

    value: str

    created_at: datetime

    description: str | None = None

    created_by: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ExperimentTagValidator.validate(
            tag_id=self.tag_id,
            key=self.key,
            value=self.value,
            created_at=self.created_at,
            description=self.description,
            created_by=self.created_by,
            metadata=self.metadata,
        )

    @property
    def full_name(
        self,
    ) -> str:
        return (
            f"{self.key}"
            f"={self.value}"
        )

    @property
    def has_description(
        self,
    ) -> bool:
        return (
            self.description
            is not None
        )

    @property
    def has_creator(
        self,
    ) -> bool:
        return (
            self.created_by
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def namespace(
        self,
    ) -> str | None:
        """
        Returns namespace portion of key.

        Example:
            model.name -> model
            dataset.version -> dataset
        """

        if "." not in self.key:
            return None

        return self.key.split(
            ".",
            maxsplit=1,
        )[0]

    @property
    def field_name(
        self,
    ) -> str:
        """
        Returns field portion of key.

        Example:
            model.name -> name
            dataset.version -> version
        """

        if "." not in self.key:
            return self.key

        return self.key.split(
            ".",
            maxsplit=1,
        )[1]