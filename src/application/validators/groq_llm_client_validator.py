from __future__ import annotations

from groq import Groq

from src.application.models.llm_request import (
    LLMRequest,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class GroqLLMClientValidator(
    BaseSchemaValidator,
):
    """
    GroqLLMClient validation helper.
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

    @classmethod
    def validate_client(
        cls,
        *,
        client: Groq,
    ) -> None:
        cls.validate_model_type(
            value=client,
            expected_type=Groq,
            field_name="client",
        )

    @classmethod
    def validate_request(
        cls,
        *,
        request: LLMRequest,
    ) -> None:
        cls.validate_model_type(
            value=request,
            expected_type=LLMRequest,
            field_name="request",
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