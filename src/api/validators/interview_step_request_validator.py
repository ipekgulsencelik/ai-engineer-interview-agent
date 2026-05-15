from __future__ import annotations

from typing import Any

from src.api.normalizers.level_normalizer import (
    LevelNormalizer,
)


class InterviewStepRequestValidator:
    """
    InterviewStepRequest API validation facade.
    """

    @staticmethod
    def normalize_current_level(
        value: Any,
    ) -> Any:
        return LevelNormalizer.normalize(
            value,
        )