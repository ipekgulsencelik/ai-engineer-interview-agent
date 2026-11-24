from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, HTTPException, status

from src.api.dependencies.interview_dependencies import (
    InterviewSessionServiceDependency,
    InterviewSessionStoreDependency,
)
from src.api.schemas.interview.session_schemas import (
    CategoryScore,
    EvaluationView,
    InterviewProgress,
    InterviewSummaryResponse,
    QuestionView,
    StartInterviewRequest,
    StartInterviewResponse,
    SubmitAnswerRequest,
    SubmitAnswerResponse,
    TurnView,
)
from src.api.storage.interview_session_store import (
    InterviewSessionNotFoundError,
)
from src.application.services.interview_session_service import (
    InterviewSession,
    InterviewSessionError,
)
from src.domain.entities.question import Question
from src.domain.results.evaluation_result import EvaluationResult

router = APIRouter(
    prefix="/interview",
    tags=["Interview"],
)


@router.post(
    "/sessions",
    response_model=StartInterviewResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_interview(
    request: StartInterviewRequest,
    service: InterviewSessionServiceDependency,
    store: InterviewSessionStoreDependency,
) -> StartInterviewResponse:
    """Start an adaptive interview and return its first question."""
    session = service.start_session(
        starting_level=request.starting_level.value,
        cv_skills=request.cv_skills,
        max_questions=request.max_questions,
    )
    session, question = _next_question_or_409(service, session)
    session_id = store.create(session)
    return StartInterviewResponse(
        session_id=session_id,
        progress=_progress(session),
        question=_question_view(question),
    )


@router.post(
    "/sessions/{session_id}/answers",
    response_model=SubmitAnswerResponse,
)
def submit_answer(
    session_id: str,
    request: SubmitAnswerRequest,
    service: InterviewSessionServiceDependency,
    store: InterviewSessionStoreDependency,
) -> SubmitAnswerResponse:
    """Grade the answer to the pending question and return the next one."""
    session = _load(store, session_id)
    try:
        outcome = service.submit_answer(session, answer=request.answer)
    except InterviewSessionError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc

    session = outcome.session
    next_question = None
    if not session.is_finished:
        session, next_question = _next_question_or_409(service, session)
    store.save(session_id, session)

    return SubmitAnswerResponse(
        evaluation=_evaluation_view(outcome.turn.evaluation),
        level_before=str(outcome.turn.level_before),
        level_after=str(outcome.turn.level_after),
        progress=_progress(session),
        next_question=_question_view(next_question) if next_question else None,
    )


@router.get(
    "/sessions/{session_id}",
    response_model=InterviewSummaryResponse,
)
def get_interview(
    session_id: str,
    store: InterviewSessionStoreDependency,
) -> InterviewSummaryResponse:
    """Return progress, per-category scores and the answered turns."""
    session = _load(store, session_id)

    by_category: dict[str, list[float]] = defaultdict(list)
    for turn in session.turns:
        by_category[str(turn.question.category)].append(turn.evaluation.score)

    scores = session.scores
    return InterviewSummaryResponse(
        session_id=session_id,
        progress=_progress(session),
        average_score=round(sum(scores) / len(scores), 2) if scores else None,
        categories=sorted(
            (
                CategoryScore(
                    category=category,
                    average_score=round(sum(values) / len(values), 2),
                    answered=len(values),
                )
                for category, values in by_category.items()
            ),
            key=lambda item: item.average_score,
        ),
        turns=[
            TurnView(
                question=_question_view(turn.question),
                answer=turn.answer,
                evaluation=_evaluation_view(turn.evaluation),
                level_after=str(turn.level_after),
            )
            for turn in session.turns
        ],
    )


def _load(store, session_id: str) -> InterviewSession:
    try:
        return store.get(session_id)
    except InterviewSessionNotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Interview session not found.") from exc


def _next_question_or_409(service, session: InterviewSession) -> tuple[InterviewSession, Question]:
    try:
        return service.next_question(session)
    except InterviewSessionError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


def _progress(session: InterviewSession) -> InterviewProgress:
    return InterviewProgress(
        current_level=str(session.current_level),
        answered=len(session.turns),
        max_questions=session.max_questions,
        finished=session.is_finished,
    )


def _question_view(question: Question) -> QuestionView:
    return QuestionView(
        id=question.id,
        text=question.text,
        category=str(question.category),
        level=str(question.level),
        question_type=str(question.question_type),
        difficulty=question.difficulty,
    )


def _evaluation_view(evaluation: EvaluationResult) -> EvaluationView:
    return EvaluationView(
        score=evaluation.score,
        technical_accuracy=evaluation.technical_accuracy,
        depth=evaluation.depth,
        communication=evaluation.communication,
        feedback=evaluation.feedback,
        missing_keywords=list(evaluation.metadata.missing_keywords),
        follow_up_question=evaluation.metadata.follow_up_question,
        rubric_version=evaluation.metadata.rubric_version,
    )
