"""Every module under src/ must import.

Refactors that move or delete a module used to leave dangling imports that no
test noticed (the importing modules were never exercised). This test imports
every module, so a broken import fails CI immediately.

Modules that are known to be broken today are listed in
known_broken_modules.txt. The list may only shrink: a listed module that starts
importing again fails the test until its line is removed.

A module whose import fails only because an optional third-party package is not
installed in the current environment is skipped, not failed.
"""

from __future__ import annotations

import importlib
import logging
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
KNOWN_BROKEN_FILE = Path(__file__).with_name("known_broken_modules.txt")

# Entry-point scripts that render or run on import; importing them here would
# execute the app (and leak Streamlit runtime state into other tests).
SCRIPTS = frozenset({"src.ui.app"})


def _all_modules() -> list[str]:
    modules = []
    for path in sorted(SRC.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        parts = path.relative_to(ROOT).with_suffix("").parts
        if parts[-1] == "__init__":
            parts = parts[:-1]
        module = ".".join(parts)
        if module not in SCRIPTS:
            modules.append(module)
    return modules


def _known_broken() -> set[str]:
    return {
        line.strip()
        for line in KNOWN_BROKEN_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def _missing_third_party(exc: BaseException) -> str | None:
    """Return the missing top-level package if exc is a third-party ImportError."""
    if isinstance(exc, ModuleNotFoundError) and exc.name:
        top = exc.name.split(".")[0]
        if top != "src":
            return top
    return None


ALL_MODULES = _all_modules()
KNOWN_BROKEN = _known_broken()


def test_known_broken_list_only_names_real_modules() -> None:
    stale = sorted(KNOWN_BROKEN - set(ALL_MODULES))
    assert not stale, f"Remove deleted modules from the known-broken list: {stale}"


@pytest.mark.parametrize("module", ALL_MODULES)
def test_module_imports(module: str) -> None:
    logging.disable(logging.CRITICAL)
    try:
        importlib.import_module(module)
    except Exception as exc:  # noqa: BLE001 - any failure is the signal
        missing = _missing_third_party(exc)
        if missing is not None:
            pytest.skip(f"optional dependency not installed: {missing}")
        if module in KNOWN_BROKEN:
            pytest.xfail(f"known broken: {type(exc).__name__}: {exc}")
        raise
    finally:
        logging.disable(logging.NOTSET)

    assert module not in KNOWN_BROKEN, (
        f"{module} imports now; remove it from {KNOWN_BROKEN_FILE.name}"
    )
