from __future__ import annotations

from datetime import datetime

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.schemas.experiment_node_schema import (
    EXPERIMENT_NODE_SCHEMA,
)


class ExperimentNodeValidator:
    """
    ExperimentNode validation service.
    """

    @staticmethod
    def validate(
        *,
        experiment_id: str,
        experiment_name: str,
        experiment_version: str,
        parent_experiment_id: str | None,
        dataset_id: str | None,
        dataset_name: str | None,
        dataset_version: str | None,
        benchmark_id: str | None,
        benchmark_name: str | None,
        benchmark_version: str | None,
        model_name: str | None,
        retriever_name: str | None,
        evaluator_name: str | None,
        overall_score: float | None,
        pass_rate: float | None,
        sample_count: int | None,
        passed_count: int | None,
        failed_count: int | None,
        tags: tuple[
            str,
            ...,
        ],
        created_at: datetime,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "experiment_id": experiment_id,
                "experiment_name": experiment_name,
                "experiment_version": experiment_version,
                "parent_experiment_id": (
                    parent_experiment_id
                ),
                "dataset_id": dataset_id,
                "dataset_name": dataset_name,
                "dataset_version": dataset_version,
                "benchmark_id": benchmark_id,
                "benchmark_name": benchmark_name,
                "benchmark_version": benchmark_version,
                "model_name": model_name,
                "retriever_name": retriever_name,
                "evaluator_name": evaluator_name,
                "overall_score": overall_score,
                "pass_rate": pass_rate,
                "sample_count": sample_count,
                "passed_count": passed_count,
                "failed_count": failed_count,
                "tags": tags,
                "created_at": created_at,
                "notes": notes,
            },
            schema=EXPERIMENT_NODE_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            parent_experiment_id
            == experiment_id
        ):
            raise EvaluationValidationError(
                "parent_experiment_id cannot equal experiment_id."
            )

        for index, tag in enumerate(
            tags,
        ):
            if not isinstance(
                tag,
                str,
            ) or not tag.strip():
                raise EvaluationValidationError(
                    f"tags[{index}] must be non-empty string."
                )

        if (
            passed_count is not None
            and failed_count is not None
            and sample_count is not None
            and passed_count + failed_count != sample_count
        ):
            raise EvaluationValidationError(
                "passed_count + failed_count must equal sample_count."
            )