from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.reporting.enums.report_role import (
    ReportRole,
)
from src.evaluation.reporting.validators.report_permission_validator import (
    ReportPermissionValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ReportPermission:
    """
    Immutable report permission.

    Represents access-control rules for report
    artifacts, templates, dashboards, scheduled
    reports, and delivered report outputs.
    """

    permission_id: str

    report_id: str

    principal_id: str

    principal_type: str

    role: ReportRole | None

    action: str

    granted: bool

    created_at: datetime

    created_by: str

    tenant_id: str | None = None

    resource_type: str = "report"

    expires_at: datetime | None = None

    reason: str | None = None

    metadata: dict[
        str,
        str,
    ] | None = None

    def __post_init__(
        self,
    ) -> None:
        ReportPermissionValidator.validate(
            permission_id=self.permission_id,
            report_id=self.report_id,
            principal_id=self.principal_id,
            principal_type=self.principal_type,
            role=self.role,
            action=self.action,
            granted=self.granted,
            created_at=self.created_at,
            created_by=self.created_by,
            tenant_id=self.tenant_id,
            resource_type=self.resource_type,
            expires_at=self.expires_at,
            reason=self.reason,
            metadata=self.metadata,
        )

    @property
    def is_user_permission(
        self,
    ) -> bool:
        return (
            self.principal_type
            == "user"
        )

    @property
    def is_role_permission(
        self,
    ) -> bool:
        return (
            self.principal_type
            == "role"
        )

    @property
    def is_team_permission(
        self,
    ) -> bool:
        return (
            self.principal_type
            == "team"
        )

    @property
    def has_role(
        self,
    ) -> bool:
        return (
            self.role
            is not None
        )

    @property
    def is_owner(
        self,
    ) -> bool:
        return (
            self.role
            == ReportRole.OWNER
        )

    @property
    def is_admin(
        self,
    ) -> bool:
        return (
            self.role
            == ReportRole.ADMIN
        )

    @property
    def is_editor(
        self,
    ) -> bool:
        return (
            self.role
            == ReportRole.EDITOR
        )

    @property
    def is_viewer(
        self,
    ) -> bool:
        return (
            self.role
            == ReportRole.VIEWER
        )

    @property
    def is_auditor(
        self,
    ) -> bool:
        return (
            self.role
            == ReportRole.AUDITOR
        )

    @property
    def is_allow(
        self,
    ) -> bool:
        return self.granted

    @property
    def is_deny(
        self,
    ) -> bool:
        return not self.granted

    @property
    def has_expiration(
        self,
    ) -> bool:
        return (
            self.expires_at
            is not None
        )

    @property
    def has_reason(
        self,
    ) -> bool:
        return (
            self.reason
            is not None
        )

    @property
    def has_metadata(
        self,
    ) -> bool:
        return bool(
            self.metadata,
        )