from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.domain.enums.agreement_level import (
    AgreementLevel,
)
from src.evaluation.domain.validators.alignment_result_validator import (
    AlignmentResultValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AlignmentResult:
    """
    Immutable human-vs-LLM alignment evaluation snapshot.
    """

    sample_id: str

    alignment_evaluation_id: str
    alignment_evaluation_timestamp: str
    alignment_evaluation_version: str
    alignment_evaluation_criteria: str
    alignment_evaluation_feedback: str

    pearson_correlation: float
    cohen_kappa: float
    mean_absolute_error: float
    agreement_level: AgreementLevel

    llm_model_name: str
    human_evaluator_id: str

    overall_alignment_score: float
    technical_alignment_score: float
    communication_alignment_score: float
    reasoning_alignment_score: float

    def __post_init__(self) -> None:
        AlignmentResultValidator.validate(
            sample_id=self.sample_id,
            alignment_evaluation_id=self.alignment_evaluation_id,
            alignment_evaluation_timestamp=(
                self.alignment_evaluation_timestamp
            ),
            alignment_evaluation_version=(
                self.alignment_evaluation_version
            ),
            alignment_evaluation_criteria=(
                self.alignment_evaluation_criteria
            ),
            alignment_evaluation_feedback=(
                self.alignment_evaluation_feedback
            ),
            pearson_correlation=self.pearson_correlation,
            cohen_kappa=self.cohen_kappa,
            mean_absolute_error=self.mean_absolute_error,
            agreement_level=self.agreement_level,
            llm_model_name=self.llm_model_name,
            human_evaluator_id=self.human_evaluator_id,
            overall_alignment_score=(
                self.overall_alignment_score
            ),
            technical_alignment_score=(
                self.technical_alignment_score
            ),
            communication_alignment_score=(
                self.communication_alignment_score
            ),
            reasoning_alignment_score=(
                self.reasoning_alignment_score
            ),
        )