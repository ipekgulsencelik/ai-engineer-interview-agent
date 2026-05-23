from __future__ import annotations

from typing import Any

from src.application.extractors.payload_field_extractor import (
    PayloadFieldExtractor,
)


class CandidateProfilePayloadExtractor:
    """
    Candidate profile payload extraction helper.
    """

    @staticmethod
    def get_detected_level(
        *,
        payload: dict[str, Any],
    ) -> str:
        return (
            PayloadFieldExtractor.get_required_string(
                payload,
                "detected_level",
            )
        )

    @staticmethod
    def get_skills(
        *,
        payload: dict[str, Any],
    ) -> tuple[str, ...]:
        return (
            PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "skills",
            )
            or ()
        )

    @staticmethod
    def get_weak_skills(
        *,
        payload: dict[str, Any],
    ) -> tuple[str, ...]:
        return (
            PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "weak_skills",
            )
            or ()
        )

    @staticmethod
    def get_target_roles(
        *,
        payload: dict[str, Any],
    ) -> tuple[str, ...]:
        return (
            PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "target_roles",
            )
            or ()
        )

    @staticmethod
    def get_years_of_experience(
        *,
        payload: dict[str, Any],
    ) -> float:
        return (
            PayloadFieldExtractor.get_optional_float(
                payload,
                "years_of_experience",
            )
            or 0.0
        )

    @staticmethod
    def get_summary(
        *,
        payload: dict[str, Any],
    ) -> str | None:
        return (
            PayloadFieldExtractor.get_optional_string(
                payload,
                "summary",
            )
        )

    @staticmethod
    def get_education(
        *,
        payload: dict[str, Any],
    ) -> tuple[str, ...]:
        return (
            PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "education",
            )
            or ()
        )

    @staticmethod
    def get_projects(
        *,
        payload: dict[str, Any],
    ) -> tuple[str, ...]:
        return (
            PayloadFieldExtractor.get_optional_string_tuple(
                payload,
                "projects",
            )
            or ()
        )