from __future__ import annotations

import time

from groq import Groq

from src.application.models.llm_request import LLMRequest
from src.application.models.llm_response import LLMResponse
from src.application.models.llm_response_metadata import (
    LLMResponseMetadata,
)
from src.application.ports.llm_client import LLMClient
from src.application.validators.groq_llm_client_validator import (
    GroqLLMClientValidator,
)
from src.domain.constants.evaluation import DEFAULT_LLM_TEMPERATURE
from src.shared.logging.logger import logger


class GroqLLMClient(LLMClient):
    """
    Groq SDK adapter implementation.

    Bu sınıf:
        - LLMRequest alır
        - Groq API çağrısı yapar
        - provider-specific response'u LLMResponse modeline normalize eder
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
            else DEFAULT_LLM_TEMPERATURE
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
                messages=self._build_messages(request),
                temperature=temperature,
                max_tokens=request.max_tokens,
                stop=request.stop or None,
            )

            latency_seconds = time.perf_counter() - started_at

            text = self._extract_text(response)

            metadata = LLMResponseMetadata(
                model=self._model_name,
                prompt_tokens=self._extract_prompt_tokens(response),
                completion_tokens=self._extract_completion_tokens(response),
                total_tokens=self._extract_total_tokens(response),
                latency_seconds=latency_seconds,
                finish_reason=self._extract_finish_reason(response),
                raw_response=None,
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

    @staticmethod
    def _build_messages(
        request: LLMRequest,
    ) -> list[dict[str, str]]:
        messages: list[dict[str, str]] = []

        if request.system_prompt is not None:
            messages.append(
                {
                    "role": "system",
                    "content": request.system_prompt,
                }
            )

        messages.append(
            {
                "role": "user",
                "content": request.prompt,
            }
        )

        return messages

    @staticmethod
    def _extract_text(
        response: object,
    ) -> str:
        choices = getattr(response, "choices", None)

        if not choices:
            raise ValueError(
                "Groq response choices cannot be empty."
            )

        message = getattr(choices[0], "message", None)

        if message is None:
            raise ValueError(
                "Groq response message cannot be None."
            )

        content = getattr(message, "content", None)

        if content is None:
            raise ValueError(
                "Groq response content cannot be None."
            )

        if not isinstance(content, str):
            raise TypeError(
                "Groq response content must be a string."
            )

        if not content.strip():
            raise ValueError(
                "Groq response content cannot be empty."
            )

        return content

    @staticmethod
    def _extract_prompt_tokens(
        response: object,
    ) -> int | None:
        return GroqLLMClient._extract_usage_int(
            response=response,
            field_name="prompt_tokens",
        )

    @staticmethod
    def _extract_completion_tokens(
        response: object,
    ) -> int | None:
        return GroqLLMClient._extract_usage_int(
            response=response,
            field_name="completion_tokens",
        )

    @staticmethod
    def _extract_total_tokens(
        response: object,
    ) -> int | None:
        return GroqLLMClient._extract_usage_int(
            response=response,
            field_name="total_tokens",
        )

    @staticmethod
    def _extract_usage_int(
        *,
        response: object,
        field_name: str,
    ) -> int | None:
        usage = getattr(response, "usage", None)

        if usage is None:
            return None

        value = getattr(usage, field_name, None)

        if value is None:
            return None

        return int(value)

    @staticmethod
    def _extract_finish_reason(
        response: object,
    ) -> str | None:
        choices = getattr(response, "choices", None)

        if not choices:
            return None

        finish_reason = getattr(
            choices[0],
            "finish_reason",
            None,
        )

        if finish_reason is None:
            return None

        return str(finish_reason)