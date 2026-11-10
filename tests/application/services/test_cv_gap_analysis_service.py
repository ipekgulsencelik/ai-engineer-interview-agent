"""Real CV gap service integration without process-global sys.modules stubs."""

from __future__ import annotations

import pytest

import src.application.services.cv_gap_analysis_service as gap_module
from src.domain.enums.level import Level
from src.domain.value_objects.candidate_profile import CandidateProfile


def test_analyze_computes_matched_missing_and_focus_areas(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        gap_module, "MARKET_REQUIRED_SKILLS",
        frozenset({"python", "sql", "docker"}),
    )
    service = gap_module.CVGapAnalysisService()
    profile = CandidateProfile(
        detected_level=Level.MID,
        skills=("Python", " Git ", "Docker"),
    )
    result = service.analyze(profile=profile)
    assert result.matched_skills == ("docker", "python")
    assert result.missing_skills == ("sql",)
    assert result.recommended_focus_areas == ("sql",)
    assert result.alignment_score == 2 / 3


def test_invalid_profile_is_rejected_by_real_validator() -> None:
    with pytest.raises(TypeError):
        gap_module.CVGapAnalysisService().analyze(
            profile=object(),  # type: ignore[arg-type]
        )
