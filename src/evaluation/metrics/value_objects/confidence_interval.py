from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.confidence_interval_validator import (
    ConfidenceIntervalValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ConfidenceInterval:
    """
    Immutable confidence interval value object.

    Represents a statistical confidence interval
    around an estimated metric.
    """

    lower_bound: float

    upper_bound: float

    confidence_level: float

    def __post_init__(
        self,
    ) -> None:
        ConfidenceIntervalValidator.validate(
            lower_bound=self.lower_bound,
            upper_bound=self.upper_bound,
            confidence_level=self.confidence_level,
        )

    @property
    def width(
        self,
    ) -> float:
        return (
            self.upper_bound
            - self.lower_bound
        )

    @property
    def midpoint(
        self,
    ) -> float:
        return (
            self.lower_bound
            + self.upper_bound
        ) / 2

    @property
    def margin_of_error(
        self,
    ) -> float:
        return self.width / 2

    def contains(
        self,
        value: float,
    ) -> bool:
        return (
            self.lower_bound
            <= value
            <= self.upper_bound
        )