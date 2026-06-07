from __future__ import annotations

from statistics import mean, pvariance

from src.evaluation.domain.errors.evaluation_validation_error import (
    EvaluationValidationError,
)
from src.evaluation.domain.value_objects.annotation_consensus import (
    AnnotationConsensus,
)
from src.evaluation.domain.value_objects.sample_annotation_consensus import (
    SampleAnnotationConsensus,
)


class AnnotationConsensusBuilder:
    """
    Builds dataset-level annotation consensus from sample-level consensus values.
    """

    @staticmethod
    def build(
        *,
        evaluation_id: str,
        evaluator_count: int,
        sample_consensuses: tuple[SampleAnnotationConsensus, ...],
        notes: str | None = None,
    ) -> AnnotationConsensus:
        if not sample_consensuses:
            raise EvaluationValidationError(
                "sample_consensuses cannot be empty."
            )

        consensus_scores = tuple(
            consensus.consensus_score
            for consensus in sample_consensuses
        )

        agreement_score = mean(consensus_scores)
        mean_score_variance = pvariance(consensus_scores)

        return AnnotationConsensus(
            evaluation_id=evaluation_id,
            evaluator_count=evaluator_count,
            sample_count=len(sample_consensuses),
            agreement_score=agreement_score,
            cohen_kappa=0.0,
            fleiss_kappa=0.0,
            mean_score_variance=mean_score_variance,
            notes=notes,
        )