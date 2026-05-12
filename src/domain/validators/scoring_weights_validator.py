from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.scoring_weights_validation_schema import (
    SCORING_WEIGHTS_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.scoring.scoring_weights import ScoringWeights


class ScoringWeightsValidator:
    """
    ScoringWeights domain invariant validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        weights: "ScoringWeights",
    ) -> None:
        cls._validate_model_type(weights)

        for model_field in fields(weights):
            field_name = model_field.name
            value = getattr(weights, field_name)

            rules = SCORING_WEIGHTS_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

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
        weights: "ScoringWeights",
    ) -> None:
        from src.domain.scoring.scoring_weights import ScoringWeights

        if not isinstance(weights, ScoringWeights):
            raise TypeError(
                "weights must be a ScoringWeights instance."
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