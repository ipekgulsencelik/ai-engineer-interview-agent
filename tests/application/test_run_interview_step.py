from src.application.use_cases.run_interview_step import (
    RunInterviewStepUseCase,
)
from src.domain.entities.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.infrastructure.evaluator.mock_evaluator import MockEvaluator
from src.services.answer_evaluation_service import AnswerEvaluationService
from src.services.level_transition_service import LevelTransitionService
from src.services.question_selection_service import QuestionSelectionService
from src.services.weighted_scoring_engine import WeightedScoringEngine


def make_question() -> Question:
    return Question(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[],
        keywords=[],
    )


def test_run_interview_step_use_case_executes_successfully() -> None:
    use_case = RunInterviewStepUseCase(
        question_selection_service=QuestionSelectionService(
            scoring_engine=WeightedScoringEngine(),
        ),
        answer_evaluation_service=AnswerEvaluationService(
            evaluator=MockEvaluator(),
        ),
        level_transition_service=LevelTransitionService(),
    )

    result = use_case.execute(
        questions=[make_question()],
        context=ScoringContext(current_level="JR"),
        answer="RAG combines retrieval and generation.",
    )

    assert result.evaluation.score == 7
    assert result.next_level == "JR"
