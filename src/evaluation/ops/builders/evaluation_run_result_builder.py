from __future__ import annotations

from datetime import datetime

from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.evaluation_run_result import (
    EvaluationRunResult,
)


class EvaluationRunResultBuilder:
    """
    Builds EvaluationRunResult instances.
    """

    @staticmethod
    def build(
        *,
        run_id: str,
        snapshot: ExperimentResultSnapshot,
        started_at: datetime,
        completed_at: datetime,
        duration_seconds: float,
        success: bool,
        ci_policy_result: (
            CIBenchmarkPolicyResult
            | None
        ),
        notes: str | None = None,
    ) -> EvaluationRunResult:
        return EvaluationRunResult(
            run_id=run_id,
            experiment_snapshot=snapshot,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration_seconds,
            success=success,
            ci_policy_result=ci_policy_result,
            error_message=None,
            notes=notes,
        )