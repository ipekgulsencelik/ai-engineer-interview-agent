from __future__ import annotations

import pytest

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.metrics.calculators.fleiss_agreement_ratio_calculator import (
    FleissAgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.fleiss_kappa_score_calculator import (
    FleissKappaScoreCalculator,
)


def test_fleiss_kappa_score_calculator_should_return_one_for_perfect_agreement() -> None:
    label_matrix = (
        (
            "pass",
            "pass",
            "pass",
        ),
        (
            "fail",
            "fail",
            "fail",
        ),
    )

    agreement_ratio = FleissAgreementRatioCalculator.calculate(
        label_matrix=label_matrix,
    )

    kappa = FleissKappaScoreCalculator.calculate(
        label_matrix=label_matrix,
        agreement_ratio=agreement_ratio,
    )

    assert kappa == pytest.approx(
        1.0,
    )


def test_fleiss_kappa_score_calculator_should_raise_for_degenerate_labels() -> None:
    label_matrix = (
        (
            "pass",
            "pass",
        ),
        (
            "pass",
            "pass",
        ),
    )

    agreement_ratio = FleissAgreementRatioCalculator.calculate(
        label_matrix=label_matrix,
    )

    with pytest.raises(
        EvaluationValidationError,
        match="Fleiss kappa is undefined",
    ):
        FleissKappaScoreCalculator.calculate(
            label_matrix=label_matrix,
            agreement_ratio=agreement_ratio,
        )