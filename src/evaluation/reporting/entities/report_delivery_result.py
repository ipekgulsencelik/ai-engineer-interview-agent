from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.validators.report_delivery_result_validator import (
    ReportDeliveryResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReportDeliveryResult:
    """
    Immutable report delivery result.

    Represents the outcome of delivering a report
    artifact to a destination such as email,
    Slack, Teams, webhook, S3, GCS, MLflow,
    Weights & Biases, or other external systems.
    """

    delivery_id: str

    report_id: str

    artifact_id: str

    delivery_type: str

    destination: str

    success: bool

    delivered_at: datetime

    provider: str | None = None

    status_code: int | None = None

    error_message: str | None = None

    retry_count: int = 0

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ReportDeliveryResultValidator.validate(
            delivery_id=self.delivery_id,
            report_id=self.report_id,
            artifact_id=self.artifact_id,
            delivery_type=self.delivery_type,
            destination=self.destination,
            success=self.success,
            delivered_at=self.delivered_at,
            provider=self.provider,
            status_code=self.status_code,
            error_message=self.error_message,
            retry_count=self.retry_count,
            metadata=self.metadata,
        )

    @property
    def failed(
        self,
    ) -> bool:
        return not self.success

    @property
    def has_provider(
        self,
    ) -> bool:
        return (
            self.provider
            is not None
        )

    @property
    def has_status_code(
        self,
    ) -> bool:
        return (
            self.status_code
            is not None
        )

    @property
    def has_error(
        self,
    ) -> bool:
        return (
            self.error_message
            is not None
        )

    @property
    def was_retried(
        self,
    ) -> bool:
        return (
            self.retry_count > 0
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )

    @property
    def is_email_delivery(
        self,
    ) -> bool:
        return (
            self.delivery_type
            == "email"
        )

    @property
    def is_slack_delivery(
        self,
    ) -> bool:
        return (
            self.delivery_type
            == "slack"
        )

    @property
    def is_webhook_delivery(
        self,
    ) -> bool:
        return (
            self.delivery_type
            == "webhook"
        )

    @property
    def is_storage_delivery(
        self,
    ) -> bool:
        return (
            self.delivery_type
            in {
                "s3",
                "gcs",
                "azure_blob",
                "filesystem",
            }
        )

    @property
    def is_tracking_delivery(
        self,
    ) -> bool:
        return (
            self.delivery_type
            in {
                "mlflow",
                "wandb",
            }
        )

    @property
    def delivery_status(
        self,
    ) -> str:
        return (
            "success"
            if self.success
            else "failed"
        )