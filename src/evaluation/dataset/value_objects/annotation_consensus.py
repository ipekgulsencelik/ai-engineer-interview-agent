from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.domain.validators.annotation_consensus_validator import (
    AnnotationConsensusValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class AnnotationConsensus:
    """
    Human annotation agreement snapshot.

    Represents consensus metrics across multiple
    human evaluators for a dataset or sample set.
    """

    evaluation_id: str

    evaluator_count: int
    sample_count: int

    agreement_score: float

    cohen_kappa: float
    fleiss_kappa: float

    mean_score_variance: float

    notes: str | None = None

    def __post_init__(self) -> None:
        AnnotationConsensusValidator.validate(
            evaluation_id=self.evaluation_id,
            evaluator_count=self.evaluator_count,
            sample_count=self.sample_count,
            agreement_score=self.agreement_score,
            cohen_kappa=self.cohen_kappa,
            fleiss_kappa=self.fleiss_kappa,
            mean_score_variance=self.mean_score_variance,
            notes=self.notes,
        )