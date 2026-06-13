from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.entities.experiment_result_snapshot import (
    ExperimentResultSnapshot,
)
from src.evaluation.ops.constants.evaluation_run import (
    CI_POLICY_RESULT_TYPE_ERROR,
    COMPLETED_AT_BEFORE_STARTED_AT_ERROR,
    DURATION_SECONDS_MISMATCH_ERROR,
    EVALUATION_RUN_DURATION_TOLERANCE,
    EXPERIMENT_SNAPSHOT_TYPE_ERROR,
    FAILED_RUN_REQUIRES_ERROR_MESSAGE,
    QUALITY_GATE_RESULT_TYPE_ERROR,
    REGRESSION_RESULT_TYPE_ERROR,
)
from src.evaluation.ops.schemas.evaluation_run_result_schema import (
    EVALUATION_RUN_RESULT_SCHEMA,
)
from src.evaluation.ops.value_objects.ci_benchmark_policy_result import (
    CIBenchmarkPolicyResult,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)
from src.evaluation.ops.value_objects.regression_detection_result import (
    RegressionDetectionResult,
)


class EvaluationRunResultValidator:
    """
    EvaluationRunResult validation service.
    """

    @staticmethod
    def validate(
        *,
        run_id: str,
        experiment_snapshot: ExperimentResultSnapshot,
        started_at: datetime,
        completed_at: datetime,
        duration_seconds: float,
        success: bool,
        regression_result: RegressionDetectionResult | None,
        quality_gate_result: QualityGateResult | None,
        ci_policy_result: CIBenchmarkPolicyResult | None,
        error_message: str | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "run_id": run_id,
                "started_at": started_at,
                "completed_at": completed_at,
                "duration_seconds": (duration_seconds),
                "success": success,
                "error_message": (error_message),
                "notes": notes,
            },
            schema=EVALUATION_RUN_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            experiment_snapshot,
            ExperimentResultSnapshot,
        ):
            raise EvaluationValidationError(EXPERIMENT_SNAPSHOT_TYPE_ERROR)

        if regression_result is not None and not isinstance(
            regression_result,
            RegressionDetectionResult,
        ):
            raise EvaluationValidationError(REGRESSION_RESULT_TYPE_ERROR)

        if quality_gate_result is not None and not isinstance(
            quality_gate_result,
            QualityGateResult,
        ):
            raise EvaluationValidationError(QUALITY_GATE_RESULT_TYPE_ERROR)

        if ci_policy_result is not None and not isinstance(
            ci_policy_result,
            CIBenchmarkPolicyResult,
        ):
            raise EvaluationValidationError(CI_POLICY_RESULT_TYPE_ERROR)

        if completed_at < started_at:
            raise EvaluationValidationError(COMPLETED_AT_BEFORE_STARTED_AT_ERROR)

        calculated_duration = (completed_at - started_at).total_seconds()

        if (
            abs(calculated_duration - duration_seconds)
            > EVALUATION_RUN_DURATION_TOLERANCE
        ):
            raise EvaluationValidationError(DURATION_SECONDS_MISMATCH_ERROR)

        if not success and error_message is None:
            raise EvaluationValidationError(FAILED_RUN_REQUIRES_ERROR_MESSAGE)
