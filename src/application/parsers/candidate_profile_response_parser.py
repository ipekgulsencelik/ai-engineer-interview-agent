from __future__ import annotations

from src.application.mappers.candidate_profile_mapper import (
    CandidateProfileMapper,
)
from src.application.models.llm_response import (
    LLMResponse,
)
from src.application.parsers.json_response_parser import (
    JsonResponseParser,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CandidateProfileResponseParser:
    """
    LLMResponse -> CandidateProfile parser.

    Bu parser:
        - raw LLM response text'ini parse eder
        - parsed payload'u CandidateProfile domain modeline dönüştürür
        - extraction veya validation logic içermez
    """

    def parse(
        self,
        *,
        response: LLMResponse,
    ) -> CandidateProfile:
        payload = JsonResponseParser.parse_object(
            raw_text=response.text,
        )

        return CandidateProfileMapper.from_payload(
            payload=payload,
        )