"""Validation helpers for immutable, typed ValidationRule schema definitions."""

from __future__ import annotations

import math

from src.domain.validation.schema_types import ValidationRule


class BaseSchemaValidator:
    """Apply the attributes of a ValidationRule, never assume a mapping."""

    @staticmethod
    def validate_model_type(
        *,
        value: object,
        expected_type: type,
        field_name: str = "value",
    ) -> None:
        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be an {expected_type.__name__} instance."
            )

    @staticmethod
    def validate_nullable(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if value is None and not rules.nullable:
            raise TypeError(f"{field_name} cannot be None.")

    @staticmethod
    def validate_type(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if rules.reject_bool and isinstance(value, bool):
            raise TypeError(f"{field_name} cannot be bool.")
        if not isinstance(value, rules.expected_type):
            raise TypeError(f"{field_name} has invalid type.")
        if rules.allowed_values is not None:
            try:
                allowed = value in rules.allowed_values
            except TypeError as exc:
                raise TypeError(f"{field_name} must be hashable.") from exc
            if not allowed:
                raise ValueError(f"{field_name} has unsupported value.")

    @staticmethod
    def validate_non_empty_string(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if not rules.non_empty and rules.allow_empty:
            return
        candidate = value.strip() if rules.strip and isinstance(value, str) else value
        if not candidate:
            raise ValueError(f"{field_name} cannot be empty.")
        if rules.min_length is not None or rules.max_length is not None:
            if not hasattr(candidate, "__len__"):
                raise TypeError(f"{field_name} must have a length.")
            length = len(candidate)
            if rules.min_length is not None and length < rules.min_length:
                raise ValueError(f"{field_name} is shorter than allowed.")
            if rules.max_length is not None and length > rules.max_length:
                raise ValueError(f"{field_name} is longer than allowed.")

    @staticmethod
    def validate_numeric_bounds(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if not (
            rules.finite or rules.min_value is not None or rules.max_value is not None
        ):
            return
        try:
            numeric_value = float(value)
        except (TypeError, ValueError) as exc:
            raise TypeError(f"{field_name} must be numeric.") from exc
        if rules.finite and not math.isfinite(numeric_value):
            raise ValueError(f"{field_name} must be finite.")
        if rules.min_value is not None and numeric_value < rules.min_value:
            raise ValueError(f"{field_name} must be >= {rules.min_value}.")
        if rules.max_value is not None and numeric_value > rules.max_value:
            raise ValueError(f"{field_name} must be <= {rules.max_value}.")

    @staticmethod
    def validate_tuple_items(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule,
    ) -> None:
        if not isinstance(value, (tuple, list)):
            return
        for item in value:
            if rules.item_type is not None and not isinstance(item, rules.item_type):
                raise TypeError(f"{field_name} items have invalid type.")
            if rules.strip_items and isinstance(item, str) and not item.strip():
                raise ValueError(f"{field_name} items cannot be empty.")

    @staticmethod
    def validate_has_callable(
        *,
        value: object,
        method_name: str,
        field_name: str,
    ) -> None:
        if not callable(getattr(value, method_name, None)):
            raise TypeError(f"{field_name} must implement callable {method_name}().")
