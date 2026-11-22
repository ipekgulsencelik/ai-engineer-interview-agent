"""Application-layer validation for the scored ranking snapshot.

Keep this validator beside its application model: domain code must not import
application modules in order to validate an application-specific snapshot.
"""

from __future__ import annotations

import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.application.rankers.scored_candidate import ScoredCandidate


class ScoredCandidateValidator:
    """Validate field metadata before a candidate enters the ranking pipeline."""

    @classmethod
    def validate(cls, candidate: ScoredCandidate) -> None:
        cls._validate_model_type(candidate)

        for model_field in fields(candidate):
            field_name = model_field.name
            value = getattr(candidate, field_name)
            rules = model_field.metadata

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

            if rules.get("finite", False):
                cls._validate_finite(field_name=field_name, value=value)

            if "min_value" in rules:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=rules["min_value"],
                )

    @staticmethod
    def _validate_model_type(candidate: object) -> None:
        from src.application.rankers.scored_candidate import ScoredCandidate

        if not isinstance(candidate, ScoredCandidate):
            raise TypeError("candidate must be a ScoredCandidate instance.")

    @staticmethod
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: Any,
    ) -> None:
        if expected_type is None:
            return

        if isinstance(value, bool):
            raise TypeError(f"{field_name} cannot be bool.")

        if not isinstance(value, expected_type):
            raise TypeError(f"{field_name} must be {expected_type}.")

    @staticmethod
    def _validate_finite(*, field_name: str, value: float) -> None:
        if not math.isfinite(value):
            raise ValueError(f"{field_name} must be finite.")

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: float,
        min_value: float,
    ) -> None:
        if value < min_value:
            raise ValueError(f"{field_name} must be >= {min_value}.")
