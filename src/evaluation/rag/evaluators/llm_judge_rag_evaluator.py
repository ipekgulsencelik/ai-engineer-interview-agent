from __future__ import annotations

from src.evaluation.rag.builders.llm_judge_prompt_builder import (
    LLMJudgePromptBuilder,
)
from src.evaluation.rag.parsers.llm_judge_response_parser import (
    LLMJudgeResponseParser,
)
from src.evaluation.rag.ports.llm_judge_ports import (
    LLMJudgePromptBuilding,
    LLMJudgeResponseParsing,
)
from src.evaluation.rag.value_objects.llm_judge_request import (
    LLMJudgeRequest,
)
from src.evaluation.rag.value_objects.llm_judge_result import (
    LLMJudgeResult,
)


class LLMJudgeRAGEvaluator:
    """Coordinates LLM judge prompt building and response parsing."""

    def __init__(
        self,
        *,
        prompt_builder: LLMJudgePromptBuilding | None = None,
        response_parser: LLMJudgeResponseParsing | None = None,
    ) -> None:
        self._prompt_builder = prompt_builder or LLMJudgePromptBuilder()
        self._response_parser = response_parser or LLMJudgeResponseParser()

    def build_prompt(
        self,
        *,
        request: LLMJudgeRequest,
    ) -> str:
        return self._prompt_builder.build(
            request=request,
        )

    def parse_response(
        self,
        *,
        response: str,
    ) -> LLMJudgeResult:
        return self._response_parser.parse(
            response=response,
        )
