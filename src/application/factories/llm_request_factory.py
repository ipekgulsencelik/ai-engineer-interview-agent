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
        # Only forward what the caller set, so LLMRequest defaults apply
        # instead of being overwritten with None.
        optional: dict[str, float | int] = {}
        if temperature is not None:
            optional["temperature"] = temperature
        if max_tokens is not None:
            optional["max_tokens"] = max_tokens

        return LLMRequest(
            prompt=prompt,
            system_prompt=system_prompt,
            stop=stop,
            **optional,  # type: ignore[arg-type]
        )