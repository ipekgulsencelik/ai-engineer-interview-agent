from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class OpenTelemetryMetricClient(
    ABC,
):
    """
    OpenTelemetry metric client port.
    """

    @abstractmethod
    def emit_metric(
        self,
        *,
        name: str,
        value: float,
        unit: str,
        attributes: dict[
            str,
            str,
        ],
    ) -> None:
        """
        Emits metric to telemetry backend.
        """
        pass