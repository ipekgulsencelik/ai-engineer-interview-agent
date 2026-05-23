from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionMetadataItem:
    """
    UI-safe immutable metadata item for question presentation.
    """

    label: str
    value: str