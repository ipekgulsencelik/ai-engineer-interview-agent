from __future__ import annotations

from dataclasses import fields
from typing import TYPE_CHECKING, Any

from src.domain.validation.scoring_signals_validation_schema import (
    SCORING_SIGNALS_VALIDATION_SCHEMA,
)

if TYPE_CHECKING:
    from src.domain.scoring.scoring_signals import ScoringSignals


class ScoringSignalsValidator:
    """
    ScoringSignals domain invariant validation işlemlerini yapar.
    """

    @classmethod
    def validate(
        cls,
        signals: "ScoringSignals",
    ) -> None:
        cls._validate_model_type(signals)

        for model_field in fields(signals):
            field_name = model_field.name
            value = getattr(signals, field_name)

            rules = SCORING_SIGNALS_VALIDATION_SCHEMA.get(
                field_name,
                {},
            )

            nullable = rules.get("nullable", False)

            if value is None:
                if nullable:
                    continue

                raise TypeError(
                    f"{field_name} cannot be None."
                )

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=rules.get("type"),
            )

    @staticmethod
    def _validate_model_type(
        signals: "ScoringSignals",
    ) -> None:
        from src.domain.scoring.scoring_signals import ScoringSignals

        if not isinstance(signals, ScoringSignals):
            raise TypeError(
                "signals must be a ScoringSignals instance."
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

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type}."
            )