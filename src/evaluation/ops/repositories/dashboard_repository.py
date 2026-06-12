from __future__ import annotations

from abc import ABC, abstractmethod

from src.evaluation.ops.entities.production_evaluation_dashboard import (
    ProductionEvaluationDashboard,
)


class DashboardRepository(
    ABC,
):
    """
    Dashboard projection repository.
    """

    @abstractmethod
    def load_dashboard(
        self,
    ) -> (
        ProductionEvaluationDashboard
    ):
        raise NotImplementedError