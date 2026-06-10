from __future__ import annotations

from src.domain.validators.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.dataset.schemas.annotation_consensus_schema import (
    ANNOTATION_CONSENSUS_SCHEMA,
)


class AnnotationConsensusValidator:
    """
    AnnotationConsensus validation service.
    """

    @staticmethod
    def validate(
        *,
        evaluation_id: str,
        evaluator_count: int,
        sample_count: int,
        agreement_score: float,
        cohen_kappa: float,
        fleiss_kappa: float,
        mean_score_variance: float,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "evaluation_id": evaluation_id,
                "evaluator_count": evaluator_count,
                "sample_count": sample_count,
                "agreement_score": agreement_score,
                "cohen_kappa": cohen_kappa,
                "fleiss_kappa": fleiss_kappa,
                "mean_score_variance": mean_score_variance,
                "notes": notes,
            },
            schema=ANNOTATION_CONSENSUS_SCHEMA,
            error_factory=EvaluationValidationError,
        )