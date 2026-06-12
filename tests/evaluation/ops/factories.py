from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.evaluation.metrics.entities.benchmark_history_entry import (
    BenchmarkHistoryEntry,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.metrics.reports.benchmark_evaluation_report import (
    BenchmarkEvaluationReport,
)
from src.evaluation.ops.entities.benchmark_history import BenchmarkHistory
from src.evaluation.ops.entities.evaluation_registry import EvaluationRegistry
from src.evaluation.ops.entities.registered_benchmark import RegisteredBenchmark
from tests.evaluation.metrics.reports.test_benchmark_evaluation_report import (
    _alignment_report,
    _category_snapshot,
)


def benchmark_report(
    *,
    benchmark_id: str = "benchmark-1",
    benchmark_name: str = "AI Engineer Benchmark",
    dataset_id: str = "dataset-1",
    dataset_version: str = "1.0.0",
    model_name: str = "gpt-5",
    overall_score: float = 0.80,
) -> BenchmarkEvaluationReport:
    return BenchmarkEvaluationReport(
        benchmark_id=benchmark_id,
        benchmark_name=benchmark_name,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        model_name=model_name,
        evaluator_id="evaluator-1",
        alignment_report=_alignment_report(),
        category_snapshots=(
            _category_snapshot(
                category="RAG",
                score=overall_score,
            ),
        ),
        overall_score=overall_score,
        interpretation="strong_benchmark",
    )


def experiment_snapshot(
    *,
    experiment_id: str = "experiment-1",
    benchmark_id: str = "benchmark-1",
    benchmark_version: str = "1.0.0",
    dataset_id: str = "dataset-1",
    dataset_version: str = "1.0.0",
    dataset_hash: str = "sha256:abc123",
    model_name: str = "gpt-5",
    overall_score: float = 0.80,
    tags: tuple[str, ...] = ("nightly",),
) -> ExperimentResultSnapshot:
    return ExperimentResultSnapshot(
        experiment_id=experiment_id,
        benchmark_id=benchmark_id,
        benchmark_version=benchmark_version,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        dataset_hash=dataset_hash,
        model_name=model_name,
        metrics_version="1.0.0",
        benchmark_report=benchmark_report(
            benchmark_id=benchmark_id,
            dataset_id=dataset_id,
            dataset_version=dataset_version,
            model_name=model_name,
            overall_score=overall_score,
        ),
        execution_time_seconds=12.5,
        created_at=datetime.now(tz=timezone.utc),
        tags=tags,
        notes="snapshot notes",
    )


def registered_benchmark(
    *,
    benchmark_id: str = "benchmark-1",
    version: str = "1.0.0",
    is_active: bool = True,
) -> RegisteredBenchmark:
    return RegisteredBenchmark(
        benchmark_id=benchmark_id,
        name="AI Engineer Benchmark",
        version=version,
        dataset_id="dataset-1",
        dataset_version="1.0.0",
        description="Benchmark description.",
        owner="ml-platform",
        tags=("nightly",),
        is_active=is_active,
        created_at=datetime.now(tz=timezone.utc),
        notes="registry notes",
    )


def evaluation_registry(
    *,
    benchmarks: tuple[RegisteredBenchmark, ...] = (),
    is_locked: bool = False,
) -> EvaluationRegistry:
    return EvaluationRegistry(
        registry_id="registry-1",
        registry_name="Evaluation Registry",
        version="1.0.0",
        benchmarks=benchmarks,
        created_at=datetime.now(tz=timezone.utc),
        is_locked=is_locked,
        notes="registry notes",
    )


def history_entry(
    *,
    experiment_id: str = "experiment-1",
    benchmark_id: str = "benchmark-1",
    benchmark_version: str = "1.0.0",
    overall_score: float = 0.80,
    recorded_at: datetime | None = None,
) -> BenchmarkHistoryEntry:
    return BenchmarkHistoryEntry(
        experiment_id=experiment_id,
        benchmark_id=benchmark_id,
        benchmark_version=benchmark_version,
        overall_score=overall_score,
        model_name="gpt-5",
        recorded_at=recorded_at or datetime.now(tz=timezone.utc),
        notes="history entry notes",
    )


def benchmark_history(
    *,
    entries: tuple[BenchmarkHistoryEntry, ...] = (),
) -> BenchmarkHistory:
    return BenchmarkHistory(
        history_id="history-1",
        benchmark_id="benchmark-1",
        benchmark_version="1.0.0",
        entries=entries,
        created_at=datetime.now(tz=timezone.utc) - timedelta(days=1),
        updated_at=datetime.now(tz=timezone.utc),
        notes="history notes",
    )
