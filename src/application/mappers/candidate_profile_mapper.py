from __future__ import annotations

from typing import Any

from src.application.extractors.candidate_profile_payload_extractor import (
    CandidateProfilePayloadExtractor,
)
from src.domain.enums.level import (
    Level,
)
from src.domain.value_objects.candidate_profile import (
    CandidateProfile,
)


class CandidateProfileMapper:
    """
    Candidate profile payload mapper.

    Bu mapper:
        - validated payload değerlerini domain modeline dönüştürür
        - payload extraction detaylarını bilmez
        - validation logic içermez
        - sadece CandidateProfile construction sorumluluğu taşır
    """

    @staticmethod
    def from_payload(
        *,
        payload: dict[str, Any],
    ) -> CandidateProfile:
        return CandidateProfile(
            detected_level=Level(
                CandidateProfilePayloadExtractor.get_detected_level(
                    payload=payload,
                )
            ),
            skills=CandidateProfilePayloadExtractor.get_skills(
                payload=payload,
            ),
            weak_skills=(
                CandidateProfilePayloadExtractor.get_weak_skills(
                    payload=payload,
                )
            ),
            target_roles=(
                CandidateProfilePayloadExtractor.get_target_roles(
                    payload=payload,
                )
            ),
            years_of_experience=(
                CandidateProfilePayloadExtractor.get_years_of_experience(
                    payload=payload,
                )
            ),
            summary=CandidateProfilePayloadExtractor.get_summary(
                payload=payload,
            ),
            education=CandidateProfilePayloadExtractor.get_education(
                payload=payload,
            ),
            projects=CandidateProfilePayloadExtractor.get_projects(
                payload=payload,
            ),
        )