from __future__ import annotations

import importlib


def test_protocols_module_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.exporters.protocols")

    assert module is not None
