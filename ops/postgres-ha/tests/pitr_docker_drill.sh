#!/usr/bin/env bash
# True PostgreSQL physical backup + archived WAL + named-point PITR test.
# Runs only against disposable Docker containers. Never accepts a DB DSN.
set -euo pipefail

for executable in docker mktemp; do
  command -v "$executable" >/dev/null || {
    echo "Missing required executable: $executable" >&2; exit 1;
  }
done

work="$(mktemp -d)"
suffix="dr-pitr-${GITHUB_RUN_ID:-local}-$$"
source_name="${suffix}-src"
restore_name="${suffix}-restored"
ci_password="ci-only-temporary-postgresql-password"

cleanup() {
  docker rm -f "$source_name" "$restore_name" >/dev/null 2>&1 || true
  rm -rf "$work"
}
trap cleanup EXIT

mkdir -p "$work"/{source,base,archive,restored}
chmod 0777 "$work"/{source,base,archive,restored}

echo "[DR] start isolated PostgreSQL 16 source with WAL archiving"
docker run -d --rm --name "$source_name" \
  -e POSTGRES_PASSWORD="$ci_password" \
  -e POSTGRES_DB="dr_fixture" \
  -v "$work/source:/var/lib/postgresql/data" \
  -v "$work/base:/backup" \
  -v "$work/archive:/archive" \
  -v "$work/restored:/restore" \
  postgres:16.16 \
  -c wal_level=replica \
  -c archive_mode=on \
  -c 'archive_command=test ! -f /archive/%f && cp %p /archive/%f' \
  -c archive_timeout=1s \
  -c max_wal_senders=5 >/dev/null

source_psql() {
  docker exec -e "PGPASSWORD=$ci_password" "$source_name" \
    psql -X -v ON_ERROR_STOP=1 -h 127.0.0.1 -U postgres \
    -d dr_fixture -Atc "$1"
}

for i in $(seq 1 60); do
  if docker exec "$source_name" pg_isready -h 127.0.0.1 -U postgres \
      -d dr_fixture >/dev/null 2>&1; then break; fi
  sleep 1
done
source_psql "CREATE TABLE dr_recovery_marker (id INTEGER PRIMARY KEY)"
source_psql "INSERT INTO dr_recovery_marker VALUES (1)"

echo "[DR] create and verify physical base backup"
docker exec -e "PGPASSWORD=$ci_password" "$source_name" \
  pg_basebackup -h 127.0.0.1 -U postgres -D /backup/base \
  -Fp -Xs -c fast --progress >/dev/null
docker exec "$source_name" pg_verifybackup /backup/base

echo "[DR] write after-base-backup evidence, then destructive change"
source_psql "INSERT INTO dr_recovery_marker VALUES (2)"
source_psql "SELECT pg_create_restore_point('dr_before_undesired_insert')"
source_psql "INSERT INTO dr_recovery_marker VALUES (3)"
segment="$(source_psql 'SELECT pg_walfile_name(pg_current_wal_lsn())')"
source_psql "SELECT pg_switch_wal()"

echo "[DR] verify archived WAL segment containing the marker"
archived=""
for i in $(seq 1 60); do
  if docker exec "$source_name" test -s "/archive/$segment"; then
    archived="yes"
    break
  fi
  sleep 1
done
if [[ "$archived" != yes ]]; then
  echo "WAL archiving failed to deliver the required segment" >&2
  exit 1
fi

# Copy a fixed physical backup, never the source's mutable PGDATA.
docker exec -u root "$source_name" sh -c \
  'cp -a /backup/base/. /restore/ && chown -R postgres:postgres /restore'
docker exec -u root "$source_name" sh -c \
  "printf '%s\n' \
    \"restore_command = 'cp /archive/%f %p'\" \
    \"recovery_target_name = 'dr_before_undesired_insert'\" \
    \"recovery_target_action = 'promote'\" \
    >> /restore/postgresql.auto.conf && touch /restore/recovery.signal"

echo "[DR] start restored database and replay WAL only to named target"
docker run -d --rm --name "$restore_name" \
  -e POSTGRES_PASSWORD="$ci_password" \
  -v "$work/restored:/var/lib/postgresql/data" \
  -v "$work/archive:/archive:ro" \
  postgres:16.16 >/dev/null

restored_psql() {
  docker exec -e "PGPASSWORD=$ci_password" "$restore_name" \
    psql -X -v ON_ERROR_STOP=1 -h 127.0.0.1 -U postgres \
    -d dr_fixture -Atc "$1"
}

ready=""
for i in $(seq 1 90); do
  if docker exec "$restore_name" pg_isready -h 127.0.0.1 -U postgres \
    -d dr_fixture >/dev/null 2>&1; then
    ready=yes
    break
  fi
  sleep 1
done
if [[ "$ready" != yes ]]; then
  echo "Restored PostgreSQL did not become ready" >&2
  exit 1
fi

observed="$(restored_psql 'SELECT string_agg(id::text, chr(44) ORDER BY id) FROM dr_recovery_marker')"
if [[ "$observed" != "1,2" ]]; then
  echo "PITR DATA MISMATCH: expected marker rows 1,2; got: $observed" >&2
  exit 1
fi
role="$(restored_psql 'SELECT pg_is_in_recovery()')"
if [[ "$role" != f ]]; then
  echo "Recovered database was not promoted" >&2
  exit 1
fi
echo "[DR] PASS: restored WAL evidence (1,2), excluded post-target row 3"
