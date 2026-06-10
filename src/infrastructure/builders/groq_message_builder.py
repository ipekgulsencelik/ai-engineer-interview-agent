from __future__ import annotations

from typing import Literal
from typing import TypedDict

from src.application.models.llm_request import (
    LLMRequest,
)


class GroqMessage(TypedDict):
    role: Literal["system", "user"]
    content: str


class GroqMessageBuilder:
    """
    Groq chat completion message builder.
    """

    @staticmethod
    def build(
        *,
        request: LLMRequest,
    ) -> list[GroqMessage]:
        messages: list[GroqMessage] = []

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