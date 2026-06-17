from __future__ import annotations

from datetime import datetime

from src.evaluation.reporting.entities.report_permission import (
    ReportPermission,
)
from src.evaluation.reporting.enums.report_role import (
    ReportRole,
)
from src.evaluation.reporting.matchers.report_permission_matcher import (
    ReportPermissionMatcher,
)
from src.evaluation.reporting.policies.report_role_action_policy import (
    ReportRoleActionPolicy,
)


class ReportPermissionEvaluator:
    """
    Evaluates report permissions.
    """

    def __init__(
        self,
        *,
        matcher: ReportPermissionMatcher,
        role_action_policy: ReportRoleActionPolicy,
    ) -> None:
        self._matcher = matcher
        self._role_action_policy = role_action_policy

    def matching_permissions(
        self,
        *,
        permissions: tuple[
            ReportPermission,
            ...,
        ],
        principal_id: str,
        principal_roles: tuple[
            str,
            ...,
        ],
        action: str,
        report_id: str,
        tenant_id: str | None,
        resource_type: str,
        now: datetime,
    ) -> tuple[
        ReportPermission,
        ...,
    ]:
        return tuple(
            permission
            for permission in self.base_matching_permissions(
                permissions=permissions,
                principal_id=principal_id,
                principal_roles=principal_roles,
                report_id=report_id,
                tenant_id=tenant_id,
                resource_type=resource_type,
                now=now,
            )
            if self.permission_allows_action(
                permission=permission,
                action=action,
            )
        )

    def base_matching_permissions(
        self,
        *,
        permissions: tuple[
            ReportPermission,
            ...,
        ],
        principal_id: str,
        principal_roles: tuple[
            str,
            ...,
        ],
        report_id: str,
        tenant_id: str | None,
        resource_type: str,
        now: datetime,
    ) -> tuple[
        ReportPermission,
        ...,
    ]:
        return tuple(
            permission
            for permission in permissions
            if self._matcher.base_matches(
                permission=permission,
                principal_id=principal_id,
                principal_roles=principal_roles,
                report_id=report_id,
                tenant_id=tenant_id,
                resource_type=resource_type,
                now=now,
            )
        )

    def permission_allows_action(
        self,
        *,
        permission: ReportPermission,
        action: str,
    ) -> bool:
        actions = self.permission_actions(
            permission=permission,
        )

        return (
            "*"
            in actions
            or action
            in actions
        )

    def permission_actions(
        self,
        *,
        permission: ReportPermission,
    ) -> frozenset[
        str,
    ]:
        return self._role_action_policy.actions_for_permission(
            role=permission.role,
            explicit_action=permission.action,
        )

    def has_role(
        self,
        *,
        permissions: tuple[
            ReportPermission,
            ...,
        ],
        principal_id: str,
        report_id: str,
        role: ReportRole,
        tenant_id: str | None,
        principal_roles: tuple[
            str,
            ...,
        ],
        resource_type: str,
        now: datetime,
    ) -> bool:
        for permission in self.base_matching_permissions(
            permissions=permissions,
            principal_id=principal_id,
            principal_roles=principal_roles,
            report_id=report_id,
            tenant_id=tenant_id,
            resource_type=resource_type,
            now=now,
        ):
            if (
                permission.granted
                and permission.role == role
            ):
                return True

        return False