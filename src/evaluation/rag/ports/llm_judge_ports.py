from __future__ import annotations

from typing import Protocol

from src.evaluation.rag.value_objects.llm_judge_request import LLMJudgeRequest
from src.evaluation.rag.value_objects.llm_judge_result import LLMJudgeResult


class LLMJudgePromptBuilding(Protocol):
    """Builds an LLM judge prompt from a RAG judge request."""

    def build(self, *, request: LLMJudgeRequest) -> str:
        ...


class LLMJudgeResponseParsing(Protocol):
    """Parses a raw LLM judge response into a typed result."""

    def parse(self, *, response: str) -> LLMJudgeResult:
        ...
