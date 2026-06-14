from __future__ import annotations

from src.evaluation.ops.enums.dashboard_severity import (
    DashboardSeverity,
)


class CIPolicyDashboardSeverityResolver:
    """
    Resolves dashboard severity for CI policy result cards.
    """

    @staticmethod
    def resolve(
        *,
        deployment_allowed: bool,
    ) -> DashboardSeverity:
        if deployment_allowed:
            return DashboardSeverity.SUCCESS

        return DashboardSeverity.CRITICAL