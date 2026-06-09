from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.entities.registered_benchmark import (
    RegisteredBenchmark,
)
from src.evaluation.ops.validators.evaluation_registry_validator import (
    EvaluationRegistryValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EvaluationRegistry:
    """
    Immutable evaluation benchmark registry.

    Represents a benchmark registry snapshot used for
    benchmark discovery, governance, and execution planning.
    """

    registry_id: str

    registry_name: str

    version: str

    benchmarks: tuple[
        RegisteredBenchmark,
        ...,
    ]

    created_at: datetime

    updated_at: datetime | None = None

    is_locked: bool = False

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        EvaluationRegistryValidator.validate(
            registry_id=self.registry_id,
            registry_name=self.registry_name,
            version=self.version,
            benchmarks=self.benchmarks,
            created_at=self.created_at,
            updated_at=self.updated_at,
            is_locked=self.is_locked,
            notes=self.notes,
        )

    @property
    def benchmark_count(
        self,
    ) -> int:
        return len(
            self.benchmarks,
        )

    @property
    def active_benchmark_count(
        self,
    ) -> int:
        return sum(
            benchmark.is_active
            for benchmark in self.benchmarks
        )

    @property
    def inactive_benchmark_count(
        self,
    ) -> int:
        return (
            self.benchmark_count
            - self.active_benchmark_count
        )

    @property
    def has_benchmarks(
        self,
    ) -> bool:
        return bool(
            self.benchmarks,
        )

    @property
    def active_benchmarks(
        self,
    ) -> tuple[
        RegisteredBenchmark,
        ...,
    ]:
        return tuple(
            benchmark
            for benchmark in self.benchmarks
            if benchmark.is_active
        )

    @property
    def inactive_benchmarks(
        self,
    ) -> tuple[
        RegisteredBenchmark,
        ...,
    ]:
        return tuple(
            benchmark
            for benchmark in self.benchmarks
            if not benchmark.is_active
        )

    def contains(
        self,
        *,
        benchmark_id: str,
        version: str,
    ) -> bool:
        identity_key = (
            f"{benchmark_id}:{version}"
        )

        return any(
            benchmark.identity_key == identity_key
            for benchmark in self.benchmarks
        )

    def get(
        self,
        *,
        benchmark_id: str,
        version: str,
    ) -> RegisteredBenchmark | None:
        identity_key = (
            f"{benchmark_id}:{version}"
        )

        return next(
            (
                benchmark
                for benchmark in self.benchmarks
                if benchmark.identity_key == identity_key
            ),
            None,
        )