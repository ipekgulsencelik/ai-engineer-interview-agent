from __future__ import annotations

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.builders.evaluation_run_result_builder import (
    EvaluationRunResultBuilder,
)
from src.evaluation.ops.calculators.run_duration_calculator import (
    RunDurationCalculator,
)
from src.evaluation.ops.evaluators.run_success_evaluator import (
    RunSuccessEvaluator,
)
from src.evaluation.ops.providers.run_id_provider import (
    RunIdProvider,
)
from src.evaluation.ops.providers.utc_datetime_provider import (
    UTCDateTimeProvider,
)
from src.evaluation.ops.services.ci_benchmark_policy import (
    CIBenchmarkPolicy,
)
from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class EvaluationRunOrchestrator:
    """
    Evaluation execution orchestrator.
    """

    def __init__(
        self,
        *,
        ci_policy: (
            CIBenchmarkPolicy | None
        ) = None,
    ) -> None:
        self._ci_policy = (
            ci_policy
            or CIBenchmarkPolicy()
        )

    def run(
        self,
        *,
        snapshot: ExperimentResultSnapshot,
        minimum_required_score: (
            float | None
        ) = None,
        policy_name: str = (
            "default_ci_benchmark_policy"
        ),
        notes: str | None = None,
    ) -> EvaluationRunResult:
        started_at = (
            UTCDateTimeProvider.now()
        )

        ci_policy_result = None

        if minimum_required_score is not None:
            ci_policy_result = (
                self._ci_policy.evaluate(
                    policy_name=policy_name,
                    snapshot=snapshot,
                    minimum_required_score=(
                        minimum_required_score
                    ),
                    notes=notes,
                )
            )

        completed_at = (
            UTCDateTimeProvider.now()
        )

        return (
            EvaluationRunResultBuilder.build(
                run_id=RunIdProvider.generate(),
                snapshot=snapshot,
                started_at=started_at,
                completed_at=completed_at,
                duration_seconds=(
                    RunDurationCalculator.calculate(
                        started_at=started_at,
                        completed_at=completed_at,
                    )
                ),
                success=(
                    RunSuccessEvaluator.evaluate(
                        ci_policy_result=(
                            ci_policy_result
                        ),
                    )
                ),
                ci_policy_result=(
                    ci_policy_result
                ),
                notes=notes,
            )
        )