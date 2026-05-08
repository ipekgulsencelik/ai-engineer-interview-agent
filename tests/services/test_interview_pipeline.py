from src.domain.question.question import Question
from src.domain.scoring.scoring_context import ScoringContext
from src.infrastructure.evaluator.mock_evaluator import (
    MockEvaluator,
)
from src.pipelines.interview_pipeline import InterviewPipeline
from src.services.answer_evaluation_service import (
    AnswerEvaluationService,
)
from src.services.level_transition_service import (
    LevelTransitionService,
)
from src.services.question_selection_service import (
    QuestionSelectionService,
)
from src.services.weighted_scoring_engine import (
    WeightedScoringEngine,
)


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


def test_interview_pipeline_runs_successfully() -> None:
    pipeline = InterviewPipeline(
        question_selection_service=QuestionSelectionService(
            scoring_engine=WeightedScoringEngine(),
        ),
        answer_evaluation_service=AnswerEvaluationService(
            evaluator=MockEvaluator(),
        ),
        level_transition_service=LevelTransitionService(),
    )

    context = ScoringContext(current_level="JR")

    result = pipeline.run(
        questions=[make_question()],
        context=context,
        answer="RAG combines retrieval and generation.",
    )

    assert result.evaluation.score == 7
    assert result.next_level.value == "JR"
