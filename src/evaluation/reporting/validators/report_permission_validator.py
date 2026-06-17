from __future__ import annotations

from datetime import datetime

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.reporting.enums.report_role import (
    ReportRole,
)
from src.evaluation.reporting.schemas.report_permission_schema import (
    REPORT_PERMISSION_SCHEMA,
)


class ReportPermissionValidator:
    """
    ReportPermission validation service.
    """

    SUPPORTED_PRINCIPAL_TYPES = frozenset(
        {
            "user",
            "role",
            "team",
            "service_account",
        }
    )

    SUPPORTED_RESOURCE_TYPES = frozenset(
        {
            "report",
            "dashboard",
            "template",
            "artifact",
            "scheduled_report",
        }
    )

    SUPPORTED_ACTIONS = frozenset(
        {
            "read",
            "write",
            "edit",
            "delete",
            "share",
            "export",
            "schedule",
            "deliver",
            "admin",
            "*",
        }
    )

    @classmethod
    def validate(
        cls,
        *,
        permission_id: str,
        report_id: str,
        principal_id: str,
        principal_type: str,
        role: ReportRole | None,
        action: str,
        granted: bool,
        created_at: datetime,
        created_by: str,
        tenant_id: str | None,
        resource_type: str,
        expires_at: datetime | None,
        reason: str | None,
        metadata: dict[
            str,
            str,
        ] | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "permission_id": permission_id,
                "report_id": report_id,
                "principal_id": principal_id,
                "principal_type": principal_type,
                "role": (
                    None
                    if role is None
                    else str(role)
                ),
                "action": action,
                "granted": granted,
                "created_at": created_at,
                "created_by": created_by,
                "tenant_id": tenant_id,
                "resource_type": resource_type,
                "expires_at": (
                    expires_at
                    or datetime.max
                ),
                "reason": reason,
                "metadata": metadata or {},
            },
            schema=REPORT_PERMISSION_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if (
            role is not None
            and not isinstance(
                role,
                ReportRole,
            )
        ):
            raise EvaluationValidationError(
                "role must be ReportRole."
            )

        if (
            principal_type
            not in cls.SUPPORTED_PRINCIPAL_TYPES
        ):
            raise EvaluationValidationError(
                "principal_type must be one of: "
                "user, role, team, service_account."
            )

        if (
            resource_type
            not in cls.SUPPORTED_RESOURCE_TYPES
        ):
            raise EvaluationValidationError(
                "resource_type must be one of: "
                "report, dashboard, template, artifact, "
                "scheduled_report."
            )

        if action not in cls.SUPPORTED_ACTIONS:
            raise EvaluationValidationError(
                "action must be one of: read, write, edit, "
                "delete, share, export, schedule, deliver, "
                "admin, *."
            )

        if (
            expires_at is not None
            and expires_at <= created_at
        ):
            raise EvaluationValidationError(
                "expires_at must be after created_at."
            )

        if (
            not granted
            and reason is None
        ):
            raise EvaluationValidationError(
                "reason is required when granted is False."
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