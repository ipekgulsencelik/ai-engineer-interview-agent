from __future__ import annotations

import pytest

from src.evaluation.metrics.interpreters.evaluator_alignment_interpreter import (
    EvaluatorAlignmentInterpreter,
)


@pytest.mark.parametrize(
    ("score", "expected"),
    [
        (0.90, "excellent_alignment"),
        (0.75, "high_alignment"),
        (0.50, "moderate_alignment"),
        (0.49, "low_alignment"),
    ],
)
def test_evaluator_alignment_interpreter_should_return_threshold_label(
    score: float,
    expected: str,
) -> None:
    assert EvaluatorAlignmentInterpreter.interpret(score) == expected
