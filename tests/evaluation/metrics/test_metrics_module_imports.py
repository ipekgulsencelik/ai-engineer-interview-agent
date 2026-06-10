from __future__ import annotations

import importlib
from pathlib import Path


def test_all_metrics_modules_should_import_successfully() -> None:
    module_paths = sorted(
        path
        for path in Path("src/evaluation/metrics").rglob("*.py")
        if path.name != "__pycache__"
    )

    failures: list[str] = []
    for path in module_paths:
        module_name = ".".join(path.with_suffix("").parts)
        try:
            importlib.import_module(module_name)
        except Exception as exc:  # pragma: no cover - assertion reports details
            failures.append(f"{module_name}: {type(exc).__name__}: {exc}")

    assert failures == []
