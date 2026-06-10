from __future__ import annotations

import random
from collections.abc import Callable, Sequence

from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)


class BootstrapSampleGenerator:
    """
    Generates bootstrap sample results.
    """

    @staticmethod
    def generate(
        *,
        sample_index: int,
        values: Sequence[float],
        statistic_fn: Callable[[tuple[float, ...]], float],
        rng: random.Random,
        seed: int,
    ) -> BootstrapSampleResult:
        sample_values = tuple(
            rng.choice(
                values,
            )
            for _ in range(
                len(values),
            )
        )

        statistic_value = statistic_fn(
            sample_values,
        )

        return BootstrapSampleResult(
            sample_index=sample_index,
            sample_size=len(sample_values),
            statistic_value=statistic_value,
            seed=seed,
        )