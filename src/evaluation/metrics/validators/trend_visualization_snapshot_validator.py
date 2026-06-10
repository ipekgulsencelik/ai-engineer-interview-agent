from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.constants.benchmark_trends import (
    VALID_TREND_DIRECTIONS,
)
from src.evaluation.metrics.schemas.trend_visualization_snapshot_schema import (
    TREND_VISUALIZATION_SNAPSHOT_SCHEMA,
)
from src.evaluation.metrics.value_objects.trend_data_point import (
    TrendDataPoint,
)


class TrendVisualizationSnapshotValidator:
    """
    TrendVisualizationSnapshot validation service.
    """

    @staticmethod
    def validate(
        *,
        title: str,
        description: str,
        trend_direction: str,
        data_points: tuple[TrendDataPoint, ...],
        notes: str | None = None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "title": title,
                "description": description,
                "trend_direction": trend_direction,
                "notes": notes,
            },
            schema=TREND_VISUALIZATION_SNAPSHOT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if trend_direction not in VALID_TREND_DIRECTIONS:
            raise EvaluationValidationError(
                "trend_direction is invalid."
            )

        if not data_points:
            raise EvaluationValidationError(
                "data_points cannot be empty."
            )

        for index, data_point in enumerate(
            data_points,
        ):
            if not isinstance(
                data_point,
                TrendDataPoint,
            ):
                raise EvaluationValidationError(
                    f"data_points[{index}] must be TrendDataPoint."
                )