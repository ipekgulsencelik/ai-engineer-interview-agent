from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.regression_metric_result_validator import (
    RegressionMetricResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class RegressionMetricResult:
    """
    Immutable regression metric analysis result.

    Represents regression evaluation metrics such as
    MAE, MSE, RMSE, and R².
    """

    metric_name: str

    mae: float
    mse: float
    rmse: float
    r2_score: float

    sample_count: int

    is_acceptable: bool
    interpretation: str

    notes: str | None = None

    def __post_init__(self) -> None:
        RegressionMetricResultValidator.validate(
            metric_name=self.metric_name,
            mae=self.mae,
            mse=self.mse,
            rmse=self.rmse,
            r2_score=self.r2_score,
            sample_count=self.sample_count,
            is_acceptable=self.is_acceptable,
            interpretation=self.interpretation,
            notes=self.notes,
        )