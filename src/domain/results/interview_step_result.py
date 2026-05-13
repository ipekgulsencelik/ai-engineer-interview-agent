from __future__ import annotations

from dataclasses import dataclass

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.results.selection_result import SelectionResult
from src.domain.validators.interview_step_result_validator import (
    InterviewStepResultValidator,
)


@dataclass(frozen=True)
class InterviewStepResult:
    """Immutable and validated snapshot of a single interview turn."""

    selection_result: SelectionResult
    question: Question
    answer: str
    evaluation_result: EvaluationResult
    next_level: Level
    updated_session: InterviewSession

    def __post_init__(self) -> None:
        InterviewStepResultValidator.validate(self)