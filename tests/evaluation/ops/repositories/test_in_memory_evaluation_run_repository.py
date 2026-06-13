from __future__ import annotations

from datetime import datetime, timedelta, timezone

from src.evaluation.ops.repositories.in_memory_evaluation_run_repository import (
    InMemoryEvaluationRunRepository,
)
from src.evaluation.ops.value_objects.evaluation_run_result import EvaluationRunResult
from tests.evaluation.ops.factories import experiment_snapshot


def _run_result(
    *,
    run_id: str,
    experiment_id: str,
    benchmark_id: str = "benchmark-1",
    benchmark_version: str = "1.0.0",
    completed_at: datetime,
) -> EvaluationRunResult:
    started_at = completed_at - timedelta(seconds=5)

    return EvaluationRunResult(
        run_id=run_id,
        experiment_snapshot=experiment_snapshot(
            experiment_id=experiment_id,
            benchmark_id=benchmark_id,
            benchmark_version=benchmark_version,
        ),
        started_at=started_at,
        completed_at=completed_at,
        duration_seconds=5.0,
        success=True,
    )


def test_in_memory_evaluation_run_repository_should_save_and_find_by_run_id() -> None:
    repository = InMemoryEvaluationRunRepository()
    result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    repository.save(result=result)

    assert repository.find_by_run_id(run_id="run-1") == result
    assert repository.find_by_run_id(run_id="missing-run") is None


def test_in_memory_evaluation_run_repository_should_replace_existing_run_id() -> None:
    repository = InMemoryEvaluationRunRepository()
    first_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    replacement_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-2",
        completed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    repository.save(result=first_result)
    repository.save(result=replacement_result)

    assert repository.find_by_run_id(run_id="run-1") == replacement_result
    assert repository.list_all() == (replacement_result,)


def test_in_memory_evaluation_run_repository_should_filter_by_experiment_id() -> None:
    repository = InMemoryEvaluationRunRepository()
    matching_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    other_result = _run_result(
        run_id="run-2",
        experiment_id="experiment-2",
        completed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    repository.save(result=matching_result)
    repository.save(result=other_result)

    assert repository.find_by_experiment_id(experiment_id="experiment-1") == (
        matching_result,
    )
    assert repository.find_by_experiment_id(experiment_id="missing") == ()


def test_in_memory_evaluation_run_repository_should_filter_by_benchmark_id() -> None:
    repository = InMemoryEvaluationRunRepository()
    first_matching_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        benchmark_id="benchmark-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    second_matching_result = _run_result(
        run_id="run-2",
        experiment_id="experiment-2",
        benchmark_id="benchmark-1",
        completed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )
    other_result = _run_result(
        run_id="run-3",
        experiment_id="experiment-3",
        benchmark_id="benchmark-2",
        completed_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
    )

    repository.save(result=first_matching_result)
    repository.save(result=second_matching_result)
    repository.save(result=other_result)

    assert repository.find_by_benchmark_id(benchmark_id="benchmark-1") == (
        first_matching_result,
        second_matching_result,
    )
    assert repository.find_by_benchmark_id(benchmark_id="missing") == ()


def test_in_memory_evaluation_run_repository_should_list_recent_by_completed_at() -> (
    None
):
    repository = InMemoryEvaluationRunRepository()
    oldest_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    newest_result = _run_result(
        run_id="run-2",
        experiment_id="experiment-2",
        completed_at=datetime(2026, 1, 3, tzinfo=timezone.utc),
    )
    middle_result = _run_result(
        run_id="run-3",
        experiment_id="experiment-3",
        completed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    repository.save(result=oldest_result)
    repository.save(result=newest_result)
    repository.save(result=middle_result)

    assert repository.list_recent(limit=2) == (newest_result, middle_result)
    assert repository.list_recent(limit=0) == ()


def test_in_memory_evaluation_run_repository_should_list_all_saved_results() -> None:
    repository = InMemoryEvaluationRunRepository()
    first_result = _run_result(
        run_id="run-1",
        experiment_id="experiment-1",
        completed_at=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    second_result = _run_result(
        run_id="run-2",
        experiment_id="experiment-2",
        completed_at=datetime(2026, 1, 2, tzinfo=timezone.utc),
    )

    repository.save(result=first_result)
    repository.save(result=second_result)

    assert repository.list_all() == (first_result, second_result)
