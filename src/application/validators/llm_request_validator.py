from __future__ import annotations

import math
from typing import TYPE_CHECKING

from src.domain.constants.evaluation import (
    MAX_LLM_TEMPERATURE,
    MIN_LLM_TEMPERATURE,
)

if TYPE_CHECKING:
    from src.application.models.llm_request import LLMRequest


class LLMRequestValidator:
    """
    LLMRequest validation kurallarını yönetir.
    """

    @classmethod
    def validate(
        cls,
        request: LLMRequest,
    ) -> None:
        cls._validate_required_string(
            field_name="prompt",
            value=request.prompt,
        )

        cls._validate_optional_string(
            field_name="system_prompt",
            value=request.system_prompt,
        )

        cls._validate_optional_temperature(
            request.temperature,
        )

        cls._validate_optional_max_tokens(
            request.max_tokens,
        )

        cls._validate_stop(
            request.stop,
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

    @staticmethod
    def _validate_optional_string(
        *,
        field_name: str,
        value: str | None,
    ) -> None:
        if value is None:
            return

        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} must be a string."
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_optional_temperature(
        value: float | None,
    ) -> None:
        if value is None:
            return

        if isinstance(value, bool):
            raise TypeError(
                "temperature must be numeric."
            )

        if not isinstance(value, int | float):
            raise TypeError(
                "temperature must be numeric."
            )

        numeric_value = float(value)

        if not math.isfinite(numeric_value):
            raise ValueError(
                "temperature must be finite."
            )

        if not (
            MIN_LLM_TEMPERATURE
            <= numeric_value
            <= MAX_LLM_TEMPERATURE
        ):
            raise ValueError(
                "temperature must be between "
                f"{MIN_LLM_TEMPERATURE} and "
                f"{MAX_LLM_TEMPERATURE}."
            )

    @staticmethod
    def _validate_optional_max_tokens(
        value: int | None,
    ) -> None:
        if value is None:
            return

        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                "max_tokens must be an integer."
            )

        if value <= 0:
            raise ValueError(
                "max_tokens must be greater than zero."
            )

    @staticmethod
    def _validate_stop(
        value: tuple[str, ...] | None,
    ) -> None:
        if value is None:
            return

        if not isinstance(value, tuple):
            raise TypeError(
                "stop must be a tuple."
            )

        for item in value:
            if not isinstance(item, str):
                raise TypeError(
                    "stop items must be strings."
                )

            if not item.strip():
                raise ValueError(
                    "stop items cannot be empty."
                )