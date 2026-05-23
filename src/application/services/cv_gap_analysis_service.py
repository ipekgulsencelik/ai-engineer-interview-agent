from __future__ import annotations

from src.domain.constants.market_skills import (
    MARKET_REQUIRED_SKILLS,
)
from src.domain.normalization.skill_normalizer import (
    SkillNormalizer,
)
from src.domain.results.cv_gap_analysis_result import (
    CVGapAnalysisResult,
)
from src.domain.scoring.cv_alignment_score_calculator import (
    CVAlignmentScoreCalculator,
)
from src.application.services.validators.cv_gap_analysis_service_validator import (
    CVGapAnalysisServiceValidator,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CVGapAnalysisService:
    """
    Candidate market gap analysis service.
    """

    def analyze(
        self,
        *,
        profile: CandidateProfile,
    ) -> CVGapAnalysisResult:
        CVGapAnalysisServiceValidator.validate_profile(
            profile=profile,
        )

        normalized_skills = (
            SkillNormalizer.normalize_many(
                skills=profile.skills,
            )
        )

        matched_skills = (
            MARKET_REQUIRED_SKILLS
            & normalized_skills
        )

        missing_skills = (
            MARKET_REQUIRED_SKILLS
            - normalized_skills
        )

        alignment_score = (
            CVAlignmentScoreCalculator.calculate(
                matched_count=len(
                    matched_skills,
                ),
                required_count=len(
                    MARKET_REQUIRED_SKILLS,
                ),
            )
        )

        sorted_matched_skills = tuple(
            sorted(matched_skills)
        )

        sorted_missing_skills = tuple(
            sorted(missing_skills)
        )

        return CVGapAnalysisResult(
            matched_skills=sorted_matched_skills,
            missing_skills=sorted_missing_skills,
            alignment_score=alignment_score,
            recommended_focus_areas=(
                sorted_missing_skills
            ),
        )