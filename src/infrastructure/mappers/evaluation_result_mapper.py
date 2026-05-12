from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from src.application.models.evaluation_metadata import EvaluationMetadata
from src.application.models.evaluation_payload import EvaluationPayload


class EvaluationResultMapper:
    """
    Raw evaluator/provider çıktısını application payload modellerine dönüştürür.

    Bu mapper:
        - raw Mapping okur
        - safe type conversion yapar
        - string/list normalization yapar

    Bu mapper:
        - business fallback kararı vermez
        - score clamp etmez
        - domain validation yapmaz
        - EvaluationResult oluşturmaz
    """

    @classmethod
    def to_payload(
        cls,
        data: Mapping[str, Any],
    ) -> EvaluationPayload:
        return EvaluationPayload(
            score=cls._to_optional_float(data.get("score")),
            feedback=cls._to_optional_non_empty_string(
                data.get("feedback")
            ),
            technical_accuracy=cls._to_optional_float(
                data.get("technical_accuracy")
            ),
            depth=cls._to_optional_float(data.get("depth")),
            communication=cls._to_optional_float(
                data.get("communication")
            ),
            missing_keywords=cls._to_string_tuple(
                data.get("missing_keywords")
            ),
            follow_up_question=cls._to_optional_non_empty_string(
                data.get("follow_up_question")
            ),
            confidence=cls._to_optional_float(
                data.get("confidence")
            ),
            rubric_version=cls._to_optional_non_empty_string(
                data.get("rubric_version")
            ),
        )

    @classmethod
    def to_metadata(
        cls,
        data: Mapping[str, Any],
    ) -> EvaluationMetadata:
        return EvaluationMetadata(
            model_name=cls._to_optional_non_empty_string(
                data.get("model_name")
            ),
            tokens_used=cls._to_optional_int(
                data.get("tokens_used")
            ),
            latency_seconds=cls._to_optional_float(
                data.get("latency_seconds")
            ),
        )

    @staticmethod
    def _to_optional_float(
        value: object,
    ) -> float | None:
        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_optional_int(
        value: object,
    ) -> int | None:
        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _to_optional_non_empty_string(
        value: object,
    ) -> str | None:
        if value is None:
            return None

        normalized_value = str(value).strip()

        if not normalized_value:
            return None

        return normalized_value

    @staticmethod
    def _to_string_tuple(
        value: object,
    ) -> tuple[str, ...]:
        if value is None:
            return ()

        if isinstance(value, str):
            normalized_value = value.strip()
            return (normalized_value,) if normalized_value else ()

        if not isinstance(value, list | tuple | set):
            return ()

        return tuple(
            normalized_item
            for item in value
            if (normalized_item := str(item).strip())
        )