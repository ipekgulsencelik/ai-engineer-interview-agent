from __future__ import annotations

from src.application.ports.cv_text_extractor import (
    CVTextExtractor,
)
from src.application.ports.skill_extractor import (
    SkillExtractor,
)
from src.application.services.cv_gap_analysis_service import (
    CVGapAnalysisService,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class CVAnalysisOrchestrationServiceValidator(
    BaseSchemaValidator,
):
    """
    CVAnalysisOrchestrationService validation helper.
    """

    @classmethod
    def validate_dependencies(
        cls,
        *,
        cv_text_extractor: CVTextExtractor,
        skill_extractor: SkillExtractor,
        gap_analysis_service: CVGapAnalysisService,
    ) -> None:
        cls.validate_has_callable(
            value=cv_text_extractor,
            method_name="extract_text",
            field_name="cv_text_extractor",
        )

        cls.validate_has_callable(
            value=skill_extractor,
            method_name="extract_candidate_profile",
            field_name="skill_extractor",
        )

        cls.validate_model_type(
            value=gap_analysis_service,
            expected_type=CVGapAnalysisService,
            field_name="gap_analysis_service",
        )