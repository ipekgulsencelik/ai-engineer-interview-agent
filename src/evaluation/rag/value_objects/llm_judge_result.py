from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True, kw_only=True)
class LLMJudgeResult:
    score: float
    reason: str
