from __future__ import annotations


class QuestionLookupValidator:
    """Input validation for repository lookup operations."""

    @staticmethod
    def validate_question_id(question_id: str) -> None:
        if not isinstance(question_id, str):
            raise ValueError("question_id must be a string.")

        if not question_id.strip():
            raise ValueError("question_id cannot be empty.")
        
        if len(question_id) > 255:
            raise ValueError("question_id cannot exceed 255 characters.")