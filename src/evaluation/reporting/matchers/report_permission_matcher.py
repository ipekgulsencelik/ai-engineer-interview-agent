from __future__ import annotations

from datetime import datetime

from src.evaluation.reporting.entities.report_permission import (
    ReportPermission,
)


class ReportPermissionMatcher:
    """
    Matches report permissions against principal and resource scope.
    """

    def base_matches(
        self,
        *,
        permission: ReportPermission,
        principal_id: str,
        principal_roles: tuple[
            str,
            ...,
        ],
        report_id: str,
        tenant_id: str | None,
        resource_type: str,
        now: datetime,
    ) -> bool:
        return (
            self._matches_scope(
                permission=permission,
                principal_id=principal_id,
                principal_roles=principal_roles,
                report_id=report_id,
                tenant_id=tenant_id,
                resource_type=resource_type,
            )
            and not self._is_expired(
                permission=permission,
                now=now,
            )
        )

    @staticmethod
    def _matches_scope(
        *,
        permission: ReportPermission,
        principal_id: str,
        principal_roles: tuple[
            str,
            ...,
        ],
        report_id: str,
        tenant_id: str | None,
        resource_type: str,
    ) -> bool:
        if permission.report_id != report_id:
            return False

        if permission.resource_type != resource_type:
            return False

        if (
            tenant_id is not None
            and permission.tenant_id is not None
            and permission.tenant_id != tenant_id
        ):
            return False

        if permission.principal_type == "user":
            return permission.principal_id == principal_id

        if permission.principal_type == "role":
            return permission.principal_id in principal_roles

        if permission.principal_type == "team":
            return permission.principal_id in principal_roles

        if permission.principal_type == "service_account":
            return permission.principal_id == principal_id

        return False

    @staticmethod
    def _is_expired(
        *,
        permission: ReportPermission,
        now: datetime,
    ) -> bool:
        return (
            permission.expires_at is not None
            and permission.expires_at <= now
        )