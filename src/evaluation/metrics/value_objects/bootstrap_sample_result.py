from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.bootstrap_sample_result_validator import (
    BootstrapSampleResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class BootstrapSampleResult:
    """
    Immutable bootstrap sample result.

    Represents a single bootstrap resampling output.
    """

    sample_index: int
    sample_size: int

    statistic_value: float

    seed: int | None = None

    def __post_init__(
        self,
    ) -> None:
        BootstrapSampleResultValidator.validate(
            sample_index=self.sample_index,
            sample_size=self.sample_size,
            statistic_value=self.statistic_value,
            seed=self.seed,
        )