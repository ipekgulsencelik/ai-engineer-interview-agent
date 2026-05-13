from __future__ import annotations

from typing import Any

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.results.selection_result import SelectionResult

INTERVIEW_STEP_RESULT_VALIDATION_SCHEMA: dict[str, dict[str, Any]] = {
    "selection_result": {
        "type": SelectionResult,
    },
    "question": {
        "type": Question,
    },
    "answer": {
        "type": str,
        "non_empty": True,
        "strip": True,
    },
    "evaluation_result": {
        "type": EvaluationResult,
    },
    "next_level": {
        "type": Level,
    },
    "updated_session": {
        "type": InterviewSession,
    },
}