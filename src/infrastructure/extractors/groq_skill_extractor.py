from __future__ import annotations

from src.application.factories.llm_request_factory import (
    LLMRequestFactory,
)
from src.application.parsers.candidate_profile_response_parser import (
    CandidateProfileResponseParser,
)
from src.application.ports.cv_skill_extraction_prompt_builder import (
    CVSkillExtractionPromptBuilder,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.application.ports.skill_extractor import (
    SkillExtractor,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)
from src.infrastructure.validators.groq_skill_extractor_validator import (
    GroqSkillExtractorValidator,
)


class GroqSkillExtractor(
    SkillExtractor,
):
    """
    Groq-based candidate profile extraction adapter.
    """

    def __init__(
        self,
        *,
        llm_client: LLMClient,
        prompt_builder: CVSkillExtractionPromptBuilder,
        response_parser: CandidateProfileResponseParser,
    ) -> None:
        GroqSkillExtractorValidator.validate_dependencies(
            llm_client=llm_client,
            prompt_builder=prompt_builder,
            response_parser=response_parser,
        )

        self._llm_client = llm_client
        self._prompt_builder = prompt_builder
        self._response_parser = response_parser

    def extract_candidate_profile(
        self,
        *,
        cv_text: str,
    ) -> CandidateProfile:
        GroqSkillExtractorValidator.validate_input(
            cv_text=cv_text,
        )

        prompt = self._prompt_builder.build(
            cv_text=cv_text,
        )

        request = LLMRequestFactory.create(
            prompt=prompt,
        )

        response = self._llm_client.generate(
            request=request,
        )

        return self._response_parser.parse(
            response=response,
        )