from __future__ import annotations

import random
from collections.abc import Callable, Sequence
from statistics import mean

from src.evaluation.metrics.builders.bootstrap_distribution_summary_builder import (
    BootstrapDistributionSummaryBuilder,
)
from src.evaluation.metrics.constants.bootstrap import (
    DEFAULT_BOOTSTRAP_ITERATIONS,
    DEFAULT_BOOTSTRAP_SEED,
)
from src.evaluation.metrics.samplers.bootstrap_sample_generator import (
    BootstrapSampleGenerator,
)
from src.evaluation.metrics.validators.bootstrap_sampling_input_validator import (
    BootstrapSamplingInputValidator,
)
from src.evaluation.metrics.value_objects.bootstrap_distribution_summary import (
    BootstrapDistributionSummary,
)


class BootstrapSamplingEngine:
    """
    Bootstrap sampling orchestration engine.
    """

    def __init__(
        self,
        *,
        summary_builder: BootstrapDistributionSummaryBuilder | None = None,
    ) -> None:
        self._summary_builder = (
            summary_builder
            or BootstrapDistributionSummaryBuilder()
        )

    def run(
        self,
        *,
        metric_name: str,
        values: Sequence[float],
        statistic_fn: Callable[[tuple[float, ...]], float] = mean,
        bootstrap_iterations: int = DEFAULT_BOOTSTRAP_ITERATIONS,
        seed: int = DEFAULT_BOOTSTRAP_SEED,
        notes: str | None = None,
    ) -> BootstrapDistributionSummary:
        BootstrapSamplingInputValidator.validate(
            values=values,
            bootstrap_iterations=bootstrap_iterations,
        )

        rng = random.Random(seed)

        bootstrap_samples = tuple(
            BootstrapSampleGenerator.generate(
                sample_index=index,
                values=values,
                statistic_fn=statistic_fn,
                rng=rng,
                seed=seed,
            )
            for index in range(bootstrap_iterations)
        )

        return self._summary_builder.build(
            metric_name=metric_name,
            bootstrap_samples=bootstrap_samples,
            notes=notes,
        )