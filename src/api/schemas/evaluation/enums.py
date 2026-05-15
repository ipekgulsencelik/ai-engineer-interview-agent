from __future__ import annotations

from enum import Enum


class QuestionLevel(str, Enum):
    JR = "JR"
    MID = "MID"
    SENIOR = "SENIOR"


class QuestionType(str, Enum):
    CONCEPTUAL = "conceptual"
    CODING = "coding"
    SCENARIO = "scenario"
    SYSTEM_DESIGN = "system_design"
    DEBUGGING = "debugging"