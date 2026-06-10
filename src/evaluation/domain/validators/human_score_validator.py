from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.schemas.human_score_schema import (
    HUMAN_SCORE_SCHEMA,
)


class HumanScoreValidator:
    """
    HumanScore entity validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_id: str,
        evaluator_id: str,
        overall_score: float,
        technical_score: float,
        communication_score: float,
        feedback: str,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "evaluator_id": evaluator_id,
                "overall_score": overall_score,
                "technical_score": technical_score,
                "communication_score": communication_score,
                "feedback": feedback,
            },
            schema=HUMAN_SCORE_SCHEMA,
            error_factory=EvaluationValidationError,
        )