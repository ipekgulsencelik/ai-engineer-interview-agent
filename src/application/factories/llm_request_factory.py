from __future__ import annotations

from src.application.models.llm_request import (
    LLMRequest,
)


class LLMRequestFactory:
    """
    LLMRequest creation factory.
    """

    @staticmethod
    def create(
        *,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
        stop: tuple[str, ...] = (),
    ) -> LLMRequest:
        return LLMRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            stop=stop,
        )