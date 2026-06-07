from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from src.domain.enums.level import Level
from src.evaluation.domain.validators.evaluation_sample_validator import (
    EvaluationSampleValidator,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EvaluationSample:
    sample_id: str
    question_id: str
    question: str
    candidate_answer: str
    expected_answer: str
    category: str
    level: Level
    retrieved_contexts: tuple[str, ...]
    metadata: Mapping[str, Any]


    def __post_init__(self) -> None:
        EvaluationSampleValidator.validate(
            sample_id=self.sample_id,
            question_id=self.question_id,
            question=self.question,
            candidate_answer=self.candidate_answer,
            expected_answer=self.expected_answer,
            category=self.category,
            level=self.level,
            retrieved_contexts=self.retrieved_contexts,
            metadata=self.metadata,
        )