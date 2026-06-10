from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.schemas.llm_score_schema import (
    LLM_SCORE_SCHEMA,
)


class LLMScoreValidator:
    """
    LLMScore entity validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_id: str,
        model_name: str,
        overall_score: float,
        technical_score: float,
        communication_score: float,
        reasoning_score: float,
        confidence_score: float,
        feedback: str,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "model_name": model_name,
                "overall_score": overall_score,
                "technical_score": technical_score,
                "communication_score": communication_score,
                "reasoning_score": reasoning_score,
                "confidence_score": confidence_score,
                "feedback": feedback,
            },
            schema=LLM_SCORE_SCHEMA,
            error_factory=EvaluationValidationError,
        )