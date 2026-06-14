from __future__ import annotations

import importlib


def test_summary_trend_direction_module_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.enums.summary_trend_direction")

    assert module is not None
