from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.application.models.evaluation_metadata import (
        EvaluationMetadata,
    )


class EvaluationMetadataValidator:
    """
    EvaluationMetadata için metadata-driven validation kurallarını yönetir.

    Bu validator:
        - field metadata kurallarını okur
        - nullable field desteği sağlar
        - runtime type validation yapar
        - empty string değerlerini engeller
        - NaN / infinity değerlerini reddeder
        - min_value constraint uygular

    Bu validator:
        - evaluation sonucu üretmez
        - provider çağrısı yapmaz
        - logging/tracing yönetmez
    """

    @classmethod
    def validate(
        cls,
        metadata: "EvaluationMetadata",
    ) -> None:
        """
        EvaluationMetadata instance'ını metadata kurallarına göre validate eder.
        """

        cls._validate_model_type(metadata)

        for model_field in fields(metadata):
            field_name = model_field.name
            value = getattr(
                metadata,
                field_name,
            )
            field_metadata = model_field.metadata

            nullable = field_metadata.get(
                "nullable",
                False,
            )

            if value is None and nullable:
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=field_metadata.get("type"),
            )

            if field_metadata.get("finite", False):
                cls._validate_finite(
                    field_name=field_name,
                    value=value,
                )

            if field_metadata.get("non_empty", False):
                cls._validate_non_empty(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in field_metadata:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=field_metadata["min_value"],
                )

    @staticmethod
    def _validate_model_type(
        metadata: "EvaluationMetadata",
    ) -> None:
        """
        Runtime'da doğru model tipinin validate edildiğini garanti eder.
        """

        from src.application.models.evaluation_metadata import (
            EvaluationMetadata,
        )

        if not isinstance(metadata, EvaluationMetadata):
            raise TypeError(
                "metadata must be an EvaluationMetadata instance."
            )

    @staticmethod
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: Any,
    ) -> None:
        """
        Field metadata içindeki expected type contract'ını doğrular.
        """

        if expected_type is None:
            return

        if expected_type is not bool and isinstance(value, bool):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type}."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: float,
    ) -> None:
        """
        NaN ve infinity değerlerini reddeder.
        """

        if not math.isfinite(value):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: str,
    ) -> None:
        """
        String alanların boş veya whitespace-only olmasını engeller.
        """

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: float,
        min_value: float,
    ) -> None:
        """
        Minimum numeric değer constraint'ini uygular.
        """

        if value < min_value:
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )