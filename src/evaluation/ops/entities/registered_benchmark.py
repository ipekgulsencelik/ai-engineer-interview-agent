from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.validators.registered_benchmark_validator import (
    RegisteredBenchmarkValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RegisteredBenchmark:
    """
    Immutable registered benchmark entity.

    Represents a benchmark definition registered in the
    evaluation system before benchmark execution.
    """

    benchmark_id: str
    name: str
    version: str

    dataset_id: str
    dataset_version: str

    description: str | None = None

    owner: str | None = None

    tags: tuple[str, ...] = ()

    is_active: bool = True

    created_at: datetime | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        RegisteredBenchmarkValidator.validate(
            benchmark_id=self.benchmark_id,
            name=self.name,
            version=self.version,
            dataset_id=self.dataset_id,
            dataset_version=self.dataset_version,
            description=self.description,
            owner=self.owner,
            tags=self.tags,
            is_active=self.is_active,
            created_at=self.created_at,
            notes=self.notes,
        )

    @property
    def identity_key(
        self,
    ) -> str:
        return (
            f"{self.benchmark_id}:{self.version}"
        )

    @property
    def dataset_key(
        self,
    ) -> str:
        return (
            f"{self.dataset_id}:{self.dataset_version}"
        )