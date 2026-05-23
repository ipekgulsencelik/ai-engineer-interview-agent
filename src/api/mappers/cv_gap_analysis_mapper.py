from __future__ import annotations

from src.api.schemas.cv_analysis_response import (
    CVAnalysisResponse,
)
from src.domain.results.cv_gap_analysis_result import (
    CVGapAnalysisResult,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CVGapAnalysisResponseMapper:
    """
    CV analysis domain -> API response mapper.
    """

    @staticmethod
    def from_profile_and_gap_analysis(
        *,
        profile: CandidateProfile,
        gap_analysis: CVGapAnalysisResult,
    ) -> CVAnalysisResponse:
        return CVAnalysisResponse(
            detected_level=(
                profile.detected_level
            ),
            years_of_experience=(
                profile.years_of_experience
            ),
            skills=list(
                profile.skills,
            ),
            weak_skills=list(
                profile.weak_skills,
            ),
            matched_skills=list(
                gap_analysis.matched_skills,
            ),
            missing_skills=list(
                gap_analysis.missing_skills,
            ),
            alignment_score=(
                gap_analysis.alignment_score
            ),
            recommended_focus_areas=list(
                gap_analysis.recommended_focus_areas,
            ),
        )