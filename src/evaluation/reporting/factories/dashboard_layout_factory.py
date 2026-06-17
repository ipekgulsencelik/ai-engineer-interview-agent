from __future__ import annotations

from uuid import uuid4

from src.evaluation.reporting.entities.dashboard_layout import (
    DashboardLayout,
)
from src.evaluation.reporting.entities.dashboard_widget import (
    DashboardWidget,
)


class DashboardLayoutFactory:
    """
    Factory for creating dashboard layout value objects.
    """

    def create(
        self,
        *,
        dashboard_id: str,
        title: str,
        widgets: tuple[
            DashboardWidget,
            ...,
        ],
        columns: int = 12,
        row_height: int = 120,
        gap: int = 16,
        compact: bool = False,
        responsive: bool = True,
        metadata: dict[
            str,
            str,
        ] | None = None,
    ) -> DashboardLayout:
        return DashboardLayout(
            layout_id=str(
                uuid4(),
            ),
            dashboard_id=dashboard_id,
            title=title,
            widgets=widgets,
            columns=columns,
            row_height=row_height,
            gap=gap,
            compact=compact,
            responsive=responsive,
            metadata=metadata,
        )