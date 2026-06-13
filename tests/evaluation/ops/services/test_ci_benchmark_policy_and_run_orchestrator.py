from __future__ import annotations

from src.evaluation.ops.services.ci_benchmark_policy import CIBenchmarkPolicy
from src.evaluation.ops.services.evaluation_run_orchestrator import (
    EvaluationRunOrchestrator,
)
from tests.evaluation.ops.factories import experiment_snapshot


def test_ci_benchmark_policy_should_build_blocking_failure_for_low_score() -> None:
    result = CIBenchmarkPolicy().evaluate(
        policy_name="release_policy",
        snapshot=experiment_snapshot(overall_score=0.74),
        minimum_required_score=0.80,
        notes="release check",
    )

    assert result.policy_name == "release_policy"
    assert result.deployment_allowed is False
    assert result.blocking_failure_count == 1
    assert result.has_blocking_failures is True
    assert result.failed_gate_count == 1
    assert result.gate_results[0].severity == "critical"
    assert result.notes == "release check"


def test_evaluation_run_orchestrator_should_return_successful_run_without_policy() -> (
    None
):
    snapshot = experiment_snapshot(overall_score=0.83)

    result = EvaluationRunOrchestrator().run(snapshot=snapshot, notes="nightly")

    assert result.experiment_id == snapshot.experiment_id
    assert result.success is True
    assert result.has_ci_policy is False
    assert result.deployment_allowed is None
    assert result.duration_seconds >= 0
    assert result.notes == "nightly"


def test_evaluation_run_orchestrator_should_attach_ci_policy_result() -> None:
    snapshot = experiment_snapshot(overall_score=0.72)

    result = EvaluationRunOrchestrator().run(
        snapshot=snapshot,
        minimum_required_score=0.80,
        policy_name="release_policy",
    )

    assert result.success is False
    assert result.has_ci_policy is True
    assert result.deployment_allowed is False
    assert result.quality_gate_result is not None
    assert result.quality_gate_result.passed is False
    assert result.blocking_failure_count == 1


def test_ci_benchmark_policy_should_accept_injected_policy_collaborators() -> None:
    class SpyInputValidator:
        def __init__(self) -> None:
            self.called = False

        def validate(self, *, snapshot, additional_gate_results) -> None:  # type: ignore[no-untyped-def]
            self.called = True
            assert additional_gate_results == ()

    class SpyBlockingFailureCounter:
        def __init__(self) -> None:
            self.gate_count = 0

        def count(self, *, gate_results) -> int:  # type: ignore[no-untyped-def]
            self.gate_count = len(gate_results)
            return 1

    class SpyPolicyEvaluator:
        def __init__(self) -> None:
            self.blocking_failure_count = -1

        def evaluate(self, *, blocking_failure_count: int) -> bool:
            self.blocking_failure_count = blocking_failure_count
            return False

    input_validator = SpyInputValidator()
    failure_counter = SpyBlockingFailureCounter()
    policy_evaluator = SpyPolicyEvaluator()

    result = CIBenchmarkPolicy(
        input_validator=input_validator,
        blocking_failure_counter=failure_counter,
        policy_evaluator=policy_evaluator,
    ).evaluate(
        policy_name="release_policy",
        snapshot=experiment_snapshot(overall_score=0.70),
        minimum_required_score=0.80,
    )

    assert input_validator.called is True
    assert failure_counter.gate_count == 1
    assert policy_evaluator.blocking_failure_count == 1
    assert result.deployment_allowed is False
    assert result.blocking_failure_count == 1


def test_evaluation_run_orchestrator_should_accept_injected_infrastructure() -> None:
    from datetime import datetime, timezone

    class FixedClock:
        def __init__(self) -> None:
            self._times = iter(
                (
                    datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                    datetime(2026, 1, 1, 0, 0, 5, tzinfo=timezone.utc),
                )
            )

        def now(self) -> datetime:
            return next(self._times)

    class FixedRunIdProvider:
        def generate(self) -> str:
            return "run-fixed"

    result = EvaluationRunOrchestrator(
        run_id_provider=FixedRunIdProvider(),
        clock=FixedClock(),
    ).run(
        snapshot=experiment_snapshot(overall_score=0.83),
        notes="deterministic run",
    )

    assert result.run_id == "run-fixed"
    assert result.started_at == datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    assert result.completed_at == datetime(2026, 1, 1, 0, 0, 5, tzinfo=timezone.utc)
    assert result.duration_seconds == 5.0
    assert result.success is True
    assert result.notes == "deterministic run"
