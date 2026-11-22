"""Typed schema rules must validate entities, reject bad input and preserve dates."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from src.domain.validation.common_rules import (
    NON_EMPTY_STRING_RULE,
    NON_NEGATIVE_NUMBER_RULE,
    OPTIONAL_STRING_RULE,
    STRING_TUPLE_RULE,
)
from src.domain.validation.schema_validator import SchemaValidator


def test_typed_rule_objects_are_supported() -> None:
    SchemaValidator.validate(
        values={"name": "candidate", "count": 0, "note": None},
        schema={
            "name": NON_EMPTY_STRING_RULE,
            "count": NON_NEGATIVE_NUMBER_RULE,
            "note": OPTIONAL_STRING_RULE,
        },
    )


@pytest.mark.parametrize(
    ("value", "rule"),
    [
        ("  ", NON_EMPTY_STRING_RULE),
        (-1, NON_NEGATIVE_NUMBER_RULE),
        (True, NON_NEGATIVE_NUMBER_RULE),
        (float("nan"), NON_NEGATIVE_NUMBER_RULE),
        ((1,), STRING_TUPLE_RULE),
    ],
)
def test_typed_rules_reject_invalid_values(value: object, rule: object) -> None:
    from src.domain.validation.schema_rules import ValidationRule

    assert isinstance(rule, ValidationRule)
    with pytest.raises(ValueError):
        SchemaValidator.validate(
            values={"field": value},
            schema={"field": rule},
        )


def test_required_datetime_rule_rejects_iso_string() -> None:
    from src.domain.validation.common_rules import DATETIME_OBJECT_RULE

    with pytest.raises(ValueError):
        SchemaValidator.validate(
            values={"when": "2026-11-22T00:00:00Z"},
            schema={"when": DATETIME_OBJECT_RULE},
        )
    SchemaValidator.validate(
        values={"when": datetime(2026, 11, 22, tzinfo=UTC)},
        schema={"when": DATETIME_OBJECT_RULE},
    )
