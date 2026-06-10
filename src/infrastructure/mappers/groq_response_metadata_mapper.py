from __future__ import annotations

from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.infrastructure.constants.providers import (
    GROQ_PROVIDER_NAME,
)
from src.infrastructure.extractors.groq_response_extractor import (
    GroqResponseExtractor,
)


class GroqResponseMetadataMapper:
    """
    Groq SDK response -> LLMResponseMetadata mapper.
    """

    @staticmethod
    def to_metadata(
        *,
        response: object,
        model_name: str,
        latency_seconds: float,
    ) -> LLMResponseMetadata:
        return LLMResponseMetadata(
            model_name=model_name,
            provider_name=GROQ_PROVIDER_NAME,
            prompt_tokens=(
                GroqResponseExtractor.extract_prompt_tokens(
                    response=response,
                )
            ),
            completion_tokens=(
                GroqResponseExtractor.extract_completion_tokens(
                    response=response,
                )
            ),
            total_tokens=(
                GroqResponseExtractor.extract_total_tokens(
                    response=response,
                )
            ),
            latency_seconds=latency_seconds,
            finish_reason=(
                GroqResponseExtractor.extract_finish_reason(
                    response=response,
                )
            ),
            raw_response=None,
        )