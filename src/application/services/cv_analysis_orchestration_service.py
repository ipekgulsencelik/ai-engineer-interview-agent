from __future__ import annotations

from pathlib import Path

from src.application.ports.cv_text_extractor import (
    CVTextExtractor,
)
from src.application.ports.skill_extractor import (
    SkillExtractor,
)
from src.application.services.cv_gap_analysis_service import (
    CVGapAnalysisService,
)
from src.application.validators.cv_analysis_orchestration_service_validator import (
    CVAnalysisOrchestrationServiceValidator,
)
from src.domain.results.cv_gap_analysis_result import (
    CVGapAnalysisResult,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CVAnalysisOrchestrationService:
    """
    End-to-end CV intelligence orchestration.
    """

    def __init__(
        self,
        *,
        cv_text_extractor: CVTextExtractor,
        skill_extractor: SkillExtractor,
        gap_analysis_service: CVGapAnalysisService,
    ) -> None:
        CVAnalysisOrchestrationServiceValidator.validate_dependencies(
            cv_text_extractor=cv_text_extractor,
            skill_extractor=skill_extractor,
            gap_analysis_service=gap_analysis_service,
        )

        self._cv_text_extractor = (
            cv_text_extractor
        )

        self._skill_extractor = (
            skill_extractor
        )

        self._gap_analysis_service = (
            gap_analysis_service
        )

    def analyze_cv(
        self,
        *,
        file_path: str | Path,
    ) -> tuple[
        CandidateProfile,
        CVGapAnalysisResult,
    ]:
        cv_text = (
            self._cv_text_extractor.extract_text(
                file_path=file_path,
            )
        )

        profile = (
            self._skill_extractor.extract_candidate_profile(
                cv_text=cv_text,
            )
        )

        gap_analysis = (
            self._gap_analysis_service.analyze(
                profile=profile,
            )
        )

        return (
            profile,
            gap_analysis,
        )