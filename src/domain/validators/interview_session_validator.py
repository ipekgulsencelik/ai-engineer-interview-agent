from __future__ import annotations

from src.domain.enums.level import Level
from src.domain.results.evaluation_result import EvaluationResult


class InterviewSessionValidator:
    @staticmethod
    def validate(session: "InterviewSession") -> None:
        InterviewSessionValidator._validate_session_id(session.session_id)
        InterviewSessionValidator._validate_level(session.current_level)
        InterviewSessionValidator._validate_question_ids(session.asked_question_ids)
        InterviewSessionValidator._validate_results(session.completed_results)
        InterviewSessionValidator._validate_scores(session.recent_scores)

    @staticmethod
    def _validate_session_id(session_id: str) -> None:
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id cannot be empty")

    @staticmethod
    def _validate_level(level: Level) -> None:
        if not isinstance(level, Level):
            raise TypeError("current_level must be a Level instance")

    @staticmethod
    def _validate_question_ids(asked_question_ids: tuple[str, ...]) -> None:
        if not isinstance(asked_question_ids, tuple):
            raise TypeError("asked_question_ids must be a tuple")

        for question_id in asked_question_ids:
            if not isinstance(question_id, str) or not question_id.strip():
                raise ValueError("asked_question_ids cannot include empty values")

    @staticmethod
    def _validate_results(completed_results: tuple[EvaluationResult, ...]) -> None:
        if not isinstance(completed_results, tuple):
            raise TypeError("completed_results must be a tuple")

        for result in completed_results:
            if not isinstance(result, EvaluationResult):
                raise TypeError("completed_results items must be EvaluationResult")

    @staticmethod
    def _validate_scores(recent_scores: tuple[float, ...]) -> None:
        if not isinstance(recent_scores, tuple):
            raise TypeError("recent_scores must be a tuple")

        for score in recent_scores:
            if not isinstance(score, (int, float)):
                raise TypeError("recent_scores items must be numeric")
            if score < 0.0 or score > 10.0:
                raise ValueError("recent_scores values must be between 0.0 and 10.0")
