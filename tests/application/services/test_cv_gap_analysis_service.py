from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType


def _stub_module(name: str, **attrs: object) -> None:
    module = ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module


def _load_service_module():
    required = {"python", "sql", "docker"}

    class SkillNormalizer:
        @staticmethod
        def normalize_many(*, skills):
            return {skill.strip().lower() for skill in skills}

    class CVAlignmentScoreCalculator:
        @staticmethod
        def calculate(*, matched_count, required_count):
            return matched_count / required_count

    class CVGapAnalysisServiceValidator:
        @staticmethod
        def validate_profile(*, profile):
            return None

    class CVGapAnalysisResult:
        def __init__(self, *, matched_skills, missing_skills, alignment_score, recommended_focus_areas):
            self.matched_skills = matched_skills
            self.missing_skills = missing_skills
            self.alignment_score = alignment_score
            self.recommended_focus_areas = recommended_focus_areas

    _stub_module("src.domain.constants.market_skills", MARKET_REQUIRED_SKILLS=required)
    _stub_module("src.domain.normalization.skill_normalizer", SkillNormalizer=SkillNormalizer)
    _stub_module("src.domain.results.cv_gap_analysis_result", CVGapAnalysisResult=CVGapAnalysisResult)
    _stub_module("src.domain.scoring.cv_alignment_score_calculator", CVAlignmentScoreCalculator=CVAlignmentScoreCalculator)
    _stub_module("src.application.services.validators.cv_gap_analysis_service_validator", CVGapAnalysisServiceValidator=CVGapAnalysisServiceValidator)
    _stub_module("src.domain.value_objects.candidate_profile", CandidateProfile=object)

    spec = importlib.util.spec_from_file_location("cv_gap_service_under_test", Path("src/application/services/cv_gap_analysis_service.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_analyze_computes_matched_missing_and_focus_areas() -> None:
    module = _load_service_module()
    service = module.CVGapAnalysisService()

    class Profile:
        skills = ("Python", " Git ", "Docker")

    result = service.analyze(profile=Profile())

    assert result.matched_skills == ("docker", "python")
    assert result.missing_skills == ("sql",)
    assert result.recommended_focus_areas == ("sql",)
    assert result.alignment_score == 2 / 3
