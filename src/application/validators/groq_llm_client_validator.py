from __future__ import annotations

from src.application.models.llm_request import LLMRequest


class GroqLLMClientValidator:
    """
    GroqLLMClient configuration ve request validation kurallarını yönetir.
    """

    @classmethod
    def validate_config(
        cls,
        *,
        api_key: str,
        model_name: str,
    ) -> None:
        cls._validate_required_string(
            field_name="api_key",
            value=api_key,
        )

        cls._validate_required_string(
            field_name="model_name",
            value=model_name,
        )

    @staticmethod
    def validate_request(
        request: LLMRequest,
    ) -> None:
        if not isinstance(request, LLMRequest):
            raise TypeError(
                "request must be an LLMRequest."
            )

    @staticmethod
    def _validate_required_string(
        *,
        field_name: str,
        value: str,
    ) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )