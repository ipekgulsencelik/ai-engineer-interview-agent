from __future__ import annotations

import time

from groq import Groq

from src.application.constants.llm import (
    DEFAULT_TEMPERATURE,
)
from src.application.models.llm_request import (
    LLMRequest,
)
from src.application.models.llm_response import (
    LLMResponse,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.application.validators.groq_llm_client_validator import (
    GroqLLMClientValidator,
)
from src.infrastructure.builders.groq_message_builder import (
    GroqMessageBuilder,
)
from src.infrastructure.extractors.groq_response_extractor import (
    GroqResponseExtractor,
)
from src.infrastructure.mappers.groq_response_metadata_mapper import (
    GroqResponseMetadataMapper,
)
from src.shared.logging.logger import logger


class GroqLLMClient(LLMClient):
    """
    Groq SDK adapter implementation.
    """

    def __init__(
        self,
        *,
        api_key: str,
        model_name: str,
        client: Groq | None = None,
    ) -> None:
        GroqLLMClientValidator.validate_config(
            api_key=api_key,
            model_name=model_name,
        )

        self._client = client or Groq(
            api_key=api_key,
        )
        self._model_name = model_name

        logger.info(
            "GroqLLMClient initialized.",
            model_name=self._model_name,
        )

    def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:
        GroqLLMClientValidator.validate_request(
            request,
        )

        temperature = (
            request.temperature
            if request.temperature is not None
            else DEFAULT_TEMPERATURE
        )

        logger.info(
            "Groq generation started.",
            model_name=self._model_name,
            prompt_length=len(request.prompt),
            temperature=temperature,
        )

        started_at = time.perf_counter()

        try:
            response = self._client.chat.completions.create(
                model=self._model_name,
                messages=GroqMessageBuilder.build(
                    request=request,
                ),
                temperature=temperature,
                max_tokens=request.max_tokens,
                stop=request.stop or None,
            )

            latency_seconds = (
                time.perf_counter()
                - started_at
            )

            text = GroqResponseExtractor.extract_text(
                response=response,
            )

            metadata = GroqResponseMetadataMapper.to_metadata(
                response=response,
                model_name=self._model_name,
                latency_seconds=latency_seconds,
            )

            logger.info(
                "Groq generation completed.",
                model_name=self._model_name,
                latency_seconds=latency_seconds,
                prompt_tokens=metadata.prompt_tokens,
                completion_tokens=metadata.completion_tokens,
                total_tokens=metadata.total_tokens,
                finish_reason=metadata.finish_reason,
            )

            return LLMResponse(
                text=text,
                metadata=metadata,
            )

        except Exception:
            logger.exception(
                "Groq generation failed.",
                model_name=self._model_name,
            )
            raise