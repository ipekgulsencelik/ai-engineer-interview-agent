from __future__ import annotations

import pytest

from src.evaluation.metrics.interpreters.correlation_interpreter import (
    CorrelationInterpreter,
)


@pytest.mark.parametrize(
    ("coefficient", "expected"),
    [
        (0.95, "very_strong"),
        (-0.71, "strong"),
        (0.51, "moderate"),
        (-0.31, "weak"),
        (0.29, "very_weak"),
    ],
)
def test_correlation_interpreter_should_use_absolute_strength_thresholds(
    coefficient: float,
    expected: str,
) -> None:
    assert (
        CorrelationInterpreter.interpret(
            correlation_coefficient=coefficient,
        )
        == expected
    )
