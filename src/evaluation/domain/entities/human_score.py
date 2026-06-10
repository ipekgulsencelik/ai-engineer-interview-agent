from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.domain.validators.human_score_validator import (
    HumanScoreValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class HumanScore:
    """
    Immutable human evaluation score snapshot.
    """

    sample_id: str
    evaluator_id: str
    overall_score: float
    technical_score: float
    communication_score: float
    feedback: str

    def __post_init__(self) -> None:
        HumanScoreValidator.validate(
            sample_id=self.sample_id,
            evaluator_id=self.evaluator_id,
            overall_score=self.overall_score,
            technical_score=self.technical_score,
            communication_score=self.communication_score,
            feedback=self.feedback,
        )