from __future__ import annotations

from src.evaluation.metrics.interpreters.agreement_interpreter import (
    AgreementInterpreter,
)


def test_agreement_interpreter_should_return_very_strong() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=0.95,
        )
        == "very_strong"
    )


def test_agreement_interpreter_should_return_strong() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=0.75,
        )
        == "strong"
    )


def test_agreement_interpreter_should_return_moderate() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=0.55,
        )
        == "moderate"
    )


def test_agreement_interpreter_should_return_weak() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=0.35,
        )
        == "weak"
    )


def test_agreement_interpreter_should_return_very_weak() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=0.10,
        )
        == "very_weak"
    )


def test_agreement_interpreter_should_use_absolute_value() -> None:
    assert (
        AgreementInterpreter.interpret(
            kappa_score=-0.95,
        )
        == "very_strong"
    )