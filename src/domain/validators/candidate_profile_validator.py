from __future__ import annotations

from src.domain.validation.candidate_profile_validation_schema import (
    CANDIDATE_PROFILE_SCHEMA,
)
from src.domain.validation.schema_validator import (
    SchemaValidator,
)


class CandidateProfileValidator:
    """
    CandidateProfile invariant validator.
    """

    @classmethod
    def validate(
        cls,
        profile: object,
    ) -> None:
        """
        Validate CandidateProfile invariants.
        """

        SchemaValidator.validate_object(
            obj=profile,
            schema=CANDIDATE_PROFILE_SCHEMA,
        )