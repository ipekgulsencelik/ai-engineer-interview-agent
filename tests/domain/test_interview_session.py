import pytest

from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult


def build_result(score: float = 8.5) -> EvaluationResult:
    return EvaluationResult(
        score=score,
        feedback="Strong answer.",
    )


def build_session(**overrides) -> InterviewSession:
    payload = {
        "session_id": "session-1",
        "current_level": Level.MID,
        "asked_question_ids": ("q1", "q2"),
        "completed_results": (build_result(),),
        "recent_scores": (8.5, 7.0),
    }
    payload.update(overrides)
    return InterviewSession(**payload)


def test_interview_session_can_be_created() -> None:
    session = build_session()

    assert session.session_id == "session-1"
    assert session.current_level == Level.MID
    assert session.asked_question_ids == ("q1", "q2")
    assert len(session.completed_results) == 1
    assert session.recent_scores == (8.5, 7.0)


def test_interview_session_is_immutable() -> None:
    session = build_session()

    with pytest.raises(Exception):
        session.session_id = "new-id"


@pytest.mark.parametrize("value", ["", "   "])
def test_interview_session_rejects_empty_session_id(value: str) -> None:
    with pytest.raises(ValueError, match="session_id cannot be empty"):
        build_session(session_id=value)


def test_interview_session_rejects_invalid_level() -> None:
    with pytest.raises(TypeError):
        build_session(current_level="MID")


def test_interview_session_rejects_invalid_question_ids_type() -> None:
    with pytest.raises(TypeError):
        build_session(asked_question_ids=["q1"])


def test_interview_session_rejects_invalid_question_id_item_type() -> None:
    with pytest.raises(TypeError):
        build_session(asked_question_ids=("q1", 123))


def test_interview_session_rejects_empty_question_id() -> None:
    with pytest.raises(ValueError):
        build_session(asked_question_ids=("q1", " "))


def test_interview_session_rejects_invalid_completed_results_type() -> None:
    with pytest.raises(TypeError):
        build_session(completed_results=["invalid"])


def test_interview_session_rejects_invalid_recent_scores_type() -> None:
    with pytest.raises(TypeError):
        build_session(recent_scores=["8.5"])


def test_interview_session_rejects_bool_recent_scores() -> None:
    with pytest.raises(TypeError):
        build_session(recent_scores=(8.0, True))


@pytest.mark.parametrize("value", [-1.0, 11.0])
def test_interview_session_rejects_out_of_range_scores(value: float) -> None:
    with pytest.raises(ValueError):
        build_session(recent_scores=(value,))


@pytest.mark.parametrize("value", [float("inf"), float("-inf"), float("nan")])
def test_interview_session_rejects_non_finite_scores(value: float) -> None:
    with pytest.raises(ValueError):
        build_session(recent_scores=(value,))