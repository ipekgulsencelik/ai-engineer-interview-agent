from __future__ import annotations


class GroqResponseExtractor:
    """
    Groq SDK response extraction helper.
    """

    @staticmethod
    def extract_text(
        *,
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
    def extract_prompt_tokens(
        *,
        response: object,
    ) -> int | None:
        return GroqResponseExtractor._extract_usage_int(
            response=response,
            field_name="prompt_tokens",
        )

    @staticmethod
    def extract_completion_tokens(
        *,
        response: object,
    ) -> int | None:
        return GroqResponseExtractor._extract_usage_int(
            response=response,
            field_name="completion_tokens",
        )

    @staticmethod
    def extract_total_tokens(
        *,
        response: object,
    ) -> int | None:
        return GroqResponseExtractor._extract_usage_int(
            response=response,
            field_name="total_tokens",
        )

    @staticmethod
    def extract_finish_reason(
        *,
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

    @staticmethod
    def _extract_usage_int(
        *,
        response: object,
        field_name: str,
    ) -> int | None:
        usage = getattr(response, "usage", None)

        if usage is None:
            return None

        value = getattr(
            usage,
            field_name,
            None,
        )

        if value is None:
            return None

        try:
            return int(value)

        except (TypeError, ValueError) as exc:
            raise TypeError(
                f"Groq usage field '{field_name}' must be an integer."
            ) from exc