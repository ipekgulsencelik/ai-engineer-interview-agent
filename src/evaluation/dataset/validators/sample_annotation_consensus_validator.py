from __future__ import annotations

import math

from src.domain.validation.schema_validator import (
    SchemaValidator,
)
from src.evaluation.domain.constants.consensus import (
    CONSENSUS_ABS_TOLERANCE,
    CONSENSUS_REL_TOLERANCE,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.schemas.sample_annotation_consensus_schema import (
    SAMPLE_ANNOTATION_CONSENSUS_SCHEMA,
)


class SampleAnnotationConsensusValidator:
    """
    SampleAnnotationConsensus validation service.
    """

    @staticmethod
    def validate(
        *,
        sample_id: str,
        annotator_count: int,
        consensus_score: float,
        min_score: float,
        max_score: float,
        score_range: float,
    ) -> None:
        SchemaValidator.validate(
            values={
                "sample_id": sample_id,
                "annotator_count": annotator_count,
                "consensus_score": consensus_score,
                "min_score": min_score,
                "max_score": max_score,
                "score_range": score_range,
            },
            schema=SAMPLE_ANNOTATION_CONSENSUS_SCHEMA,
            error_factory=EvaluationValidationError,
        )

        if min_score > max_score:
            raise EvaluationValidationError(
                "min_score cannot be greater than max_score."
            )

        expected_range = max_score - min_score

        if not math.isclose(
            score_range,
            expected_range,
            rel_tol=CONSENSUS_REL_TOLERANCE,
            abs_tol=CONSENSUS_ABS_TOLERANCE,
        ):
            raise EvaluationValidationError(
                "score_range must equal max_score - min_score."
            )