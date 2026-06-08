from __future__ import annotations

from statistics import mean

from src.evaluation.dataset.constants.consensus import (
    MIN_ANNOTATOR_COUNT,
)
from src.evaluation.domain.entities import (
    HumanScore,
)
from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.dataset.value_objects.sample_annotation_consensus import (
    SampleAnnotationConsensus,
)


class SampleAnnotationConsensusBuilder:
    """
    Builds sample-level annotation consensus from human scores.
    """

    @staticmethod
    def build(
        *,
        scores: tuple[HumanScore, ...],
    ) -> SampleAnnotationConsensus:
        SampleAnnotationConsensusBuilder._validate_scores(
            scores=scores,
        )

        numeric_scores = tuple(
            score.overall_score
            for score in scores
        )

        min_score = min(numeric_scores)
        max_score = max(numeric_scores)

        return SampleAnnotationConsensus(
            sample_id=scores[0].sample_id,
            annotator_count=len(scores),
            consensus_score=mean(numeric_scores),
            min_score=min_score,
            max_score=max_score,
            score_range=max_score - min_score,
        )

    @staticmethod
    def _validate_scores(
        *,
        scores: tuple[HumanScore, ...],
    ) -> None:
        if len(scores) < MIN_ANNOTATOR_COUNT:
            raise EvaluationValidationError(
                "scores cannot be empty."
            )

        sample_ids = {
            score.sample_id
            for score in scores
        }

        if len(sample_ids) != 1:
            raise EvaluationValidationError(
                "all scores must belong to the same sample."
            )