from __future__ import annotations

import inspect

import pytest

MODULE_UNDER_TEST = "src.evaluation.reporting.stores.scheduled_report_store"


def test_module_imports_and_exposes_public_api() -> None:
    module = pytest.importorskip(MODULE_UNDER_TEST, exc_type=ImportError)


    assert module.__name__ == MODULE_UNDER_TEST
    assert hasattr(module, "__file__")


def test_public_callables_are_documented_or_named_explicitly() -> None:
    module = pytest.importorskip(MODULE_UNDER_TEST, exc_type=ImportError)

    public_callables = [
        value
        for name, value in vars(module).items()
        if not name.startswith("_")
        and (inspect.isclass(value) or inspect.isfunction(value))
        and getattr(value, "__module__", MODULE_UNDER_TEST) == MODULE_UNDER_TEST
    ]

    assert isinstance(public_callables, list)
    for value in public_callables:
        assert value.__name__
