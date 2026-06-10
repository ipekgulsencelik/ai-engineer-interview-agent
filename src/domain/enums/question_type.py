from __future__ import annotations

from enum import StrEnum


class QuestionType(StrEnum):
    """
    Interview question type enum.
    """

    CONCEPTUAL = "conceptual"
    CODING = "coding"
    SCENARIO = "scenario"
    SYSTEM_DESIGN = "system_design"
    DEBUGGING = "debugging"
    COMPARISON = "comparison"
