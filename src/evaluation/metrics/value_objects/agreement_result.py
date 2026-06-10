from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.metrics.validators.agreement_result_validator import (
    AgreementResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AgreementResult:
    """
    Immutable evaluator agreement analysis result.

    Represents inter-rater agreement metrics
    across one or more evaluators.
    """

    metric_name: str

    kappa_score: float
    agreement_ratio: float

    sample_count: int
    evaluator_count: int

    method: str

    is_reliable: bool

    interpretation: str

    p_value: float | None = None
    notes: str | None = None

    def __post_init__(self) -> None:
        AgreementResultValidator.validate(
            metric_name=self.metric_name,
            kappa_score=self.kappa_score,
            agreement_ratio=self.agreement_ratio,
            sample_count=self.sample_count,
            evaluator_count=self.evaluator_count,
            method=self.method,
            is_reliable=self.is_reliable,
            interpretation=self.interpretation,
            p_value=self.p_value,
            notes=self.notes,
        )