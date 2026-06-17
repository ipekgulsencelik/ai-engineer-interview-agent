from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.evaluation.reporting.entities.chart_data import (
    ChartData,
)


class ChartRenderer(ABC):
    """
    Base interface for chart renderers.
    """

    @abstractmethod
    def render(
        self,
        *,
        chart: ChartData,
    ) -> dict[str, object]:
        raise NotImplementedError