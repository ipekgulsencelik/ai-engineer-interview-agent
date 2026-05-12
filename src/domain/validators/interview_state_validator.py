from __future__ import annotations

from src.domain.enums.level import Level


class InterviewStateValidator:
    @staticmethod
    def validate_identity(*, session_id: str, candidate_id: str) -> None:
        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError("session_id cannot be empty")

        if not isinstance(candidate_id, str) or not candidate_id.strip():
            raise ValueError("candidate_id cannot be empty")

    @staticmethod
    def validate_level(level: Level) -> None:
        if not isinstance(level, Level):
            raise TypeError("current_level must be a Level instance")

    @staticmethod
    def validate_question_id(question_id: str) -> str:
        if not isinstance(question_id, str):
            raise TypeError("question_id must be a string")

        normalized = question_id.strip()
        if not normalized:
            raise ValueError("question_id cannot be empty")

        return normalized

    @staticmethod
    def validate_score(score: float | None) -> None:
        if score is None:
            return

        if not isinstance(score, (int, float)):
            raise TypeError("score must be numeric")

        if score < 0.0 or score > 10.0:
            raise ValueError("score must be between 0.0 and 10.0")
