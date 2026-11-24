from __future__ import annotations


class AnswerValidator:
    """
    Candidate answer validation kurallarını yönetir.
    """

    @staticmethod
    def validate(
        answer: str,
    ) -> str:
        """Validate and return the answer with surrounding whitespace removed."""
        if not isinstance(answer, str):
            raise TypeError(
                "answer must be a string."
            )

        if not answer.strip():
            raise ValueError(
                "answer cannot be empty."
            )

        return answer.strip()