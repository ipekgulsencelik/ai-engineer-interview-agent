#!/usr/bin/env bash
# Reproducible source bundle for a verified Git commit; no manual copy step.
set -euo pipefail

: "${RELEASE_TAG:?RELEASE_TAG must be set}"
: "${GITHUB_SHA:?GITHUB_SHA must be set}"

python -m src.infrastructure.operations.release_cli verify-source \
  --tag "$RELEASE_TAG" --sha "$GITHUB_SHA"

mkdir -p dist
archive="dist/ai-engineer-interview-agent-${RELEASE_TAG}.tar.gz"
git archive --format=tar HEAD | gzip -n -9 > "$archive"

python -m src.infrastructure.operations.release_cli create-manifest \
  --tag "$RELEASE_TAG" --sha "$GITHUB_SHA" \
  --archive "$archive" --output dist/release-manifest.json

python -m src.infrastructure.operations.release_cli verify-manifest \
  --tag "$RELEASE_TAG" --sha "$GITHUB_SHA" \
  --archive "$archive" --manifest dist/release-manifest.json

# Rebuild from the same Git tree and require byte-identical output.
git archive --format=tar HEAD | gzip -n -9 > dist/repro-check.tar.gz
cmp "$archive" dist/repro-check.tar.gz
rm dist/repro-check.tar.gz
sha256sum "$archive" > dist/release-sha256sums.txt
echo "Release source bundle and SHA256 manifest verified"
