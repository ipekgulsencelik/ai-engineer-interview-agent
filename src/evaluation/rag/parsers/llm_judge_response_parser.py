from __future__ import annotations

import json
from typing import Any

from src.evaluation.rag.value_objects.llm_judge_result import LLMJudgeResult


class LLMJudgeResponseParser:
    @staticmethod
    def parse(*, response: str) -> LLMJudgeResult:
        payload: dict[str, Any] = json.loads(response)
        return LLMJudgeResult(score=float(payload["score"]), reason=str(payload["reason"]))
