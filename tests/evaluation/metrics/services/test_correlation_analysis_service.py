from __future__ import annotations

from collections.abc import Sequence

from src.evaluation.metrics.services.correlation_analysis_service import (
    CorrelationAnalysisService,
)
from src.evaluation.metrics.value_objects.correlation_result import (
    CorrelationResult,
)


class StubPearsonCalculator:
    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

    def calculate(
        self,
        *,
        metric_x: str,
        metric_y: str,
        x_values: Sequence[float],
        y_values: Sequence[float],
        p_value: float,
    ) -> CorrelationResult:
        self.calls.append(
            {
                "metric_x": metric_x,
                "metric_y": metric_y,
                "x_values": x_values,
                "y_values": y_values,
                "p_value": p_value,
            }
        )
        return CorrelationResult(
            metric_x=metric_x,
            metric_y=metric_y,
            correlation_coefficient=1.0,
            p_value=p_value,
            sample_count=len(x_values),
            method="pearson",
            is_significant=True,
            interpretation="very_strong",
        )


def test_correlation_analysis_service_should_delegate_to_pearson_calculator() -> None:
    calculator = StubPearsonCalculator()
    service = CorrelationAnalysisService(
        pearson_calculator=calculator,  # type: ignore[arg-type]
    )

    result = service.analyze_pearson(
        metric_x="human_score",
        metric_y="llm_score",
        x_values=(1.0, 2.0),
        y_values=(1.0, 2.0),
        p_value=0.01,
    )

    assert result.correlation_coefficient == 1.0
    assert calculator.calls == [
        {
            "metric_x": "human_score",
            "metric_y": "llm_score",
            "x_values": (1.0, 2.0),
            "y_values": (1.0, 2.0),
            "p_value": 0.01,
        }
    ]
