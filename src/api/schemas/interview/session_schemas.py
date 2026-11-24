from __future__ import annotations

from pydantic import BaseModel, Field

from src.api.schemas.evaluation.enums import QuestionLevel

MAX_ANSWER_CHARS = 8000


class StartInterviewRequest(BaseModel):
    starting_level: QuestionLevel = QuestionLevel.JR
    cv_skills: list[str] = Field(default_factory=list, max_length=100)
    max_questions: int = Field(default=15, ge=1, le=40)


class SubmitAnswerRequest(BaseModel):
    answer: str = Field(min_length=1, max_length=MAX_ANSWER_CHARS)


class QuestionView(BaseModel):
    id: str
    text: str
    category: str
    level: str
    question_type: str
    difficulty: int


class EvaluationView(BaseModel):
    score: float
    technical_accuracy: float
    depth: float
    communication: float
    feedback: str
    missing_keywords: list[str]
    follow_up_question: str | None
    rubric_version: str


class InterviewProgress(BaseModel):
    current_level: str
    answered: int
    max_questions: int
    finished: bool


class StartInterviewResponse(BaseModel):
    session_id: str
    progress: InterviewProgress
    question: QuestionView


class SubmitAnswerResponse(BaseModel):
    evaluation: EvaluationView
    level_before: str
    level_after: str
    progress: InterviewProgress
    next_question: QuestionView | None


class CategoryScore(BaseModel):
    category: str
    average_score: float
    answered: int


class TurnView(BaseModel):
    question: QuestionView
    answer: str
    evaluation: EvaluationView
    level_after: str


class InterviewSummaryResponse(BaseModel):
    session_id: str
    progress: InterviewProgress
    average_score: float | None
    categories: list[CategoryScore]
    turns: list[TurnView]
