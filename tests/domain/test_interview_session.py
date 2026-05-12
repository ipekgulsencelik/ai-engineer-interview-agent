import pytest

from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult


def build_result(score: float = 7.5) -> EvaluationResult:
    return EvaluationResult(
        score=score,
        feedback="Good",
        technical_accuracy=7.0,
        depth=7.0,
        communication=8.0,
    )


def test_session_initialization() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.MID,
    )

    assert session.session_id == "s1"
    assert session.current_level == Level.MID
    assert session.asked_question_ids == ()


def test_with_completed_turn_returns_new_session() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.JR,
    )

    updated = session.with_completed_turn(
        question_id=" q1 ",
        result=build_result(8.0),
    )

    assert updated is not session
    assert updated.asked_question_ids == ("q1",)
    assert updated.completed_results[0].score == 8.0
    assert updated.recent_scores == (8.0,)


def test_with_level_returns_new_session() -> None:
    session = InterviewSession(
        session_id="s1",
        current_level=Level.JR,
    )

    updated = session.with_level(level=Level.SENIOR)

    assert updated.current_level == Level.SENIOR
    assert session.current_level == Level.JR


def test_session_rejects_empty_session_id() -> None:
    with pytest.raises(ValueError):
        InterviewSession(
            session_id="",
            current_level=Level.JR,
        )
