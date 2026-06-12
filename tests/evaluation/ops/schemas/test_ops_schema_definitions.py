from __future__ import annotations

import importlib
from pathlib import Path


def test_ops_schema_modules_should_define_non_empty_schema_dictionaries() -> None:
    schema_paths = sorted(
        path
        for path in Path("src/evaluation/ops/schemas").glob("*_schema.py")
        if path.name != "__init__.py"
    )

    assert schema_paths
    for path in schema_paths:
        module = importlib.import_module(".".join(path.with_suffix("").parts))
        schema_names = [name for name in dir(module) if name.endswith("_SCHEMA")]
        assert schema_names, f"{module.__name__} should expose a *_SCHEMA constant"
        for schema_name in schema_names:
            schema = getattr(module, schema_name)
            assert isinstance(schema, dict)
            assert schema, f"{schema_name} should not be empty"
            assert all(isinstance(field_name, str) for field_name in schema)


def test_registered_benchmark_schema_should_match_registered_benchmark_contract() -> None:
    from src.evaluation.ops.schemas.registered_benchmark_schema import (
        REGISTERED_BENCHMARK_SCHEMA,
    )

    assert set(REGISTERED_BENCHMARK_SCHEMA) == {
        "benchmark_id",
        "name",
        "version",
        "dataset_id",
        "dataset_version",
        "description",
        "owner",
        "tags",
        "is_active",
        "notes",
    }


def test_evaluation_registry_schema_should_match_registry_contract() -> None:
    from src.evaluation.ops.schemas.evaluation_registry_schema import (
        EVALUATION_REGISTRY_SCHEMA,
    )

    assert set(EVALUATION_REGISTRY_SCHEMA) == {
        "registry_id",
        "registry_name",
        "version",
        "is_locked",
        "notes",
    }
    assert "benchmarks" not in EVALUATION_REGISTRY_SCHEMA


def test_benchmark_history_schema_should_match_history_contract() -> None:
    from src.evaluation.ops.schemas.benchmark_history_schema import (
        BENCHMARK_HISTORY_SCHEMA,
    )

    assert set(BENCHMARK_HISTORY_SCHEMA) == {
        "history_id",
        "benchmark_id",
        "benchmark_version",
        "notes",
    }
    assert "entries" not in BENCHMARK_HISTORY_SCHEMA


def test_leaderboard_entry_schema_should_match_leaderboard_entry_contract() -> None:
    from src.evaluation.ops.schemas.leaderboard_entry_schema import (
        LEADERBOARD_ENTRY_SCHEMA,
    )

    assert set(LEADERBOARD_ENTRY_SCHEMA) == {
        "rank",
        "experiment_id",
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "model_name",
        "overall_score",
        "dataset_id",
        "dataset_version",
        "dataset_hash",
        "metrics_version",
        "interpretation",
        "tags",
        "notes",
    }


def test_quality_gate_result_schema_should_match_quality_gate_contract() -> None:
    from src.evaluation.ops.schemas.quality_gate_result_schema import (
        QUALITY_GATE_RESULT_SCHEMA,
    )

    assert set(QUALITY_GATE_RESULT_SCHEMA) == {
        "gate_name",
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "experiment_id",
        "model_name",
        "metric_name",
        "actual_value",
        "expected_value",
        "passed",
        "severity",
        "interpretation",
        "notes",
    }


def test_regression_detection_result_schema_should_match_regression_contract() -> None:
    from src.evaluation.ops.schemas.regression_detection_result_schema import (
        REGRESSION_DETECTION_RESULT_SCHEMA,
    )

    assert set(REGRESSION_DETECTION_RESULT_SCHEMA) == {
        "benchmark_id",
        "benchmark_name",
        "benchmark_version",
        "baseline_experiment_id",
        "candidate_experiment_id",
        "baseline_score",
        "candidate_score",
        "score_delta",
        "regression_threshold",
        "regression_detected",
        "interpretation",
        "notes",
    }
