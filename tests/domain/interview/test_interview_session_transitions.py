from datetime import UTC, datetime

import pytest

from src.domain.enums.level import Level
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult


def build_result(score: float = 8.0) -> EvaluationResult:
    return EvaluationResult(
        score=score,
        feedback="Solid answer.",
    )


def build_session() -> InterviewSession:
    return InterviewSession(
        session_id="session-1",
        current_level=Level.JR,
        asked_question_ids=(),
        completed_results=(),
        recent_scores=(),
        started_at=datetime.now(UTC),
    )


def test_with_completed_turn_returns_new_session_instance() -> None:
    session = build_session()

    updated = session.with_completed_turn(
        question_id="q1",
        result=build_result(7.5),
    )

    assert updated is not session


def test_with_completed_turn_appends_question_result_and_score() -> None:
    session = build_session()

    updated = session.with_completed_turn(
        question_id="q1",
        result=build_result(7.5),
    )

    assert updated.asked_question_ids == ("q1",)
    assert len(updated.completed_results) == 1
    assert updated.completed_results[0].score == 7.5
    assert updated.recent_scores == (7.5,)


def test_with_completed_turn_strips_question_id() -> None:
    session = build_session()

    updated = session.with_completed_turn(
        question_id="   q-123   ",
        result=build_result(),
    )

    assert updated.asked_question_ids == ("q-123",)


def test_with_completed_turn_rejects_empty_question_id() -> None:
    session = build_session()

    with pytest.raises(ValueError, match="question_id cannot be empty"):
        session.with_completed_turn(
            question_id="   ",
            result=build_result(),
        )


def test_with_level_returns_new_session_with_updated_level() -> None:
    session = build_session()

    updated = session.with_level(level=Level.SENIOR)

    assert updated is not session
    assert updated.current_level == Level.SENIOR
    assert session.current_level == Level.JR


def test_with_level_preserves_other_state_fields() -> None:
    session = InterviewSession(
        session_id="session-1",
        current_level=Level.MID,
        asked_question_ids=("q1",),
        completed_results=(build_result(8.2),),
        recent_scores=(8.2,),
        started_at=datetime.now(UTC),
    )

    updated = session.with_level(level=Level.SENIOR)

    assert updated.session_id == session.session_id
    assert updated.asked_question_ids == session.asked_question_ids
    assert updated.completed_results == session.completed_results
    assert updated.recent_scores == session.recent_scores
    assert updated.started_at == session.started_at