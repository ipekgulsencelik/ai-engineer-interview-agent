from __future__ import annotations

from datetime import datetime, timezone

from src.evaluation.ops.entities.evaluation_registry import (
    EvaluationRegistry,
)
from src.evaluation.ops.entities.registered_benchmark import (
    RegisteredBenchmark,
)


class EvaluationRegistryFactory:
    """
    Creates immutable evaluation registry snapshots.
    """

    @staticmethod
    def create(
        *,
        registry_id: str,
        registry_name: str,
        version: str,
        benchmarks: tuple[RegisteredBenchmark, ...] = (),
        notes: str | None = None,
    ) -> EvaluationRegistry:
        return EvaluationRegistry(
            registry_id=registry_id,
            registry_name=registry_name,
            version=version,
            benchmarks=benchmarks,
            created_at=datetime.now(tz=timezone.utc),
            updated_at=None,
            is_locked=False,
            notes=notes,
        )