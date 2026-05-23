from __future__ import annotations

from enum import Enum


class QuestionLevel(str, Enum):
    """
    API-level interview question difficulty tiers.
    """

    JR = "JR"

    MID = "MID"

    SENIOR = "SENIOR"


class QuestionType(str, Enum):
    """
    API-level interview question type definitions.
    """

    CONCEPTUAL = "conceptual"

    CODING = "coding"

    SCENARIO = "scenario"

    SYSTEM_DESIGN = "system_design"

    DEBUGGING = "debugging"