from __future__ import annotations

from typing import Any

from src.api.normalizers.difficulty_normalizer import DifficultyNormalizer
from src.api.normalizers.level_normalizer import LevelNormalizer
from src.api.normalizers.question_type_normalizer import QuestionTypeNormalizer


class EvaluationRequestValidator:
    """
    EvaluationRequest schema'sı için API boundary validation/normalization facade'ıdır.
    """

    @staticmethod
    def normalize_level(
        value: Any,
    ) -> Any:
        return LevelNormalizer.normalize(value)

    @staticmethod
    def normalize_difficulty(
        value: Any,
    ) -> Any:
        return DifficultyNormalizer.normalize(value)

    @staticmethod
    def normalize_question_type(
        value: Any,
    ) -> Any:
        return QuestionTypeNormalizer.normalize(value)