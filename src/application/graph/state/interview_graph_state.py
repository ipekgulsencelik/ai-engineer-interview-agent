from __future__ import annotations

from typing import TypedDict

from src.application.graph.state.graph_state_types import (
    CandidateAnswer,
    FeedbackText,
    LevelName,
    QuestionId,
    QuestionText,
    SearchQuery,
)


class InterviewGraphState(
    TypedDict,
    total=False,
):
    """
    LangGraph interview workflow state.
    """

    query: SearchQuery

    current_question_id: QuestionId

    current_question_text: QuestionText

    candidate_answer: CandidateAnswer

    evaluation_score: float

    feedback: FeedbackText

    follow_up_question: QuestionText

    current_level: LevelName

    target_difficulty: int