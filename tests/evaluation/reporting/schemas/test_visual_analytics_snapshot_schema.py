from __future__ import annotations

import importlib


def test_visual_analytics_snapshot_schema_module_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.schemas.visual_analytics_snapshot_schema")

    assert module is not None
