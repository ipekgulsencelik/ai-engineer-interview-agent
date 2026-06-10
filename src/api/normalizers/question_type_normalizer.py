from __future__ import annotations

from typing import Any


class QuestionTypeNormalizer:
    """
    API boundary question_type input değerini normalize eder.
    """

    @staticmethod
    def normalize(
        value: Any,
    ) -> Any:
        if isinstance(value, str):
            return value.strip().lower()

        return value