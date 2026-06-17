from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.schemas.report_delivery_result_schema import (
    REPORT_DELIVERY_RESULT_SCHEMA,
)


class ReportDeliveryResultValidator:
    """
    ReportDeliveryResult validation service.
    """

    SUPPORTED_DELIVERY_TYPES = frozenset(
        {
            "email",
            "slack",
            "teams",
            "webhook",
            "s3",
            "gcs",
            "azure_blob",
            "filesystem",
            "mlflow",
            "wandb",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        delivery_id: str,
        report_id: str,
        artifact_id: str,
        delivery_type: str,
        destination: str,
        success: bool,
        delivered_at: datetime,
        provider: str | None,
        status_code: int | None,
        error_message: str | None,
        retry_count: int,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "delivery_id": delivery_id,
                "report_id": report_id,
                "artifact_id": artifact_id,
                "delivery_type": delivery_type,
                "destination": destination,
                "success": success,
                "delivered_at": delivered_at,
                "provider": provider,
                "status_code": status_code,
                "error_message": error_message,
                "retry_count": retry_count,
                "metadata": metadata or {},
            },
            schema=REPORT_DELIVERY_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            delivery_type
            not in cls.SUPPORTED_DELIVERY_TYPES
        ):
            raise EvaluationValidationError(
                "delivery_type must be one of: "
                "email, slack, teams, webhook, s3, gcs, "
                "azure_blob, filesystem, mlflow, wandb."
            )

        if (
            success
            and error_message is not None
        ):
            raise EvaluationValidationError(
                "error_message must be None when success is True."
            )

        if (
            not success
            and error_message is None
        ):
            raise EvaluationValidationError(
                "error_message is required when success is False."
            )

        if (
            status_code is not None
            and status_code < 100
        ):
            raise EvaluationValidationError(
                "status_code must be greater than or equal to 100."
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