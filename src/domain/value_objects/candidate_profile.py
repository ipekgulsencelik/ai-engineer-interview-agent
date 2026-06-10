from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field

from src.domain.enums.level import (
    Level,
)
from src.domain.validators.candidate_profile_validator import (
    CandidateProfileValidator,
)


@dataclass(
    frozen=True,
    slots=True,
)
class CandidateProfile:
    """
    Normalized candidate profile domain model.

    Bu model:
        - CV parsing pipeline
        - LLM extraction pipeline
        - interview adaptation
        - scoring/context generation

    süreçlerinde kullanılan provider-independent
    candidate snapshot modelidir.
    """

    detected_level: Level

    skills: tuple[str, ...] = field(
        default_factory=tuple,
    )

    weak_skills: tuple[str, ...] = field(
        default_factory=tuple,
    )

    target_roles: tuple[str, ...] = field(
        default_factory=tuple,
    )

    years_of_experience: float = 0.0

    summary: str | None = None

    education: tuple[str, ...] = field(
        default_factory=tuple,
    )

    projects: tuple[str, ...] = field(
        default_factory=tuple,
    )

    def __post_init__(self) -> None:
        CandidateProfileValidator.validate(
            self,
        )