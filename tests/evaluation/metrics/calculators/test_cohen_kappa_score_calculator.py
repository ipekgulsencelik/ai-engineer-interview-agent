from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.agreement_ratio_calculator import (
    AgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.cohens_kappa_score_calculator import (
    CohensKappaScoreCalculator,
)


def test_cohens_kappa_score_calculator_should_return_one_for_perfect_agreement() -> None:
    evaluator_a_labels = (
        "pass",
        "fail",
        "pass",
        "fail",
    )
    evaluator_b_labels = (
        "pass",
        "fail",
        "pass",
        "fail",
    )

    agreement_ratio = AgreementRatioCalculator.calculate(
        evaluator_a_labels=evaluator_a_labels,
        evaluator_b_labels=evaluator_b_labels,
    )

    kappa_score = CohensKappaScoreCalculator.calculate(
        evaluator_a_labels=evaluator_a_labels,
        evaluator_b_labels=evaluator_b_labels,
        agreement_ratio=agreement_ratio,
    )

    assert kappa_score == pytest.approx(1.0)


def test_cohens_kappa_score_calculator_should_return_zero_for_chance_agreement() -> None:
    evaluator_a_labels = (
        "pass",
        "pass",
        "fail",
        "fail",
    )
    evaluator_b_labels = (
        "pass",
        "fail",
        "pass",
        "fail",
    )

    agreement_ratio = AgreementRatioCalculator.calculate(
        evaluator_a_labels=evaluator_a_labels,
        evaluator_b_labels=evaluator_b_labels,
    )

    kappa_score = CohensKappaScoreCalculator.calculate(
        evaluator_a_labels=evaluator_a_labels,
        evaluator_b_labels=evaluator_b_labels,
        agreement_ratio=agreement_ratio,
    )

    assert kappa_score == pytest.approx(0.0)


def test_cohens_kappa_score_calculator_should_raise_for_degenerate_labels() -> None:
    evaluator_a_labels = (
        "pass",
        "pass",
    )
    evaluator_b_labels = (
        "pass",
        "pass",
    )

    agreement_ratio = AgreementRatioCalculator.calculate(
        evaluator_a_labels=evaluator_a_labels,
        evaluator_b_labels=evaluator_b_labels,
    )

    with pytest.raises(
        EvaluationValidationError,
        match="Cohen kappa is undefined",
    ):
        CohensKappaScoreCalculator.calculate(
            evaluator_a_labels=evaluator_a_labels,
            evaluator_b_labels=evaluator_b_labels,
            agreement_ratio=agreement_ratio,
        )