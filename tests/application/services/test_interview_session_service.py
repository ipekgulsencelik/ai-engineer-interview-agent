"""Behavioural tests for the adaptive interview loop.

Uses the real question bank, the real scoring engine and level transition
policy; only the evaluator is replaced by one that returns scripted scores.
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from src.application.services.interview_session_service import (
    InterviewSession,
    InterviewSessionError,
    InterviewSessionService,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.evaluation.evaluator import Evaluator
from src.domain.results.evaluation_result import EvaluationResult
from src.infrastructure.evaluators.keyword_coverage_evaluator import (
    KeywordCoverageEvaluator,
)
from src.infrastructure.repositories.json_question_repository_builder import (
    JsonQuestionRepositoryBuilder,
)
from src.services.weighted_scoring_engine import WeightedScoringEngine

BANK = Path(__file__).resolve().parents[3] / "data/question_bank/questions.json"


class ScriptedEvaluator(Evaluator):
    def __init__(self, scores: list[float]) -> None:
        self._scores = list(scores)

    def evaluate(self, *, question: Question, answer: str) -> EvaluationResult:
        return EvaluationResult(score=self._scores.pop(0), feedback="scripted")


def make_service(scores: list[float] | None = None, **kwargs) -> InterviewSessionService:
    return InterviewSessionService(
        question_repository=JsonQuestionRepositoryBuilder.build_default(file_path=BANK),
        scoring_engine=WeightedScoringEngine(),
        evaluator=ScriptedEvaluator(scores) if scores is not None else KeywordCoverageEvaluator(),
        **kwargs,
    )


def run(service: InterviewSessionService, session: InterviewSession, answers: int):
    levels = []
    for _ in range(answers):
        session, question = service.next_question(session)
        levels.append((question.level, session.current_level))
        session = service.submit_answer(session, answer="an answer").session
    return session, levels


def test_three_high_scores_promote_one_level() -> None:
    service = make_service([9, 9, 9])
    session = service.start_session(starting_level="MID", max_questions=3)

    session, _ = run(service, session, 3)

    assert session.current_level == Level.SENIOR
    assert [t.level_after for t in session.turns] == [Level.MID, Level.MID, Level.SENIOR]


def test_three_low_scores_demote_one_level() -> None:
    service = make_service([3, 2, 4])
    session = service.start_session(starting_level="MID", max_questions=3)

    session, _ = run(service, session, 3)

    assert session.current_level == Level.JR


def test_a_single_score_never_changes_level() -> None:
    """Warm-up: the first answers cannot move the level (decision 7)."""
    service = make_service([10, 10])
    session = service.start_session(starting_level="JR", max_questions=5)

    session, _ = run(service, session, 2)

    assert session.current_level == Level.JR


def test_window_restarts_after_a_level_change() -> None:
    """Six strong answers move JR->MID->SENIOR, not JR->MID->SENIOR->... per answer."""
    service = make_service([9] * 6)
    session = service.start_session(starting_level="JR", max_questions=6)

    session, _ = run(service, session, 6)

    changes = [i for i, t in enumerate(session.turns) if t.level_before != t.level_after]
    assert changes == [2, 5]
    assert session.current_level == Level.SENIOR


def test_mixed_scores_stay_at_level() -> None:
    service = make_service([6, 7, 5, 6])
    session = service.start_session(starting_level="MID", max_questions=4)

    session, _ = run(service, session, 4)

    assert session.current_level == Level.MID


def test_questions_follow_the_current_level() -> None:
    service = make_service([9, 9, 9, 9])
    session = service.start_session(starting_level="MID", max_questions=4)

    session, levels = run(service, session, 4)

    assert all(question_level == level for question_level, level in levels)
    assert session.turns[-1].question.level == Level.SENIOR


def test_no_question_is_asked_twice() -> None:
    service = make_service([6] * 20)
    session = service.start_session(starting_level="MID", max_questions=20)

    session, _ = run(service, session, 20)

    ids = [t.question.id for t in session.turns]
    assert len(ids) == len(set(ids))


def test_categories_rotate_before_repeating() -> None:
    """Minimum category diversity: 8 questions at one level cover 8 categories."""
    service = make_service([6] * 8)
    session = service.start_session(starting_level="MID", max_questions=8)

    session, _ = run(service, session, 8)

    counts = Counter(str(t.question.category) for t in session.turns)
    assert len(counts) == 8


def test_session_ends_after_max_questions() -> None:
    service = make_service([6, 6])
    session = service.start_session(starting_level="JR", max_questions=2)

    session, _ = run(service, session, 2)

    assert session.is_finished
    with pytest.raises(InterviewSessionError):
        service.next_question(session)


def test_next_question_is_idempotent_until_answered() -> None:
    service = make_service([6])
    session = service.start_session(max_questions=3)

    session, first = service.next_question(session)
    session, again = service.next_question(session)

    assert first.id == again.id


def test_answer_requires_a_pending_question_and_text() -> None:
    service = make_service([6])
    session = service.start_session(max_questions=3)

    with pytest.raises(InterviewSessionError):
        service.submit_answer(session, answer="anything")

    session, _ = service.next_question(session)
    with pytest.raises(InterviewSessionError):
        service.submit_answer(session, answer="   ")


def test_retriever_narrows_choice_without_breaking_diversity() -> None:
    calls = []

    def retriever(*, query, context, top_k):
        calls.append(query)
        bank = JsonQuestionRepositoryBuilder.build_default(file_path=BANK).list_all()
        return [q for q in bank if q.id == "rag_mid_002"]

    service = make_service([6], retriever=retriever)
    session = service.start_session(starting_level="MID", max_questions=3)

    _, question = service.next_question(session)

    assert calls
    assert question.id == "rag_mid_002"


def test_empty_retrieval_falls_back_to_the_bank() -> None:
    service = make_service([6], retriever=lambda **_: [])
    session = service.start_session(starting_level="JR", max_questions=3)

    _, question = service.next_question(session)

    assert question.level == Level.JR


def test_keyword_evaluator_rewards_better_answers() -> None:
    bank = {q.id: q for q in JsonQuestionRepositoryBuilder.build_default(file_path=BANK).list_all()}
    question = bank["rag_jr_001"]
    evaluator = KeywordCoverageEvaluator()

    weak = evaluator.evaluate(question=question, answer="I am not sure.")
    strong = evaluator.evaluate(
        question=question,
        answer=(
            "RAG retrieves relevant documents from a vector store using embeddings. "
            "It injects them into the prompt as context. This grounds answers in "
            "current or private data and reduces hallucination."
        ),
    )

    assert weak.score < 2 < 6 < strong.score
    assert strong.metadata.follow_up_question == question.followup


def test_failing_retriever_does_not_stop_the_interview() -> None:
    calls = []

    def broken(**_):
        calls.append(1)
        raise RuntimeError("index missing")

    service = make_service([6, 6, 6], retriever=broken)
    session = service.start_session(starting_level="JR", max_questions=3)

    session, _ = run(service, session, 3)

    assert len(session.turns) == 3
    assert len(calls) == 1  # disabled after the first failure
