from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.correlation_result_validator import (
    CorrelationResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class CorrelationResult:
    """
    Immutable correlation analysis result.
    """

    metric_x: str
    metric_y: str

    correlation_coefficient: float
    p_value: float
    sample_count: int

    method: str
    is_significant: bool
    interpretation: str | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        CorrelationResultValidator.validate(
            metric_x=self.metric_x,
            metric_y=self.metric_y,
            correlation_coefficient=self.correlation_coefficient,
            p_value=self.p_value,
            sample_count=self.sample_count,
            method=self.method,
            is_significant=self.is_significant,
            interpretation=self.interpretation,
            notes=self.notes,
        )
