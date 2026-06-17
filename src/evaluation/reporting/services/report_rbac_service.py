from __future__ import annotations

from datetime import UTC
from datetime import datetime

from src.evaluation.reporting.entities.report_permission import (
    ReportPermission,
)
from src.evaluation.reporting.enums.report_role import (
    ReportRole,
)
from src.evaluation.reporting.evaluators.report_permission_evaluator import (
    ReportPermissionEvaluator,
)
from src.evaluation.reporting.policies.report_role_action_policy import (
    ReportRoleActionPolicy,
)


class ReportRBACService:
    """
    Facade service for report role-based access control.
    """

    def __init__(
        self,
        *,
        evaluator: ReportPermissionEvaluator,
        role_action_policy: ReportRoleActionPolicy,
    ) -> None:
        self._evaluator = evaluator
        self._role_action_policy = role_action_policy

    def can(
        self,
        *,
        permissions: tuple[
            ReportPermission,
            ...,
        ],
        principal_id: str,
        action: str,
        report_id: str,
        tenant_id: str | None = None,
        principal_roles: tuple[
            str,
            ...,
        ] = (),
        resource_type: str = "report",
        now: datetime | None = None,
    ) -> bool:
        current_time = now or datetime.now(
            UTC,
        )

        matching_permissions = self._evaluator.matching_permissions(
            permissions=permissions,
            principal_id=principal_id,
            principal_roles=principal_roles,
            action=action,
            report_id=report_id,
            tenant_id=tenant_id,
            resource_type=resource_type,
            now=current_time,
        )

        if any(
            permission.is_deny
            for permission in matching_permissions
        ):
            return False

        return any(
            permission.is_allow
            for permission in matching_permissions
        )

    def allowed_actions(
        self,
        *,
        permissions: tuple[
            ReportPermission,
            ...,
        ],
        principal_id: str,
        report_id: str,
        tenant_id: str | None = None,
        principal_roles: tuple[
            str,
            ...,
        ] = (),
        resource_type: str = "report",
        now: datetime | None = None,
    ) -> tuple[
        str,
        ...,
    ]:
        current_time = now or datetime.now(
            UTC,
        )

        allowed: set[
            str
        ] = set()

        denied: set[
            str
        ] = set()

        for permission in self._evaluator.base_matching_permissions(
            permissions=permissions,
            principal_id=principal_id,
            principal_roles=principal_roles,
            report_id=report_id,
            tenant_id=tenant_id,
            resource_type=resource_type,
            now=current_time,
        ):
            actions = self._evaluator.permission_actions(
                permission=permission,
            )

            if permission.is_deny:
                denied.update(
                    actions,
                )
            else:
                allowed.update(
                    actions,
                )

        if "*" in denied:
            return ()

        allowed = self._role_action_policy.expand_wildcard(
            actions=allowed,
        )

        return tuple(
            sorted(
                allowed - denied,
            )
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
        tenant_id: str | None = None,
        principal_roles: tuple[
            str,
            ...,
        ] = (),
        resource_type: str = "report",
        now: datetime | None = None,
    ) -> bool:
        return self._evaluator.has_role(
            permissions=permissions,
            principal_id=principal_id,
            report_id=report_id,
            role=role,
            tenant_id=tenant_id,
            principal_roles=principal_roles,
            resource_type=resource_type,
            now=now
            or datetime.now(
                UTC,
            ),
        )