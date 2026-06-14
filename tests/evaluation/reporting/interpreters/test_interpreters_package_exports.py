from __future__ import annotations

import importlib


def test_package_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.interpreters")

    assert module is not None
