"""Manual, evidence-only DR readiness CLI; no live cluster mutations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.application.operations.dr_readiness import (
    ReadinessEvaluator,
    ReadinessPolicy,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluate independently gathered PostgreSQL HA/DR evidence"
    )
    parser.add_argument("--evidence", required=True, type=Path)
    parser.add_argument("--max-rpo-seconds", type=float, default=300)
    parser.add_argument("--max-rto-seconds", type=float, default=900)
    args = parser.parse_args()
    try:
        if not args.evidence.is_file() or args.evidence.stat().st_size > 1_048_576:
            raise ValueError("evidence must be an existing JSON file <= 1 MiB")
        with args.evidence.open("r", encoding="utf-8") as stream:
            evidence = json.load(stream)
        policy = ReadinessPolicy(
            max_rpo_seconds=args.max_rpo_seconds,
            max_rto_seconds=args.max_rto_seconds,
        )
        report = ReadinessEvaluator(policy=policy).evaluate(evidence)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        # Never echo input JSON, file path, DSN, or potentially sensitive
        # exception text to CI or production logs.
        print(json.dumps({"ready": False, "error": "invalid or incomplete evidence"}))
        return 2
    print(json.dumps(report.to_dict(), sort_keys=True))
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
