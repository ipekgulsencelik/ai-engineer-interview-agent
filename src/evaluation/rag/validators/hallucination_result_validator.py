from __future__ import annotations

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.rag.enums.hallucination_label import (
    HallucinationLabel,
)
from src.evaluation.rag.schemas.hallucination_result_schema import (
    HALLUCINATION_RESULT_SCHEMA,
)


class HallucinationResultValidator:
    """
    HallucinationResult validation service.
    """

    @staticmethod
    def validate(
        *,
        label: HallucinationLabel,
        confidence: float,
        hallucination_score: float,
        hallucination_detected: bool,
        unsupported_claim_count: int,
        total_claim_count: int,
        explanation: str,
        notes: str | None,
    ) -> None:
        SchemaValidator.validate(
            values={
                "label": str(label),
                "confidence": confidence,
                "hallucination_score": hallucination_score,
                "hallucination_detected": hallucination_detected,
                "unsupported_claim_count": unsupported_claim_count,
                "total_claim_count": total_claim_count,
                "explanation": explanation,
                "notes": notes,
            },
            schema=HALLUCINATION_RESULT_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if not isinstance(
            label,
            HallucinationLabel,
        ):
            raise EvaluationValidationError(
                "label must be HallucinationLabel."
            )

        if (
            unsupported_claim_count
            > total_claim_count
        ):
            raise EvaluationValidationError(
                "unsupported_claim_count cannot exceed total_claim_count."
            )

        if (
            hallucination_detected
            and unsupported_claim_count == 0
        ):
            raise EvaluationValidationError(
                "unsupported_claim_count must be greater than zero when hallucination_detected is true."
            )

        if (
            not hallucination_detected
            and unsupported_claim_count > 0
        ):
            raise EvaluationValidationError(
                "unsupported_claim_count must be zero when hallucination_detected is false."
            )