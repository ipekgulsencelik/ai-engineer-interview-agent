from __future__ import annotations

from src.evaluation.ops.entities import (
    BenchmarkHistory,
    EvaluationRegistry,
    RegisteredBenchmark,
)
from src.evaluation.ops.services import (
    BenchmarkHistoryMutationService,
    BenchmarkHistoryQueryService,
    BenchmarkHistoryStore,
    EvaluationRegistryLockService,
    EvaluationRegistryMutationService,
    EvaluationRegistryQueryService,
)
from src.evaluation.ops.value_objects import (
    LeaderboardEntry,
    QualityGateResult,
    RegressionDetectionResult,
)


def test_ops_entities_package_should_export_public_entities() -> None:
    assert BenchmarkHistory.__name__ == "BenchmarkHistory"
    assert EvaluationRegistry.__name__ == "EvaluationRegistry"
    assert RegisteredBenchmark.__name__ == "RegisteredBenchmark"


def test_ops_services_package_should_export_public_services() -> None:
    assert (
        BenchmarkHistoryMutationService.__name__
        == "BenchmarkHistoryMutationService"
    )
    assert BenchmarkHistoryQueryService.__name__ == "BenchmarkHistoryQueryService"
    assert BenchmarkHistoryStore.__name__ == "BenchmarkHistoryStore"
    assert EvaluationRegistryLockService.__name__ == "EvaluationRegistryLockService"
    assert (
        EvaluationRegistryMutationService.__name__
        == "EvaluationRegistryMutationService"
    )
    assert EvaluationRegistryQueryService.__name__ == "EvaluationRegistryQueryService"


def test_ops_value_objects_package_should_export_public_value_objects() -> None:
    assert LeaderboardEntry.__name__ == "LeaderboardEntry"
    assert QualityGateResult.__name__ == "QualityGateResult"
    assert RegressionDetectionResult.__name__ == "RegressionDetectionResult"
