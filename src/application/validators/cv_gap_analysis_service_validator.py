from __future__ import annotations

from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CVGapAnalysisServiceValidator(
    BaseSchemaValidator,
):
    """
    CVGapAnalysisService validation helper.
    """

    @classmethod
    def validate_profile(
        cls,
        *,
        profile: CandidateProfile,
    ) -> None:
        cls.validate_model_type(
            value=profile,
            expected_type=CandidateProfile,
            field_name="profile",
        )