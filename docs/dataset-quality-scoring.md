# Phase 2 — Dataset Quality Scoring v1

This increment adds **derived**, explainable dataset-quality scores to the
existing immutable, durable `QualityReport` history. It does not rewrite
`DatasetQualityEngine`, register new artifact content or add a public API.

## Data flow and architecture

1. The existing Quality Engine evaluates records; the registry-bound quality
   gate can verify artifact SHA-256 before evaluation.
2. `SQLiteDatasetQualityReportRepository` persists the authoritative
   `QualityReport` (existing behavior).
3. `DatasetQualityScoringService` reads reports through
   `QualityReportHistoryPort`, checks each referenced revision through
   `RegistryReader`, and calculates derived scores.
4. Scores are **not written back to the registry**. `score_run` evaluates
   a persisted run; `score_versions` returns the most recent report per
   SemVer, in numeric version order.

The scoring service depends only on read ports, domain models, and the
existing strict SemVer parser. No SQLite, FastAPI, or cloud provider imports
are required by the application service.

## Scoring formula (`dataset-quality-v1`)

The score ranges from 0 to 100 points. Components are rounded to two decimals:

| Component | Maximum points | Formula |
| --- | ---: | --- |
| Passing rule checks | 70 | `70 * report.pass_rate` |
| Records without reported failures | 20 | `20 * (1 - failed_record_count / record_count)` |
| Error issue density | 10 | `10 * (1 - min(1, error_count / total_checks))` |

An empty dataset or a run with no checks scores **zero**.
Warning-only failed checks already affect `pass_rate`. Multiple error issues
may originate from one check, so the error-density ratio is capped at 1.

These metrics measure **the configured rule outcomes**, **not factual
accuracy**, semantic diversity, fairness, human review quality or legal
compliance. Scores from different rule sets are not necessarily comparable;
the v1 formula is fixed and identified by an explicit model version.

## Admission and regression policy

`QualityScoringPolicy` defaults:

- `min_score=90.0` (points out of 100)
- `max_regression_points=5.0` (absolute point drop, not percent)
- `require_baseline=False` (initial version can be evaluated)
- `history_limit=1000` (bounded local history read)

A run passes only when the existing rule engine's `report.accepted` flag
is true, its score meets `min_score`, and the most recent report of the
immediately preceding **registered** numeric SemVer has a quality report,
that baseline report is accepted, and the score drop is within the allowed
regression. If `require_baseline` is enabled, a first version is
rejected with `baseline_missing`.

The baseline is the **latest checked run** for the immediately previous
registered dataset version (ties broken by run ID), not an arbitrarily
high-scoring historical run. If that registered version has no persisted
quality report, the decision fails with `baseline_report_missing`. The score does not modify the original
`QualityReport.accepted`. The `reason_codes` provide deterministic,
non-sensitive gate explanations.

## Fail-closed boundaries

- Reports referring to unregistered revisions are rejected (not silently
  omitted). Registry presence alone does **not** prove that a report was
  evaluated from matching bytes: that provenance comes from using the
  separate registry-bound artifact quality gate.
- Wrong dataset IDs, repeated run IDs and non-report history are rejected.
- A full bounded history **or registry version** page is treated as
  **potentially truncated** and rejected rather than permitting an invalid prior-version comparison.
- A rejected baseline blocks the next version even if the numeric score is
  high. An empty history produces an empty version history.
- Scoring returns identifiers, dates, numeric scores and fixed reason codes;
  it never returns raw records or issue messages. Existing quality reports
  still contain issue messages and must be protected according to their own
  data-classification policies.
- Quality report and catalog SQLite files are separate stores. There is no
  global transaction, snapshot isolation between reads, authorization API,
  immutable externally signed audit log or production rollout claim.
- This is **derived history**, not immutable policy-versioned score
  attestations; retention, cursor pagination, change-controlled policies,
  signed results and multi-tenant authorization are separate increments.

## Verification

```bash
uv run ruff check .
uv run pyright
uv run pytest -q tests/evaluation/dataset/quality/test_scoring.py
uv run pytest -q
```

Do not merge until the exact PR head passes required CI and review.
This PR does not change production image publishing or the separate
release-security blockers tracked under Issue #47.
