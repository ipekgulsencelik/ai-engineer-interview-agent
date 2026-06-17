from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.scheduled_report_schema import (
    SCHEDULED_REPORT_SCHEMA,
)


class ScheduledReportValidator:
    """
    ScheduledReport validation service.
    """

    SUPPORTED_REPORT_FORMATS = frozenset(
        {
            "markdown",
            "html",
            "json",
            "pdf",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        schedule_id: str,
        report_id: str,
        report_name: str,
        report_type: str,
        report_format: str,
        cron_expression: str,
        output_directory: str,
        created_at: datetime,
        enabled: bool,
        dashboard_id: str | None,
        experiment_id: str | None,
        run_id: str | None,
        benchmark_id: str | None,
        model_name: str | None,
        generated_by: str | None,
        last_run_at: datetime | None,
        next_run_at: datetime | None,
        execution_count: int,
        failure_count: int,
        last_error: str | None,
        recipient_emails: tuple[
            str,
            ...,
        ],
        metadata: dict[
            str,
            str,
        ] | None,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "schedule_id": schedule_id,
                "report_id": report_id,
                "report_name": report_name,
                "report_type": report_type,
                "report_format": report_format,
                "cron_expression": cron_expression,
                "output_directory": output_directory,
                "created_at": created_at,
                "enabled": enabled,
                "dashboard_id": dashboard_id,
                "experiment_id": experiment_id,
                "run_id": run_id,
                "benchmark_id": benchmark_id,
                "model_name": model_name,
                "generated_by": generated_by,
                "last_run_at": (
                    last_run_at
                    or datetime.min
                ),
                "next_run_at": (
                    next_run_at
                    or datetime.max
                ),
                "execution_count": execution_count,
                "failure_count": failure_count,
                "last_error": last_error,
                "recipient_emails": recipient_emails,
                "metadata": metadata or {},
                "notes": notes,
            },
            schema=SCHEDULED_REPORT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            report_format
            not in cls.SUPPORTED_REPORT_FORMATS
        ):
            raise EvaluationValidationError(
                "report_format must be one of: "
                "markdown, html, json, pdf."
            )

        if failure_count > execution_count:
            raise EvaluationValidationError(
                "failure_count cannot exceed execution_count."
            )

        if (
            last_error is not None
            and failure_count == 0
        ):
            raise EvaluationValidationError(
                "last_error cannot be provided when failure_count is zero."
            )

        if (
            last_run_at is not None
            and next_run_at is not None
            and next_run_at < last_run_at
        ):
            raise EvaluationValidationError(
                "next_run_at cannot be before last_run_at."
            )

        for index, email in enumerate(
            recipient_emails,
        ):
            if (
                not isinstance(
                    email,
                    str,
                )
                or "@"
                not in email
            ):
                raise EvaluationValidationError(
                    f"recipient_emails[{index}] must be a valid email-like string."
                )

        if metadata is not None:
            for key, value in metadata.items():
                if (
                    not isinstance(
                        key,
                        str,
                    )
                    or not key.strip()
                ):
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