from __future__ import annotations

import importlib
from pathlib import Path


def test_metrics_schema_modules_should_define_non_empty_schema_dictionaries() -> None:
    schema_paths = sorted(
        path
        for path in Path("src/evaluation/metrics/schemas").glob("*_schema.py")
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


def test_benchmark_evaluation_report_schema_should_match_report_contract() -> None:
    from src.evaluation.metrics.schemas.benchmark_evaluation_report_schema import (
        BENCHMARK_EVALUATION_REPORT_SCHEMA,
    )

    assert set(BENCHMARK_EVALUATION_REPORT_SCHEMA) == {
        "benchmark_id",
        "benchmark_name",
        "dataset_id",
        "dataset_version",
        "model_name",
        "evaluator_id",
        "overall_score",
        "interpretation",
        "notes",
    }
    assert "benchmark_version" not in BENCHMARK_EVALUATION_REPORT_SCHEMA


def test_experiment_result_snapshot_schema_should_keep_benchmark_version() -> None:
    from src.evaluation.metrics.schemas.experiment_result_snapshot_schema import (
        EXPERIMENT_RESULT_SNAPSHOT_SCHEMA,
    )

    assert "benchmark_version" in EXPERIMENT_RESULT_SNAPSHOT_SCHEMA
    assert "experiment_id" in EXPERIMENT_RESULT_SNAPSHOT_SCHEMA
