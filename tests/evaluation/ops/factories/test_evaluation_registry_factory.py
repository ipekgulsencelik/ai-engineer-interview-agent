from __future__ import annotations

from src.evaluation.ops.factories.evaluation_registry_factory import (
    EvaluationRegistryFactory,
)
from tests.evaluation.ops.factories import registered_benchmark


def test_evaluation_registry_factory_should_create_unlocked_registry() -> None:
    benchmark = registered_benchmark()

    registry = EvaluationRegistryFactory.create(
        registry_id="registry-1",
        registry_name="Evaluation Registry",
        version="1.0.0",
        benchmarks=(benchmark,),
        notes="Created by factory.",
    )

    assert registry.registry_id == "registry-1"
    assert registry.benchmarks == (benchmark,)
    assert registry.is_locked is False
    assert registry.updated_at is None
    assert registry.notes == "Created by factory."
