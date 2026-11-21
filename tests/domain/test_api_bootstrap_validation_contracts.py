"""Regression coverage for legacy CV and search schemas used at API boot."""

from __future__ import annotations

import pytest

from src.domain.enums.level import Level
from src.domain.enums.question_category import QuestionCategory
from src.domain.enums.question_type import QuestionType
from src.domain.results.cv_gap_analysis_result import CVGapAnalysisResult
from src.domain.retrieval.search_filters import SearchFilters
from src.domain.value_objects.candidate_profile import CandidateProfile


def test_candidate_profile_validates_with_dataclass_rule_contract() -> None:
    profile = CandidateProfile(
        detected_level=Level.MID,
        skills=("Python", "RAG"),
        weak_skills=(),
        years_of_experience=3.5,
    )
    assert profile.skills == ("Python", "RAG")


@pytest.mark.parametrize("invalid_years", [-1.0, float("nan"), True])
def test_candidate_profile_rejects_invalid_years(invalid_years: object) -> None:
    with pytest.raises(ValueError):
        CandidateProfile(
            detected_level=Level.MID,
            years_of_experience=invalid_years,  # type: ignore[arg-type]
        )


def test_cv_gap_result_validates_alignment_score() -> None:
    result = CVGapAnalysisResult(
        matched_skills=("Python",),
        missing_skills=("MLOps",),
        alignment_score=0.5,
        recommended_focus_areas=("MLOps",),
    )
    assert result.alignment_score == 0.5
    with pytest.raises(ValueError):
        CVGapAnalysisResult(
            matched_skills=(),
            missing_skills=(),
            alignment_score=1.5,
            recommended_focus_areas=(),
        )


def test_search_filters_accept_real_domain_enums() -> None:
    filters = SearchFilters(
        category=QuestionCategory.RAG,
        level=Level.JR,
        question_type=QuestionType.CONCEPTUAL,
        min_difficulty=1,
        max_difficulty=8,
    )
    assert filters.category is QuestionCategory.RAG


def test_search_filters_reject_invalid_difficulty_order() -> None:
    with pytest.raises(ValueError, match="min_difficulty"):
        SearchFilters(min_difficulty=9, max_difficulty=4)
