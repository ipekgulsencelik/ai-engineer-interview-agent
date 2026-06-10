from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace

import pytest


def _stub_module(name: str, **attrs: object) -> None:
    module = ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module


def _load_calculator_module():
    class RepeatPenaltyPolicy:
        @staticmethod
        def calculate(*, repeat_count):
            return 0.1 * repeat_count

    class NormalizedScoreClamper:
        @staticmethod
        def clamp(*, score):
            return max(0.0, min(1.0, score))

    _stub_module("src.domain.constants.diversity_scoring", DEFAULT_DIVERSITY_SCORE=1.0)
    _stub_module("src.domain.entities.question", Question=object)
    _stub_module("src.domain.scoring.normalized_score_clamper", NormalizedScoreClamper=NormalizedScoreClamper)
    _stub_module("src.domain.scoring.repeat_penalty_policy", RepeatPenaltyPolicy=RepeatPenaltyPolicy)
    _stub_module("src.domain.value_objects.interview_coverage", InterviewCoverage=object)

    spec = importlib.util.spec_from_file_location("diversity_calc_under_test", Path("src/domain/scoring/diversity_score_calculator.py"))
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_calculate_returns_default_when_no_questions_asked() -> None:
    module = _load_calculator_module()
    q = SimpleNamespace(category=SimpleNamespace(value="backend"), question_type=SimpleNamespace(value="technical"))
    coverage = SimpleNamespace(total_questions=0, category_counts={}, question_type_counts={})

    assert module.DiversityScoreCalculator.calculate(question=q, coverage=coverage) == 1.0


def test_calculate_reduces_score_with_repetition() -> None:
    module = _load_calculator_module()
    q = SimpleNamespace(category=SimpleNamespace(value="backend"), question_type=SimpleNamespace(value="technical"))
    coverage = SimpleNamespace(total_questions=3, category_counts={"backend": 2}, question_type_counts={"technical": 1})

    assert module.DiversityScoreCalculator.calculate(question=q, coverage=coverage) == pytest.approx(0.7)
