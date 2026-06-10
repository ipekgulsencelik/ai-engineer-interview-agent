from __future__ import annotations

from typing import Protocol, runtime_checkable

from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


@runtime_checkable
class SkillExtractor(Protocol):
    """
    Provider-independent candidate profile extraction contract.

    Bu protocol:
        - CV text içinden structured candidate profile extraction davranışını tanımlar
        - application katmanını LLM/provider implementasyonlarından izole eder
        - structural typing sayesinde loose coupling sağlar

    Implementasyonlar infrastructure katmanında yer almalıdır.
    """

    def extract_candidate_profile(
        self,
        *,
        cv_text: str,
    ) -> CandidateProfile:
        """
        CV text içinden structured candidate profile çıkarır.
        """
        ...