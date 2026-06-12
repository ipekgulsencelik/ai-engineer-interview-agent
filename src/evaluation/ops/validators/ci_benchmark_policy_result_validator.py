from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.ops.schemas.ci_benchmark_policy_result_schema import (
    CI_BENCHMARK_POLICY_RESULT_SCHEMA,
)
from src.evaluation.ops.value_objects.quality_gate_result import (
    QualityGateResult,
)


class CIBenchmarkPolicyResultValidator:
    """
    CIBenchmarkPolicyResult validation service.
    """

    @staticmethod
    def validate(
        *,
        policy_name: str,
        benchmark_id: str,
        benchmark_name: str,
        benchmark_version: str,
        benchmark_score: float,
        minimum_required_score: float,
        experiment_id: str,
        overall_score: float,
        gate_results: tuple[
            QualityGateResult,
            ...,
        ],
        blocking_failure_count: int,
        deployment_allowed: bool,
        interpretation: str,
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "policy_name": policy_name,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "benchmark_score": benchmark_score,
                "minimum_required_score": (
                    minimum_required_score
                ),
                "experiment_id": experiment_id,
                "overall_score": overall_score,
                "blocking_failure_count": (
                    blocking_failure_count
                ),
                "deployment_allowed": (
                    deployment_allowed
                ),
                "interpretation": interpretation,
                "notes": notes,
            },
            schema=CI_BENCHMARK_POLICY_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            gate_results,
            tuple,
        ):
            raise EvaluationValidationError(
                "gate_results must be tuple."
            )

        for index, gate in enumerate(
            gate_results,
        ):
            if not isinstance(
                gate,
                QualityGateResult,
            ):
                raise EvaluationValidationError(
                    f"gate_results[{index}] must be QualityGateResult."
                )

        calculated_failures = sum(
            (
                not gate.passed
                and gate.severity == "critical"
            )
            for gate in gate_results
        )

        if calculated_failures != blocking_failure_count:
            raise EvaluationValidationError(
                "blocking_failure_count mismatch."
            )

        expected_deployment_allowed = (
            benchmark_score >= minimum_required_score
            and calculated_failures == 0
        )

        if deployment_allowed != expected_deployment_allowed:
            raise EvaluationValidationError(
                "deployment_allowed mismatch."
            )