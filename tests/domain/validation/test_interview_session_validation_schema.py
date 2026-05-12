import math

import pytest

from src.domain.constants.evaluation import (
    MAX_EVALUATION_SCORE,
    MIN_EVALUATION_SCORE,
)
from src.domain.enums.level import Level
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.validation.interview_session_validation_schema import (
    INTERVIEW_SESSION_VALIDATION_SCHEMA,
)


def test_schema_contains_expected_fields() -> None:
    expected_fields = {
        "session_id",
        "current_level",
        "asked_question_ids",
        "completed_results",
        "recent_scores",
        "started_at",
    }

    assert set(INTERVIEW_SESSION_VALIDATION_SCHEMA.keys()) == expected_fields


def test_session_id_rule_is_non_empty_string() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["session_id"]

    assert rule["type"] is str
    assert rule["non_empty"] is True


def test_current_level_rule_uses_level_enum() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["current_level"]

    assert rule["type"] is Level


def test_asked_question_ids_rule_uses_tuple_of_strings() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["asked_question_ids"]

    assert rule["type"] is tuple
    assert rule["item_type"] is str


def test_completed_results_rule_uses_tuple_of_evaluation_result() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["completed_results"]

    assert rule["type"] is tuple
    assert rule["item_type"] is EvaluationResult


def test_recent_scores_rule_uses_numeric_finite_range() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["recent_scores"]

    assert rule["type"] is tuple
    assert rule["item_type"] == (int, float)
    assert rule["finite"] is True
    assert rule["min_value"] == MIN_EVALUATION_SCORE
    assert rule["max_value"] == MAX_EVALUATION_SCORE


def test_recent_scores_range_is_valid() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["recent_scores"]

    min_value = rule["min_value"]
    max_value = rule["max_value"]

    assert isinstance(min_value, float)
    assert isinstance(max_value, float)
    assert math.isfinite(min_value)
    assert math.isfinite(max_value)
    assert min_value <= max_value


def test_started_at_rule_is_timezone_aware_datetime() -> None:
    rule = INTERVIEW_SESSION_VALIDATION_SCHEMA["started_at"]

    from datetime import datetime

    assert rule["type"] is datetime
    assert rule["timezone_aware"] is True