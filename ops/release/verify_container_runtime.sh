#!/usr/bin/env bash
# Release candidate smoke-test; no service or model provider egress allowed.
set -Eeuo pipefail

if [[ "$#" -ne 1 || -z "$1" ]]; then
  echo "Usage: verify_container_runtime.sh <local-image:tag>" >&2
  exit 2
fi
image="$1"
identity="$(docker image inspect --format '{{.Config.User}}' "$image")"
if [[ "$identity" != "10001:10001" ]]; then
  echo "Security gate: runtime image must specify 10001:10001." >&2
  exit 1
fi

cid=""
cleanup() {
  if [[ -n "$cid" ]]; then
    docker logs "$cid" >&2 || true
    docker rm -f "$cid" >/dev/null || true
  fi
}
trap cleanup EXIT

# Restrict network (including external downloads), privilege escalation,
# writable filesystem, kernel capabilities, memory and process count.
cid="$(docker run --detach \
  --network none \
  --read-only \
  --cap-drop ALL \
  --security-opt no-new-privileges \
  --pids-limit 256 \
  --memory 4g \
  --tmpfs /tmp:rw,nosuid,nodev,size=64m \
  --tmpfs /app/data:rw,nosuid,nodev,size=64m,uid=10001,gid=10001,mode=0700 \
  "$image")"

for attempt in $(seq 1 60); do
  if docker exec "$cid" /app/.venv/bin/python -c '
import importlib.util
import json
import os
import sqlite3
import stat
import urllib.request
from pathlib import Path

assert os.getuid() == 10001
assert os.getgid() == 10001
assert not os.access("/app", os.W_OK)
assert stat.S_IMODE(Path("/app/data").stat().st_mode) == 0o700
assert Path("/app/data").stat().st_uid == 10001
assert sqlite3.connect(":memory:").execute("SELECT 1").fetchone() == (1,)
assert importlib.util.find_spec("chromadb") is None
with urllib.request.urlopen(
    "http://127.0.0.1:8000/api/v1/health/", timeout=3
) as response:
    assert response.status == 200
    assert json.loads(response.read())["status"] == "ok"
print("ISOLATED_NONROOT_READONLY_HEALTH_PASS")
' 2>/dev/null; then
    echo "No-network read-only-root nonroot HTTP+SQLite smoke passed."
    exit 0
  fi
  if [[ "$(docker inspect --format '{{.State.Running}}' "$cid")" != "true" ]]; then
    echo "Container terminated before the isolated health check passed." >&2
    exit 1
  fi
  sleep 2
done

echo "Isolated read-only-root health check failed after bounded retries." >&2
exit 1
