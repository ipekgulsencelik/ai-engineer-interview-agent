import pytest

from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.validators.interview_session_validator import (
    InterviewSessionValidator,
)


def build_result(score: float = 8.0) -> EvaluationResult:
    return EvaluationResult(
        score=score,
        feedback="Good answer.",
    )


def build_session(**overrides) -> InterviewSession:
    payload = {
        "session_id": "session-1",
        "current_level": Level.MID,
        "asked_question_ids": ("q1", "q2"),
        "completed_results": (build_result(),),
        "recent_scores": (8.0, 7.5),
    }
    payload.update(overrides)
    return InterviewSession(**payload)


def test_validate_accepts_valid_session() -> None:
    session = build_session()
    InterviewSessionValidator.validate(session)


def test_validate_rejects_non_session_model() -> None:
    with pytest.raises(TypeError, match="InterviewSession"):
        InterviewSessionValidator.validate(object())  # type: ignore[arg-type]


@pytest.mark.parametrize("value", ["", "   "])
def test_validate_rejects_empty_session_id(value: str) -> None:
    with pytest.raises(ValueError, match="session_id"):
        build_session(session_id=value)


def test_validate_rejects_invalid_level_type() -> None:
    with pytest.raises(TypeError, match="current_level"):
        build_session(current_level="MID")  # type: ignore[arg-type]


def test_validate_rejects_non_tuple_question_ids() -> None:
    with pytest.raises(TypeError, match="asked_question_ids"):
        build_session(asked_question_ids=["q1"])  # type: ignore[arg-type]


def test_validate_rejects_non_string_question_id_item() -> None:
    with pytest.raises(TypeError, match="asked_question_ids"):
        build_session(asked_question_ids=("q1", 2))  # type: ignore[arg-type]


def test_validate_rejects_empty_question_id_item() -> None:
    with pytest.raises(ValueError, match="asked_question_ids"):
        build_session(asked_question_ids=("q1", "  "))


def test_validate_rejects_non_tuple_completed_results() -> None:
    with pytest.raises(TypeError, match="completed_results"):
        build_session(completed_results=["invalid"])  # type: ignore[arg-type]


def test_validate_rejects_invalid_completed_result_item() -> None:
    with pytest.raises(TypeError, match="completed_results"):
        build_session(completed_results=("invalid",))  # type: ignore[arg-type]


def test_validate_rejects_non_tuple_recent_scores() -> None:
    with pytest.raises(TypeError, match="recent_scores"):
        build_session(recent_scores=["8.0"])  # type: ignore[arg-type]


def test_validate_rejects_bool_in_recent_scores() -> None:
    with pytest.raises(TypeError, match="recent_scores"):
        build_session(recent_scores=(8.0, True))  # type: ignore[arg-type]


@pytest.mark.parametrize("value", [-1.0, 11.0])
def test_validate_rejects_out_of_range_recent_scores(value: float) -> None:
    with pytest.raises(ValueError, match="recent_scores"):
        build_session(recent_scores=(value,))


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_validate_rejects_non_finite_recent_scores(value: float) -> None:
    with pytest.raises(ValueError, match="recent_scores"):
        build_session(recent_scores=(value,))