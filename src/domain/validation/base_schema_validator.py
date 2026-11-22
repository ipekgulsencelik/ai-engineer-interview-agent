"""Validation helpers for immutable, typed ValidationRule schema definitions."""

from __future__ import annotations

import math
from collections.abc import Mapping
from typing import Any

from src.domain.validation.schema_types import ValidationRule


class BaseSchemaValidator:
    """Apply typed rules; adapt legacy mapping callers at the boundary."""

    @staticmethod
    def _normalize(
        rules: ValidationRule | Mapping[str, Any],
    ) -> ValidationRule:
        if isinstance(rules, ValidationRule):
            return rules
        if not isinstance(rules, Mapping):
            raise TypeError("rules must be a ValidationRule or mapping.")
        return ValidationRule(
            expected_type=rules.get(
                "expected_type", rules.get("type", object)
            ),
            nullable=bool(rules.get("nullable", False)),
            non_empty=bool(rules.get("non_empty", False)),
            strip=bool(rules.get("strip", rules.get("non_empty", False))),
            allow_empty=bool(rules.get("allow_empty", True)),
            item_type=rules.get("item_type"),
            strip_items=bool(
                rules.get("strip_items", rules.get("non_empty_items", False))
            ),
            reject_bool_items=bool(rules.get("reject_bool_items", False)),
            reject_bool=bool(rules.get("reject_bool", False)),
            finite=bool(rules.get("finite", False)),
            min_value=rules.get("min_value"),
            max_value=rules.get("max_value"),
            min_length=rules.get("min_length"),
            max_length=rules.get("max_length"),
            allowed_values=rules.get("allowed_values"),
        )

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
        rules: ValidationRule | Mapping[str, Any],
    ) -> None:
        rules = BaseSchemaValidator._normalize(rules)
        if value is None and not rules.nullable:
            raise TypeError(f"{field_name} cannot be None.")

    @staticmethod
    def validate_type(
        *,
        field_name: str,
        value: object,
        rules: ValidationRule | Mapping[str, Any],
    ) -> None:
        rules = BaseSchemaValidator._normalize(rules)
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
        rules: ValidationRule | Mapping[str, Any],
    ) -> None:
        rules = BaseSchemaValidator._normalize(rules)
        if (
            not rules.non_empty
            and rules.allow_empty
            and rules.min_length is None
            and rules.max_length is None
        ):
            return
        candidate = (
            value.strip()
            if isinstance(value, str)
            and (rules.strip or rules.non_empty or not rules.allow_empty)
            else value
        )
        if (rules.non_empty or not rules.allow_empty) and not candidate:
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
        rules: ValidationRule | Mapping[str, Any],
    ) -> None:
        rules = BaseSchemaValidator._normalize(rules)
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
        rules: ValidationRule | Mapping[str, Any],
    ) -> None:
        rules = BaseSchemaValidator._normalize(rules)
        if not isinstance(value, (tuple, list)):
            return
        for item in value:
            if rules.reject_bool_items and isinstance(item, bool):
                raise TypeError(f"{field_name} items cannot be bool.")
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
