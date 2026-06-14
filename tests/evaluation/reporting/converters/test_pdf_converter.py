from __future__ import annotations

import importlib


def test_pdf_converter_module_imports() -> None:
    module = importlib.import_module("src.evaluation.reporting.converters.pdf_converter")

    assert module is not None
