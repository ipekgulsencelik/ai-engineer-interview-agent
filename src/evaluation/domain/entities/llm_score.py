from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.domain.validators.llm_score_validator import (
    LLMScoreValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class LLMScore:
    """
    Immutable LLM evaluation score snapshot.
    """

    sample_id: str
    model_name: str

    overall_score: float
    technical_score: float
    communication_score: float
    reasoning_score: float
    confidence_score: float

    feedback: str

    def __post_init__(self) -> None:
        LLMScoreValidator.validate(
            sample_id=self.sample_id,
            model_name=self.model_name,
            overall_score=self.overall_score,
            technical_score=self.technical_score,
            communication_score=self.communication_score,
            reasoning_score=self.reasoning_score,
            confidence_score=self.confidence_score,
            feedback=self.feedback,
        )