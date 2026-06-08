from __future__ import annotations

from src.domain.schemas.cv_gap_analysis_result_schema import (
    CV_GAP_ANALYSIS_RESULT_SCHEMA,
)
from src.domain.validators.schema_validator import (
    SchemaValidator,
)


class CVGapAnalysisResultValidator:
    """
    CVGapAnalysisResult invariant validator.
    """

    @classmethod
    def validate(
        cls,
        result: object,
    ) -> None:
        """
        Validate CVGapAnalysisResult invariants.
        """

        SchemaValidator.validate_object(
            obj=result,
            schema=CV_GAP_ANALYSIS_RESULT_SCHEMA,
        )