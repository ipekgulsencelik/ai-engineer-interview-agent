from __future__ import annotations

import inspect

import pytest

MODULE_UNDER_TEST = "src.evaluation.reporting.validators.brand_theme_validator"


def test_module_imports_and_exposes_public_api() -> None:
    module = pytest.importorskip(MODULE_UNDER_TEST, exc_type=ImportError)

    public_members = {
        name: value for name, value in vars(module).items() if not name.startswith("_")
    }

    assert public_members, "module should expose a public API"
    assert any(
        inspect.isclass(value) or inspect.isfunction(value) or name.isupper()
        for name, value in public_members.items()
    )


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
