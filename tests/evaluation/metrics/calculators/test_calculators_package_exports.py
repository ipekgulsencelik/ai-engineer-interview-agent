from __future__ import annotations

import src.evaluation.metrics.calculators as calculators
from src.evaluation.metrics.calculators.agreement_ratio_calculator import (
    AgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.cohens_kappa_calculator import (
    CohensKappaCalculator,
)
from src.evaluation.metrics.calculators.cohens_kappa_score_calculator import (
    CohensKappaScoreCalculator,
)
from src.evaluation.metrics.calculators.confidence_interval_calculator import (
    ConfidenceIntervalCalculator,
)
from src.evaluation.metrics.calculators.fleiss_agreement_ratio_calculator import (
    FleissAgreementRatioCalculator,
)
from src.evaluation.metrics.calculators.fleiss_kappa_calculator import (
    FleissKappaCalculator,
)
from src.evaluation.metrics.calculators.fleiss_kappa_score_calculator import (
    FleissKappaScoreCalculator,
)
from src.evaluation.metrics.calculators.mae_calculator import (
    MAECalculator,
)
from src.evaluation.metrics.calculators.mse_calculator import (
    MSECalculator,
)
from src.evaluation.metrics.calculators.overall_alignment_score_calculator import (
    OverallAlignmentScoreCalculator,
)
from src.evaluation.metrics.calculators.paired_t_test_calculator import (
    PairedTTestCalculator,
)
from src.evaluation.metrics.calculators.pearson_coefficient_calculator import (
    PearsonCoefficientCalculator,
)
from src.evaluation.metrics.calculators.pearson_correlation_calculator import (
    PearsonCorrelationCalculator,
)
from src.evaluation.metrics.calculators.r2_score_calculator import (
    R2ScoreCalculator,
)
from src.evaluation.metrics.calculators.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)
from src.evaluation.metrics.calculators.rmse_calculator import (
    RMSECalculator,
)


def test_calculators_package_should_export_public_calculator_classes() -> None:
    assert calculators.__all__ == [
        "AgreementRatioCalculator",
        "CohensKappaScoreCalculator",
        "CohensKappaCalculator",
        "ConfidenceIntervalCalculator",
        "FleissAgreementRatioCalculator",
        "FleissKappaCalculator",
        "FleissKappaScoreCalculator",
        "MAECalculator",
        "MSECalculator",
        "OverallAlignmentScoreCalculator",
        "PairedTTestCalculator",
        "PearsonCoefficientCalculator",
        "PearsonCorrelationCalculator",
        "R2ScoreCalculator",
        "RegressionMetricsCalculator",
        "RMSECalculator",
    ]
    assert calculators.AgreementRatioCalculator is AgreementRatioCalculator
    assert calculators.CohensKappaScoreCalculator is CohensKappaScoreCalculator
    assert calculators.CohensKappaCalculator is CohensKappaCalculator
    assert calculators.ConfidenceIntervalCalculator is ConfidenceIntervalCalculator
    assert calculators.FleissAgreementRatioCalculator is FleissAgreementRatioCalculator
    assert calculators.FleissKappaCalculator is FleissKappaCalculator
    assert calculators.FleissKappaScoreCalculator is FleissKappaScoreCalculator
    assert calculators.MAECalculator is MAECalculator
    assert calculators.MSECalculator is MSECalculator
    assert (
        calculators.OverallAlignmentScoreCalculator is OverallAlignmentScoreCalculator
    )
    assert calculators.PairedTTestCalculator is PairedTTestCalculator
    assert calculators.PearsonCoefficientCalculator is PearsonCoefficientCalculator
    assert calculators.PearsonCorrelationCalculator is PearsonCorrelationCalculator
    assert calculators.R2ScoreCalculator is R2ScoreCalculator
    assert calculators.RegressionMetricsCalculator is RegressionMetricsCalculator
    assert calculators.RMSECalculator is RMSECalculator
