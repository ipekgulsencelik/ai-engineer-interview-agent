from __future__ import annotations

import importlib


def test_executive_summary_schema_module_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.schemas.executive_summary_schema")

    assert module is not None
