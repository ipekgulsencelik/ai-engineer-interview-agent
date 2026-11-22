"""Read Trivy's exact JSON evidence and append a factual CI summary."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from src.application.security.trivy_report import summarize_trivy_report


def main() -> int:
    parser = argparse.ArgumentParser(description="Summarize a blocking Trivy scan")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("trivy-image-findings.json"),
    )
    args = parser.parse_args()
    try:
        with args.input.open(encoding="utf-8") as file:
            summary = summarize_trivy_report(json.load(file)).to_markdown()
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        parser.exit(1, f"Invalid Trivy evidence: {exc.__class__.__name__}\n")

    print(summary)
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        try:
            with Path(summary_file).open("a", encoding="utf-8") as file:
                file.write(summary + "\n")
        except OSError:
            parser.exit(1, "Could not write GitHub Actions security summary\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
