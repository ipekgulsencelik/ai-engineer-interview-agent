from src.domain.constants.scoring import (
    ASKED_QUESTION_DIVERSITY_SCORE,
    DEFAULT_FATIGUE_SCORE,
    EXACT_LEVEL_MATCH_SCORE,
    MAX_SCORE,
    MIN_SCORE,
    ONE_LEVEL_DISTANCE_SCORE,
    TWO_LEVEL_DISTANCE_SCORE,
    UNASKED_QUESTION_DIVERSITY_SCORE,
    UNKNOWN_SKILL_GAP_SCORE,
)
from src.domain.entities.question import Question
from src.domain.enums.difficulty import Difficulty
from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.policies.cv_gap_score_policy import CvGapScorePolicy
from src.domain.policies.diversity_score_policy import DiversityScorePolicy
from src.domain.policies.fatigue_score_policy import FatigueScorePolicy
from src.domain.policies.level_score_policy import LevelScorePolicy
from src.domain.policies.market_score_policy import MarketScorePolicy
from src.domain.policies.unasked_question_filter_policy import UnaskedQuestionFilterPolicy
from src.domain.scoring.scoring_context import ScoringContext


def build_question(**overrides) -> Question:
    payload = {
        "id": "q-1",
        "text": "Explain retrieval augmented generation.",
        "category": QuestionCategory.RAG,
        "level": Level.MID,
        "difficulty": Difficulty.MEDIUM,
        "question_type": QuestionType.CONCEPTUAL,
        "expected_points": ["retrieval", "generation"],
        "keywords": ["rag", "vector db"],
        "market_weight": 0.8,
    }
    payload.update(overrides)
    return Question(**payload)


def build_context(**overrides) -> ScoringContext:
    payload = {
        "current_level": Level.MID,
        "cv_skills": ("python", "rag"),
        "asked_question_ids": frozenset(),
        "recent_scores": (6.0, 6.5),
    }
    payload.update(overrides)
    return ScoringContext(**payload)


def test_level_score_policy_returns_expected_scores_by_level_distance() -> None:
    policy = LevelScorePolicy()
    context = build_context(current_level=Level.MID)

    exact = policy.compute(question=build_question(level=Level.MID), context=context)
    one_step = policy.compute(question=build_question(level=Level.JR), context=context)
    two_step = policy.compute(question=build_question(level=Level.SENIOR), context=build_context(current_level=Level.JR))

    assert exact == EXACT_LEVEL_MATCH_SCORE
    assert one_step == ONE_LEVEL_DISTANCE_SCORE
    assert two_step == TWO_LEVEL_DISTANCE_SCORE


def test_market_score_policy_clamps_values_to_min_max() -> None:
    policy = MarketScorePolicy()
    context = build_context()

    assert policy.compute(question=build_question(market_weight=0.0), context=context) == MIN_SCORE
    assert policy.compute(question=build_question(market_weight=0.6), context=context) == 0.6
    assert policy.compute(question=build_question(market_weight=1.0), context=context) == MAX_SCORE


def test_cv_gap_score_policy_handles_missing_and_partial_skill_overlap() -> None:
    policy = CvGapScorePolicy()

    no_keywords = policy.compute(
        question=build_question(keywords=[]),
        context=build_context(cv_skills=("python",)),
    )
    no_cv = policy.compute(
        question=build_question(keywords=["rag", "vector db"]),
        context=build_context(cv_skills=()),
    )
    partial_gap = policy.compute(
        question=build_question(keywords=["rag", "vector db"]),
        context=build_context(cv_skills=("rag",)),
    )

    assert no_keywords == MIN_SCORE
    assert no_cv == UNKNOWN_SKILL_GAP_SCORE
    assert partial_gap == 0.5


def test_diversity_score_policy_scores_asked_and_unasked_questions() -> None:
    policy = DiversityScorePolicy()

    asked_score = policy.compute(
        question=build_question(id="q-asked"),
        context=build_context(asked_question_ids=frozenset({"q-asked"})),
    )
    unasked_score = policy.compute(
        question=build_question(id="q-new"),
        context=build_context(asked_question_ids=frozenset({"q-asked"})),
    )

    assert asked_score == ASKED_QUESTION_DIVERSITY_SCORE
    assert unasked_score == UNASKED_QUESTION_DIVERSITY_SCORE


def test_fatigue_score_policy_returns_expected_values_for_score_buckets() -> None:
    policy = FatigueScorePolicy()

    no_history = policy.compute(
        question=build_question(difficulty=Difficulty.HARD),
        context=build_context(recent_scores=()),
    )
    low_perf_hard = policy.compute(
        question=build_question(difficulty=Difficulty.HARD),
        context=build_context(recent_scores=(2.0, 3.0, 4.0)),
    )
    high_perf_hard = policy.compute(
        question=build_question(difficulty=Difficulty.HARD),
        context=build_context(recent_scores=(8.0, 9.0, 8.5)),
    )

    assert no_history == DEFAULT_FATIGUE_SCORE
    assert low_perf_hard == MIN_SCORE
    assert high_perf_hard == MAX_SCORE


def test_unasked_question_filter_policy_filters_without_mutating_input() -> None:
    policy = UnaskedQuestionFilterPolicy()
    q1 = build_question(id="q1")
    q2 = build_question(id="q2")
    q3 = build_question(id="q3")
    original = [q1, q2, q3]

    filtered = policy.apply(
        questions=original,
        asked_question_ids={"q2"},
    )

    assert [q.id for q in filtered] == ["q1", "q3"]
    assert [q.id for q in original] == ["q1", "q2", "q3"]