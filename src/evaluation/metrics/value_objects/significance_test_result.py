from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.significance_test_result_validator import (
    SignificanceTestResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class SignificanceTestResult:
    """
    Immutable statistical significance test result.

    Represents the output of a statistical hypothesis test
    such as t-test, Mann-Whitney U, Wilcoxon, or chi-square.
    """

    test_name: str

    statistic: float
    p_value: float

    alpha: float

    is_significant: bool

    sample_count: int

    effect_size: float | None = None

    interpretation: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        SignificanceTestResultValidator.validate(
            test_name=self.test_name,
            statistic=self.statistic,
            p_value=self.p_value,
            alpha=self.alpha,
            is_significant=self.is_significant,
            sample_count=self.sample_count,
            effect_size=self.effect_size,
            interpretation=self.interpretation,
            notes=self.notes,
        )

    @property
    def rejects_null_hypothesis(
        self,
    ) -> bool:
        return self.is_significant

    @property
    def retains_null_hypothesis(
        self,
    ) -> bool:
        return not self.is_significant