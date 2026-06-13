from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from src.evaluation.ops.validators.human_feedback_record_validator import (
    HumanFeedbackRecordValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class HumanFeedbackRecord:
    """
    Immutable human feedback record.

    Represents human review feedback collected for
    evaluation governance, evaluator calibration,
    and benchmark improvement workflows.
    """

    feedback_id: str

    evaluator_id: str

    experiment_id: str

    benchmark_id: str
    benchmark_name: str
    benchmark_version: str

    model_name: str

    created_at: datetime

    sample_id: str | None = None

    reviewer_id: str | None = None

    rating: float | None = None

    score: float | None = None

    is_accepted: bool | None = None

    comment: str | None = None

    notes: str | None = None

    def __post_init__(
        self,
    ) -> None:
        HumanFeedbackRecordValidator.validate(
            feedback_id=self.feedback_id,
            evaluator_id=self.evaluator_id,
            experiment_id=self.experiment_id,
            benchmark_id=self.benchmark_id,
            benchmark_name=self.benchmark_name,
            benchmark_version=self.benchmark_version,
            model_name=self.model_name,
            created_at=self.created_at,
            sample_id=self.sample_id,
            reviewer_id=self.reviewer_id,
            rating=self.rating,
            score=self.score,
            is_accepted=self.is_accepted,
            comment=self.comment,
            notes=self.notes,
        )

    @property
    def has_rating(
        self,
    ) -> bool:
        return self.rating is not None

    @property
    def has_score(
        self,
    ) -> bool:
        return self.score is not None

    @property
    def has_comment(
        self,
    ) -> bool:
        return self.comment is not None

    @property
    def has_reviewer(
        self,
    ) -> bool:
        return self.reviewer_id is not None