from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.chart_data_schema import (
    CHART_DATA_SCHEMA,
)


class ChartDataValidator:
    """
    ChartData validation service.
    """

    @staticmethod
    def validate(
        *,
        title: str,
        chart_type: str,
        labels: tuple[
            str,
            ...,
        ],
        scores: tuple[
            float,
            ...,
        ],
        average_score: float | None,
        trend_direction: str | None,
        x_axis_label: str | None,
        y_axis_label: str | None,
        series_name: str | None,
        metric_name: str | None,
        description: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "title": title,
                "chart_type": chart_type,
                "labels": labels,
                "scores": scores,
                "average_score": average_score,
                "trend_direction": trend_direction,
                "x_axis_label": x_axis_label,
                "y_axis_label": y_axis_label,
                "series_name": series_name,
                "metric_name": metric_name,
                "description": description,
                "metadata": metadata or {},
            },
            schema=CHART_DATA_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if chart_type not in {
            "line",
            "bar",
            "pie",
            "scatter",
        }:
            raise EvaluationValidationError(
                "chart_type must be one of: line, bar, pie, scatter."
            )

        if len(labels) != len(scores):
            raise EvaluationValidationError(
                "labels and scores must have the same length."
            )

        if not labels:
            raise EvaluationValidationError(
                "labels cannot be empty."
            )

        if not scores:
            raise EvaluationValidationError(
                "scores cannot be empty."
            )

        for index, label in enumerate(
            labels,
        ):
            if not isinstance(
                label,
                str,
            ) or not label.strip():
                raise EvaluationValidationError(
                    f"labels[{index}] must be a non-empty string."
                )

        for index, score in enumerate(
            scores,
        ):
            if not isinstance(
                score,
                int | float,
            ):
                raise EvaluationValidationError(
                    f"scores[{index}] must be numeric."
                )

        if average_score is not None:
            expected_average = sum(
                scores,
            ) / len(
                scores,
            )

            if abs(
                average_score
                - expected_average
            ) > 1e-6:
                raise EvaluationValidationError(
                    "average_score mismatch."
                )

        if metadata is not None:
            for key, value in metadata.items():
                if not isinstance(
                    key,
                    str,
                ) or not key.strip():
                    raise EvaluationValidationError(
                        "metadata keys must be non-empty strings."
                    )

                if not isinstance(
                    value,
                    str,
                ):
                    raise EvaluationValidationError(
                        "metadata values must be strings."
                    )