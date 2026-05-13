from dataclasses import FrozenInstanceError

import pytest

from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.interview.interview_session import InterviewSession
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.results.interview_step_result import InterviewStepResult
from src.domain.results.selection_breakdown import SelectionBreakdown
from src.domain.results.selection_result import SelectionResult


def build_question() -> Question:
    return Question(
        id="q-1",
        text="Explain vector databases.",
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=2,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=["embedding", "retrieval"],
        keywords=["vector db"],
    )


def build_evaluation() -> EvaluationResult:
    return EvaluationResult(score=8.0, feedback="Good depth.")


def build_selection_result(question: Question) -> SelectionResult:
    breakdown = SelectionBreakdown(
        level_score=0.8,
        market_score=0.7,
        cv_gap_score=0.6,
        difficulty_score=0.7,
        diversity_score=0.9,
        fatigue_score=0.95,
        final_score=3.2,
    )
    return SelectionResult(question=question, final_score=3.2, breakdown=breakdown)


def build_session() -> InterviewSession:
    return InterviewSession(session_id="s-1", current_level=Level.MID)


def test_interview_step_result_can_be_created() -> None:
    question = build_question()
    result = InterviewStepResult(
        selection_result=build_selection_result(question),
        question=question,
        answer="Vector DB stores embeddings for semantic retrieval.",
        evaluation_result=build_evaluation(),
        next_level=Level.SENIOR,
        updated_session=build_session(),
    )

    assert result.next_level == Level.SENIOR
    assert result.selection_result.question == question


def test_interview_step_result_is_immutable() -> None:
    question = build_question()
    result = InterviewStepResult(
        selection_result=build_selection_result(question),
        question=question,
        answer="answer",
        evaluation_result=build_evaluation(),
        next_level=Level.MID,
        updated_session=build_session(),
    )

    with pytest.raises(FrozenInstanceError):
        result.next_level = Level.SENIOR


def test_interview_step_result_rejects_empty_answer() -> None:
    question = build_question()

    with pytest.raises(ValueError, match="answer cannot be empty"):
        InterviewStepResult(
            selection_result=build_selection_result(question),
            question=question,
            answer="   ",
            evaluation_result=build_evaluation(),
            next_level=Level.MID,
            updated_session=build_session(),
        )


def test_interview_step_result_rejects_question_mismatch() -> None:
    question = build_question()
    other = Question(
        id="q-2",
        text="Explain chunking.",
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=2,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=["split"],
        keywords=["chunk"],
    )

    with pytest.raises(ValueError, match="selection_result.question must match question"):
        InterviewStepResult(
            selection_result=build_selection_result(question),
            question=other,
            answer="answer",
            evaluation_result=build_evaluation(),
            next_level=Level.MID,
            updated_session=build_session(),
        )