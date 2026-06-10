from __future__ import annotations

from dataclasses import dataclass

from src.evaluation.dataset.validators.sample_annotation_consensus_validator import (
    SampleAnnotationConsensusValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class SampleAnnotationConsensus:
    """
    Consensus metrics for a single evaluation sample.
    """

    sample_id: str
    annotator_count: int

    consensus_score: float
    min_score: float
    max_score: float
    score_range: float

    def __post_init__(self) -> None:
        SampleAnnotationConsensusValidator.validate(
            sample_id=self.sample_id,
            annotator_count=self.annotator_count,
            consensus_score=self.consensus_score,
            min_score=self.min_score,
            max_score=self.max_score,
            score_range=self.score_range,
        )