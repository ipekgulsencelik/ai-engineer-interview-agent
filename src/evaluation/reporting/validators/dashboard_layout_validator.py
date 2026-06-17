from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.dashboard_layout_schema import (
    DASHBOARD_LAYOUT_SCHEMA,
)
from src.evaluation.reporting.entities.dashboard_widget import (
    DashboardWidget,
)


class DashboardLayoutValidator:
    """
    DashboardLayout validation service.
    """

    @staticmethod
    def validate(
        *,
        layout_id: str,
        dashboard_id: str,
        title: str,
        widgets: tuple[
            DashboardWidget,
            ...,
        ],
        columns: int,
        row_height: int,
        gap: int,
        compact: bool,
        responsive: bool,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "layout_id": layout_id,
                "dashboard_id": dashboard_id,
                "title": title,
                "widgets": widgets,
                "columns": columns,
                "row_height": row_height,
                "gap": gap,
                "compact": compact,
                "responsive": responsive,
                "metadata": metadata or {},
            },
            schema=DASHBOARD_LAYOUT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if columns > 12:
            raise EvaluationValidationError(
                "columns cannot exceed 12."
            )

        if not widgets:
            raise EvaluationValidationError(
                "widgets cannot be empty."
            )

        widget_ids: set[
            str
        ] = set()

        for index, widget in enumerate(
            widgets,
        ):
            if not isinstance(
                widget,
                DashboardWidget,
            ):
                raise EvaluationValidationError(
                    f"widgets[{index}] must be DashboardWidget."
                )

            if widget.widget_id in widget_ids:
                raise EvaluationValidationError(
                    "widget_id values must be unique."
                )

            widget_ids.add(
                widget.widget_id,
            )

            if widget.width > columns:
                raise EvaluationValidationError(
                    "widget width cannot exceed layout columns."
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