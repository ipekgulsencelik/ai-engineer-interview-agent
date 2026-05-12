from src.domain.constants.scoring import (
    HIGH_PERFORMANCE_DIFFICULTY_SCORES,
    LOW_PERFORMANCE_DIFFICULTY_SCORES,
    MID_PERFORMANCE_DIFFICULTY_SCORES,
)
from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.policies.difficulty_score_policy import DifficultyScorePolicy
from src.domain.scoring.scoring_context import ScoringContext


def build_question(*, difficulty: int) -> Question:
    return Question(
        id="difficulty_q",
        text="Explain vector databases.",
        category=QuestionCategory.RAG,
        level=Level.MID,
        difficulty=difficulty,
        question_type=QuestionType.CONCEPTUAL,
        expected_points=["indexing"],
        keywords=["vector-db"],
    )


def build_context(*, recent_scores: tuple[float, ...]) -> ScoringContext:
    return ScoringContext(
        current_level=Level.MID,
        cv_skills=("python",),
        recent_scores=recent_scores,
    )


def test_compute_returns_high_performance_mapping_for_hard_question() -> None:
    policy = DifficultyScorePolicy()

    result = policy.compute(
        question=build_question(difficulty=Difficulty.HARD),
        context=build_context(recent_scores=(9.0, 8.5, 8.0)),
    )

    assert result == HIGH_PERFORMANCE_DIFFICULTY_SCORES[Difficulty.HARD]


def test_compute_returns_low_performance_mapping_for_easy_question() -> None:
    policy = DifficultyScorePolicy()

    result = policy.compute(
        question=build_question(difficulty=Difficulty.EASY),
        context=build_context(recent_scores=(2.0, 3.5, 4.0)),
    )

    assert result == LOW_PERFORMANCE_DIFFICULTY_SCORES[Difficulty.EASY]


def test_compute_defaults_to_mid_mapping_when_recent_scores_missing() -> None:
    policy = DifficultyScorePolicy()

    result = policy.compute(
        question=build_question(difficulty=Difficulty.MEDIUM),
        context=build_context(recent_scores=()),
    )

    assert result == MID_PERFORMANCE_DIFFICULTY_SCORES[Difficulty.MEDIUM]


def test_compute_uses_mid_performance_mapping_for_average_mid_scores() -> None:
    policy = DifficultyScorePolicy()

    result = policy.compute(
        question=build_question(difficulty=Difficulty.HARD),
        context=build_context(recent_scores=(5.0, 6.5, 7.0)),
    )

    assert result == MID_PERFORMANCE_DIFFICULTY_SCORES[Difficulty.HARD]