from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.enums.agreement_level import (
    AgreementLevel,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.schemas.alignment_result_schema import (
    ALIGNMENT_RESULT_SCHEMA,
)


class AlignmentResultValidator:
    """
    AlignmentResult entity validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_id: str,
        alignment_evaluation_id: str,
        alignment_evaluation_timestamp: str,
        alignment_evaluation_version: str,
        alignment_evaluation_criteria: str,
        alignment_evaluation_feedback: str,
        pearson_correlation: float,
        cohen_kappa: float,
        mean_absolute_error: float,
        agreement_level: AgreementLevel,
        llm_model_name: str,
        human_evaluator_id: str,
        overall_alignment_score: float,
        technical_alignment_score: float,
        communication_alignment_score: float,
        reasoning_alignment_score: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "alignment_evaluation_id": alignment_evaluation_id,
                "alignment_evaluation_timestamp": (
                    alignment_evaluation_timestamp
                ),
                "alignment_evaluation_version": (
                    alignment_evaluation_version
                ),
                "alignment_evaluation_criteria": (
                    alignment_evaluation_criteria
                ),
                "alignment_evaluation_feedback": (
                    alignment_evaluation_feedback
                ),
                "pearson_correlation": pearson_correlation,
                "cohen_kappa": cohen_kappa,
                "mean_absolute_error": mean_absolute_error,
                "llm_model_name": llm_model_name,
                "human_evaluator_id": human_evaluator_id,
                "overall_alignment_score": (
                    overall_alignment_score
                ),
                "technical_alignment_score": (
                    technical_alignment_score
                ),
                "communication_alignment_score": (
                    communication_alignment_score
                ),
                "reasoning_alignment_score": (
                    reasoning_alignment_score
                ),
            },
            schema=ALIGNMENT_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            agreement_level,
            AgreementLevel,
        ):
            raise EvaluationValidationError(
                "agreement_level must be an "
                "AgreementLevel enum."
            )