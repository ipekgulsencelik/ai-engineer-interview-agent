from __future__ import annotations

from src.application.parsers.candidate_profile_response_parser import (
    CandidateProfileResponseParser,
)
from src.application.ports.cv_skill_extraction_prompt_builder import (
    CVSkillExtractionPromptBuilder,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.domain.schemas.cv_extraction_schema import (
    CV_TEXT_RULE,
)
from src.domain.validation.base_schema_validator import (
    BaseSchemaValidator,
)


class GroqSkillExtractorValidator(
    BaseSchemaValidator,
):
    """
    GroqSkillExtractor validation helper.
    """

    @classmethod
    def validate_dependencies(
        cls,
        *,
        llm_client: LLMClient,
        prompt_builder: CVSkillExtractionPromptBuilder,
        response_parser: CandidateProfileResponseParser,
    ) -> None:
        cls.validate_has_callable(
            value=llm_client,
            method_name="generate",
            field_name="llm_client",
        )

        cls.validate_has_callable(
            value=prompt_builder,
            method_name="build",
            field_name="prompt_builder",
        )

        cls.validate_model_type(
            value=response_parser,
            expected_type=CandidateProfileResponseParser,
            field_name="response_parser",
        )

    @classmethod
    def validate_input(
        cls,
        *,
        cv_text: str,
    ) -> None:
        cls.validate_type(
            field_name="cv_text",
            value=cv_text,
            rules=CV_TEXT_RULE,
        )

        cls.validate_non_empty_string(
            field_name="cv_text",
            value=cv_text,
            rules=CV_TEXT_RULE,
        )