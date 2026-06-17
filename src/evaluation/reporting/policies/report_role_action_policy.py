from __future__ import annotations

from src.evaluation.reporting.enums.report_role import (
    ReportRole,
)


class ReportRoleActionPolicy:
    """
    Defines default report actions by role.
    """

    ALL_ACTIONS = frozenset(
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
        }
    )

    ROLE_ACTIONS: dict[
        ReportRole,
        frozenset[
            str,
        ],
    ] = {
        ReportRole.OWNER: frozenset(
            {
                "*",
            }
        ),
        ReportRole.ADMIN: ALL_ACTIONS,
        ReportRole.EDITOR: frozenset(
            {
                "read",
                "write",
                "edit",
                "export",
            }
        ),
        ReportRole.VIEWER: frozenset(
            {
                "read",
                "export",
            }
        ),
        ReportRole.AUDITOR: frozenset(
            {
                "read",
            }
        ),
    }

    def actions_for_role(
        self,
        *,
        role: ReportRole,
    ) -> frozenset[
        str,
    ]:
        return self.ROLE_ACTIONS.get(
            role,
            frozenset(),
        )

    def actions_for_permission(
        self,
        *,
        role: ReportRole | None,
        explicit_action: str,
    ) -> frozenset[
        str,
    ]:
        actions: set[
            str
        ] = {
            explicit_action,
        }

        if role is not None:
            actions.update(
                self.actions_for_role(
                    role=role,
                )
            )

        return frozenset(
            actions,
        )

    def expand_wildcard(
        self,
        *,
        actions: set[
            str,
        ],
    ) -> set[
        str,
    ]:
        if "*" not in actions:
            return actions

        return set(
            self.ALL_ACTIONS,
        )