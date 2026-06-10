from __future__ import annotations

from functools import cached_property

from src.application.parsers.candidate_profile_response_parser import (
    CandidateProfileResponseParser,
)
from src.application.ports.llm_client import (
    LLMClient,
)
from src.application.services.cv_analysis_orchestration_service import (
    CVAnalysisOrchestrationService,
)
from src.application.services.cv_gap_analysis_service import (
    CVGapAnalysisService,
)
from src.infrastructure.containers.base_container import (
    BaseContainer,
)
from src.infrastructure.extractors.groq_skill_extractor import (
    GroqSkillExtractor,
)
from src.infrastructure.extractors.pdfplumber_cv_text_extractor import (
    PdfPlumberCVTextExtractor,
)
from src.infrastructure.prompting.cv_skill_extraction_prompt_builder import (
    DefaultCVSkillExtractionPromptBuilder,
)


class CVContainer(BaseContainer):
    """
    CV analysis dependency container.
    """

    def __init__(
        self,
        *,
        llm_client: LLMClient,
    ) -> None:
        self._llm_client = llm_client

    @cached_property
    def cv_text_extractor(
        self,
    ) -> PdfPlumberCVTextExtractor:
        return PdfPlumberCVTextExtractor()

    @cached_property
    def cv_gap_analysis_service(
        self,
    ) -> CVGapAnalysisService:
        return CVGapAnalysisService()

    @cached_property
    def candidate_profile_response_parser(
        self,
    ) -> CandidateProfileResponseParser:
        return CandidateProfileResponseParser()

    @cached_property
    def cv_skill_extraction_prompt_builder(
        self,
    ) -> DefaultCVSkillExtractionPromptBuilder:
        return DefaultCVSkillExtractionPromptBuilder()

    @cached_property
    def skill_extractor(
        self,
    ) -> GroqSkillExtractor:
        return GroqSkillExtractor(
            llm_client=self._llm_client,
            prompt_builder=self.cv_skill_extraction_prompt_builder,
            response_parser=self.candidate_profile_response_parser,
        )

    @cached_property
    def cv_analysis_orchestration_service(
        self,
    ) -> CVAnalysisOrchestrationService:
        return CVAnalysisOrchestrationService(
            cv_text_extractor=self.cv_text_extractor,
            skill_extractor=self.skill_extractor,
            gap_analysis_service=self.cv_gap_analysis_service,
        )