from __future__ import annotations

import random

import pytest

from src.evaluation.metrics.samplers.bootstrap_sample_generator import (
    BootstrapSampleGenerator,
)
from src.evaluation.metrics.value_objects.bootstrap_sample_result import (
    BootstrapSampleResult,
)


def test_bootstrap_sample_generator_should_generate_deterministic_sample_result() -> (
    None
):
    captured_samples: list[tuple[float, ...]] = []

    def statistic_fn(values: tuple[float, ...]) -> float:
        captured_samples.append(values)
        return sum(values) / len(values)

    result = BootstrapSampleGenerator.generate(
        sample_index=3,
        values=(10.0, 20.0, 30.0),
        statistic_fn=statistic_fn,
        rng=random.Random(42),
        seed=42,
    )

    assert isinstance(result, BootstrapSampleResult)
    assert result.sample_index == 3
    assert result.sample_size == 3
    assert captured_samples == [(30.0, 10.0, 10.0)]
    assert result.statistic_value == pytest.approx(50.0 / 3.0)
    assert result.seed == 42
