from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationMetricItem:
    """
    Immutable evaluation metric presentation item.
    """

    label: str
    value: str