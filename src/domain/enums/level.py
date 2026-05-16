from __future__ import annotations

from enum import StrEnum


class Level(StrEnum):
    """
    Interview difficulty level enum.

    Bu enum sadece sabit domain değerlerini temsil eder.
    Parsing, validation veya transition logic içermez.
    """

    JR = "JR"
    MID = "MID"
    SENIOR = "SENIOR"