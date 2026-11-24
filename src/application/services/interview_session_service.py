"""Adaptive interview session orchestration.

One place that runs the interview loop end to end:

    start_session -> next_question -> submit_answer -> next_question -> ...

It composes existing building blocks through their ports:

    - QuestionRepository:   the full question bank (fallback candidate pool)
    - question retriever:   semantic candidates for the current focus (optional)
    - ScoringEngine:        ranks candidates for the current context
    - Evaluator:            scores the candidate's answer (Groq or offline)
    - LevelTransitionService: JR/MID/SENIOR decisions (DECISIONS.md, decision 7)

The session is an immutable value object; every call returns a new session,
so the service itself holds no per-user state and is safe to share.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Sequence
from dataclasses import dataclass, field, replace
from typing import Protocol

from src.application.ports.question_repository import QuestionRepository
from src.application.services.level_transition_service import (
    LevelTransitionService,
)
from src.domain.entities.question import Question
from src.domain.enums.level import Level
from src.domain.evaluation.evaluator import Evaluator
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.scoring.scoring_context import ScoringContext
from src.shared.logging.logger import logger

DEFAULT_MAX_QUESTIONS = 15
DEFAULT_RETRIEVAL_TOP_K = 10


class CandidateRetriever(Protocol):
    """Returns candidate questions relevant to a free-text focus."""

    def __call__(
        self,
        *,
        query: str,
        context: ScoringContext,
        top_k: int,
    ) -> Sequence[Question]: ...


class QuestionScorer(Protocol):
    def score(self, *, question: Question, context: ScoringContext) -> object: ...


@dataclass(frozen=True, slots=True)
class InterviewTurn:
    question: Question
    answer: str
    evaluation: EvaluationResult
    level_before: Level
    level_after: Level


@dataclass(frozen=True, slots=True)
class InterviewSession:
    current_level: Level = Level.JR
    cv_skills: tuple[str, ...] = ()
    max_questions: int = DEFAULT_MAX_QUESTIONS
    turns: tuple[InterviewTurn, ...] = ()
    # Scores collected since the last level change; the transition window
    # restarts after every promotion/demotion so one streak cannot trigger
    # two consecutive jumps.
    scores_at_level: tuple[float, ...] = ()
    pending_question: Question | None = None

    @property
    def asked_question_ids(self) -> frozenset[str]:
        ids = {turn.question.id for turn in self.turns}
        if self.pending_question is not None:
            ids.add(self.pending_question.id)
        return frozenset(ids)

    @property
    def is_finished(self) -> bool:
        return len(self.turns) >= self.max_questions

    @property
    def scores(self) -> tuple[float, ...]:
        return tuple(turn.evaluation.score for turn in self.turns)

    def scoring_context(self) -> ScoringContext:
        return ScoringContext(
            current_level=self.current_level,
            cv_skills=self.cv_skills,
            asked_question_ids=self.asked_question_ids,
            recent_scores=self.scores_at_level,
        )


@dataclass(frozen=True, slots=True)
class AnswerOutcome:
    session: InterviewSession
    turn: InterviewTurn

    @property
    def level_changed(self) -> bool:
        return self.turn.level_before != self.turn.level_after


class InterviewSessionError(RuntimeError):
    pass


@dataclass
class InterviewSessionService:
    question_repository: QuestionRepository
    scoring_engine: QuestionScorer
    evaluator: Evaluator
    level_transition_service: LevelTransitionService = field(
        default_factory=LevelTransitionService,
    )
    retriever: CandidateRetriever | None = None
    retrieval_top_k: int = DEFAULT_RETRIEVAL_TOP_K
    focus_builder: Callable[[InterviewSession], str] | None = None
    _retrieval_disabled: bool = field(default=False, init=False, repr=False)

    def start_session(
        self,
        *,
        starting_level: Level | str = Level.JR,
        cv_skills: Sequence[str] = (),
        max_questions: int = DEFAULT_MAX_QUESTIONS,
    ) -> InterviewSession:
        if max_questions < 1:
            raise InterviewSessionError("max_questions must be at least 1.")
        return InterviewSession(
            current_level=Level(str(starting_level).upper()),
            cv_skills=tuple(skill.strip().lower() for skill in cv_skills if skill.strip()),
            max_questions=max_questions,
        )

    def next_question(self, session: InterviewSession) -> tuple[InterviewSession, Question]:
        if session.pending_question is not None:
            return session, session.pending_question
        if session.is_finished:
            raise InterviewSessionError("Interview is finished.")

        context = session.scoring_context()
        candidates = self._candidates(session=session, context=context)
        if not candidates:
            raise InterviewSessionError("No unasked questions left in the bank.")

        best = max(
            candidates,
            key=lambda q: (self._score(q, context), -_level_distance(q, session.current_level), q.id),
        )
        return replace(session, pending_question=best), best

    def submit_answer(self, session: InterviewSession, *, answer: str) -> AnswerOutcome:
        question = session.pending_question
        if question is None:
            raise InterviewSessionError("No question is waiting for an answer.")
        if not answer.strip():
            raise InterviewSessionError("Answer cannot be empty.")

        evaluation = self.evaluator.evaluate(question=question, answer=answer)

        window = (*session.scores_at_level, float(evaluation.score))
        level_after = self.level_transition_service.transition(
            current_level=session.current_level,
            recent_scores=list(window),
        )
        turn = InterviewTurn(
            question=question,
            answer=answer,
            evaluation=evaluation,
            level_before=session.current_level,
            level_after=level_after,
        )
        next_session = replace(
            session,
            current_level=level_after,
            turns=(*session.turns, turn),
            scores_at_level=() if level_after != session.current_level else window,
            pending_question=None,
        )
        return AnswerOutcome(session=next_session, turn=turn)

    # ------------------------------------------------------------------

    def _candidates(self, *, session: InterviewSession, context: ScoringContext) -> list[Question]:
        """Build the candidate pool, narrowing step by step but never to empty.

        1. unasked questions from the bank
        2. at the current level, if any remain
        3. in the least-covered categories (minimum category diversity rule,
           so a high market weight cannot monopolise the interview)
        4. among those, the ones semantic retrieval considers relevant, if any
        """
        asked = session.asked_question_ids
        pool = [q for q in self.question_repository.list_all() if q.id not in asked]
        pool = _narrow(pool, lambda q: q.level == session.current_level)

        coverage = Counter(str(turn.question.category) for turn in session.turns)
        least = min((coverage[str(q.category)] for q in pool), default=0)
        pool = _narrow(pool, lambda q: coverage[str(q.category)] == least)

        if self.retriever is not None and not self._retrieval_disabled:
            focus = (self.focus_builder or _default_focus)(session)
            try:
                found = self.retriever(query=focus, context=context, top_k=self.retrieval_top_k)
            except Exception as exc:  # noqa: BLE001 - retrieval is optional
                # Missing index, model download failure, ...: keep interviewing
                # from the bank and stop retrying on every question.
                self._retrieval_disabled = True
                logger.warning(
                    "Semantic retrieval failed; continuing without it.",
                    error_type=type(exc).__name__,
                )
            else:
                relevant = {q.id for q in found}
                pool = _narrow(pool, lambda q: q.id in relevant)

        return pool

    def _score(self, question: Question, context: ScoringContext) -> float:
        # Engines return either a float or a breakdown with final_score.
        result = self.scoring_engine.score(question=question, context=context)
        return float(getattr(result, "final_score", result))


def _narrow(pool: list[Question], keep: Callable[[Question], bool]) -> list[Question]:
    """Apply a preference filter; keep the original pool if nothing matches."""
    narrowed = [q for q in pool if keep(q)]
    return narrowed or pool


def _level_distance(question: Question, level: Level) -> int:
    order = [Level.JR, Level.MID, Level.SENIOR]
    return abs(order.index(question.level) - order.index(level))


def _default_focus(session: InterviewSession) -> str:
    """Steer retrieval to categories the candidate has not covered yet."""
    covered = {str(turn.question.category) for turn in session.turns}
    skills = " ".join(session.cv_skills)
    if covered:
        return f"{session.current_level} AI engineer interview question beyond {' '.join(sorted(covered))} {skills}".strip()
    return f"{session.current_level} AI engineer interview question {skills}".strip()
