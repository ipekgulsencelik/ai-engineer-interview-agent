from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.ranked_candidate_validation_schema import (
    RANKED_CANDIDATE_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.results.ranked_candidate import RankedCandidate


class RankedCandidateValidator:
    """
    RankedCandidate domain snapshot'ının invariant kurallarını doğrular.

    Bu validator:
        - model type kontrolü yapar
        - field type validation yapar
        - finite number validation yapar
        - min boundary validation yapar
        - numeric alanlarda bool değerlerini reddeder
    """

    @classmethod
    def validate(
        cls,
        candidate: "RankedCandidate",
    ) -> None:
        cls._validate_model_type(candidate)

        for model_field in fields(candidate):
            field_name = model_field.name
            value = getattr(candidate, field_name)

            rules = RANKED_CANDIDATE_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

            cls._validate_nullable(
                field_name=field_name,
                value=value,
                nullable=rules.get("nullable", False),
            )

            if value is None and rules.get("nullable", False):
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("finite", False):
                cls._validate_finite(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in rules:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=rules["min_value"],
                )

    @staticmethod
    def _validate_model_type(
        candidate: "RankedCandidate",
    ) -> None:
        from src.domain.results.ranked_candidate import RankedCandidate

        if not isinstance(candidate, RankedCandidate):
            raise TypeError(
                "candidate must be a RankedCandidate instance."
            )

    @staticmethod
    def _validate_nullable(
        *,
        field_name: str,
        value: object,
        nullable: bool,
    ) -> None:
        if value is None and not nullable:
            raise TypeError(
                f"{field_name} cannot be None."
            )

    @staticmethod
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: Any,
    ) -> None:
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
        if not math.isfinite(value):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: float,
        min_value: float,
    ) -> None:
        if value < min_value:
            raise ValueError(
                f"{field_name} must be greater than or equal to "
                f"{min_value}."
            )