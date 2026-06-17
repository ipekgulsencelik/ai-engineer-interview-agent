from __future__ import annotations

from typing import Any

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.dashboard_widget_schema import (
    DASHBOARD_WIDGET_SCHEMA,
)


class DashboardWidgetValidator:
    """
    DashboardWidget validation service.
    """

    SUPPORTED_WIDGET_TYPES = frozenset(
        {
            "metric",
            "chart",
            "table",
            "summary",
            "alert",
            "leaderboard",
            "heatmap",
            "distribution",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        widget_id: str,
        title: str,
        widget_type: str,
        data: dict[
            str,
            Any,
        ],
        payload: dict[
            str,
            Any,
        ] | None,
        order: int,
        width: int,
        height: int,
        description: str | None,
        group: str | None,
        refresh_interval_seconds: int | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "widget_id": widget_id,
                "title": title,
                "widget_type": widget_type,
                "data": data,
                "payload": payload or {},
                "order": order,
                "width": width,
                "height": height,
                "description": description,
                "group": group,
                "refresh_interval_seconds": (
                    refresh_interval_seconds
                ),
                "metadata": metadata or {},
            },
            schema=DASHBOARD_WIDGET_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        cls._validate_widget_type(
            widget_type=widget_type,
        )

        cls._validate_dimensions(
            width=width,
            height=height,
        )

        cls._validate_refresh_interval(
            refresh_interval_seconds=(
                refresh_interval_seconds
            ),
        )

        cls._validate_data(
            data=data,
        )

        cls._validate_payload(
            payload=payload,
        )

        cls._validate_metadata(
            metadata=metadata,
        )

    @classmethod
    def _validate_widget_type(
        cls,
        *,
        widget_type: str,
    ) -> None:
        if (
            widget_type
            not in cls.SUPPORTED_WIDGET_TYPES
        ):
            raise EvaluationValidationError(
                "Unsupported widget_type: "
                f"{widget_type}"
            )

    @staticmethod
    def _validate_dimensions(
        *,
        width: int,
        height: int,
    ) -> None:
        if width <= 0:
            raise EvaluationValidationError(
                "width must be greater than zero."
            )

        if height <= 0:
            raise EvaluationValidationError(
                "height must be greater than zero."
            )

        if width > 12:
            raise EvaluationValidationError(
                "width cannot exceed 12."
            )

        if height > 12:
            raise EvaluationValidationError(
                "height cannot exceed 12."
            )

    @staticmethod
    def _validate_refresh_interval(
        *,
        refresh_interval_seconds: int | None,
    ) -> None:
        if (
            refresh_interval_seconds
            is not None
            and refresh_interval_seconds <= 0
        ):
            raise EvaluationValidationError(
                "refresh_interval_seconds "
                "must be greater than zero."
            )

    @staticmethod
    def _validate_data(
        *,
        data: dict[
            str,
            Any,
        ],
    ) -> None:
        if not data:
            raise EvaluationValidationError(
                "data cannot be empty."
            )

    @staticmethod
    def _validate_payload(
        *,
        payload: dict[
            str,
            Any,
        ] | None,
    ) -> None:
        if payload is None:
            return

        if not isinstance(
            payload,
            dict,
        ):
            raise EvaluationValidationError(
                "payload must be a dictionary."
            )

    @staticmethod
    def _validate_metadata(
        *,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        if metadata is None:
            return

        for key, value in metadata.items():
            if (
                not isinstance(
                    key,
                    str,
                )
                or not key.strip()
            ):
                raise EvaluationValidationError(
                    "metadata keys must be "
                    "non-empty strings."
                )

            if not isinstance(
                value,
                str,
            ):
                raise EvaluationValidationError(
                    "metadata values must "
                    "be strings."
                )