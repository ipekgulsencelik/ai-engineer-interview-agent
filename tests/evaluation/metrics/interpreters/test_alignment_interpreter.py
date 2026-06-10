from __future__ import annotations

from src.evaluation.metrics.interpreters.alignment_interpreter import (
    AlignmentInterpreter,
)


def test_alignment_interpreter_should_return_strong_alignment() -> None:
    assert (
        AlignmentInterpreter.interpret(
            alignment_score=0.85,
        )
        == "strong_alignment"
    )


def test_alignment_interpreter_should_return_moderate_alignment() -> None:
    assert (
        AlignmentInterpreter.interpret(
            alignment_score=0.70,
        )
        == "moderate_alignment"
    )


def test_alignment_interpreter_should_return_weak_alignment() -> None:
    assert (
        AlignmentInterpreter.interpret(
            alignment_score=0.40,
        )
        == "weak_alignment"
    )