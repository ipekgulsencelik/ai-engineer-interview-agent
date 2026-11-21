# PostgreSQL High Availability and Disaster Recovery — reference design

**Status:** Reference Kubernetes HA/DR deployment and automated disposable
PostgreSQL recovery test. This change does NOT deploy an actual Kubernetes
cluster, migrate an existing PostgreSQL database, configure cloud secrets,
or demonstrate the production environment's RPO/RTO. No HA/SLA certification
is claimed without an environment-specific failover and restore drill.

## Topology and boundaries

- **CloudNativePG operator (1.30.x):** manages a 3-instance PostgreSQL
  16.16 cluster, one primary and two hot standbys, health monitoring,
  election and automatic primary failover.
- **Synchronous replication:** `minSyncReplicas: 1` and
  `maxSyncReplicas: 1`. Healthy acknowledged commits are written to a
  primary and one sync standby. With no healthy standby the system may
  **block writes rather than risk data loss**. This is an explicit
  durability/availability choice, not zero-RPO or continuous-write SLA.
- **Zone anti-affinity:** one PostgreSQL pod per distinct
  `topology.kubernetes.io/zone`; requires at least 3 schedulable zones
  and a CSI volume driver with compatible independent storage. A single
  Kubernetes control-plane failure domain is not equivalent to cross-region HA.
- **CloudNativePG Barman Cloud Plugin (0.16.x):** continuous WAL archive
  to versioned, encrypted, private object storage and daily plugin-backed
  physical base backups. Immediate initial backup is requested.
- **Retention:** example `30d` recovery window; retention and WAL
  availability depend on correct object-store permissions, backup success,
  ongoing WAL archiving and object retention settings.
- **PITR:** a separate, *single-instance* restoration cluster with different
  namespace/name, **read-only** credentials against the source backup
  archive, and an explicitly selected UTC recovery timestamp.
- **Existing RLS/RBAC:** database user/tenant privileges and role binding
  remain governed by Alembic revision `20261121_03`. Recovery replays
  physical PostgreSQL content, including relevant role catalogs and tenant
  mappings, subject to target time. Never connect application workloads
  using the operator/migration superuser.

CloudNativePG's operator manages automatic failover. The included
`ControlledFailoverVerifier` is only an explicitly approved **destructive
staging drill**, not a replacement leader election/HA implementation.

## Preconditions — do NOT blindly apply to production

1. Review current CloudNativePG **1.30.x** and official Barman Cloud
   Plugin **0.16.x** release and compatibility advisories; install and
   validate operator, plugin, and CRDs through your trusted deployment
   process, not an unpinned public remote-install pipe.
2. Create `interview-db` namespace, three independent ready zones,
   appropriately encrypted volume classes and tested PVC performance.
   Cluster manifests require an application-specific capacity review.
3. Provision a versioned, encrypted S3 bucket with off-site replication,
   lifecycle, restricted permissions, retention/object-lock policy and
   tested access. **Replace**
   `s3://REPLACE_WITH_REAL_VERSIONED_BACKUP_BUCKET/interview-db-primary/`
   with the actual archive prefix *before applying*. The placeholder is
   deliberately unusable. Never use the same prefix for a second writer.
4. Supply `interview-db-s3-writer` Kubernetes Secret through an external
   secrets controller, not Git. The source writer needs appropriately scoped
   PutObject/GetObject/ListBucket/DeleteObject permissions consistent with
   Barman cleanup; avoid public bucket policies. Separate IAM accounts for
   restore credentials, with only **GetObject/ListBucket**.
5. Keep database passwords and TLS CA material in an approved secret
   manager; enable network policies/ingress and audit. Do not expose
   PostgreSQL or backups on a public endpoint.
6. Decide who owns the PostgreSQL operator/cluster namespace permissions
   and who can trigger backup or restore. Restrict deletion of backups,
   PVCs, ObjectStores and `Cluster` custom resources.
7. Verify the **existing data migration** from your local Docker/SQLite
   setup to PostgreSQL separately. This manifest does not copy SQLite
   data, create tenants, or migrate SQL schema automatically. Alembic and
   the DBA tenant role bootstrap are separate deployment steps.
8. Review retention and actual operational RPO and RTO targets with
   application owners. `archive_timeout: 300s` is NOT a hard 5-minute
   RPO promise. A failure before successful WAL upload can lose data
   beyond the last archived segment, especially during cluster-wide loss.

## Deployment — Kubernetes only

After installing the operator, plugin, backup infrastructure, and secrets:

```bash
kubectl apply -f ops/postgres-ha/kubernetes/namespace.yaml
kubectl apply -f ops/postgres-ha/kubernetes/object-store.yaml
kubectl apply -f ops/postgres-ha/kubernetes/cluster.yaml
kubectl apply -f ops/postgres-ha/kubernetes/scheduled-backup.yaml

kubectl -n interview-db get clusters.postgresql.cnpg.io
kubectl -n interview-db get scheduledbackups.postgresql.cnpg.io
kubectl -n interview-db get backups.postgresql.cnpg.io
```

Validate a **completed** base backup and successful recent WAL archives
before accepting the system as protected. The existence of a ScheduledBackup
resource alone does not prove recoverability.

The CNPG primary write endpoint is
`interview-db-primary-rw.interview-db.svc.cluster.local:5432`, and
read-only replicas are exposed through
`interview-db-primary-ro.interview-db.svc.cluster.local:5432`.
Only workloads already deployed into the Kubernetes cluster with
authenticated PostgreSQL credentials can use these endpoints. Keep
database access controlled by your existing tenant-specific DB roles.
No application DSN is changed by this PR.

## Point-In-Time Recovery drill (isolated)

A restore requires a valid base backup completed **before** the desired
target, and all archived WAL segments between the backup and that point.
Determine an exact UTC timestamp **from backed-up data and WAL history**.

The recovery template
`ops/postgres-ha/recovery/pitr-cluster.yaml` uses
`REPLACE_WITH_VERIFIED_UTC_TIMESTAMP`; **it must be replaced with a
verified RFC3339 timestamp** (for example `2026-11-21T09:15:00Z`) before
applying. Do not use an invented timestamp or a timestamp before the base
backup. The target must be reachable in the archive; restoring to a
timestamp without a qualifying following transaction can fail.

```bash
kubectl apply -f ops/postgres-ha/recovery/recovery-namespace.yaml
# First provide interview-db-s3-restore-reader Secret in the restore namespace.
kubectl apply -f ops/postgres-ha/recovery/source-object-store.yaml
# Only after editing the recovery target and verifying all prerequisites:
kubectl apply -f ops/postgres-ha/recovery/pitr-cluster.yaml

kubectl -n interview-db-restore get clusters.postgresql.cnpg.io
```

Inspect the restored database **without running the source application's
normal traffic**. Compare known record counts/checksums, schema revision,
RLS/tenant bindings, and a marker inserted *after* the target (which
must **not** exist). Write a signed operator drill report including
backup identifier, recovery target, achieved RPO/RTO and any missing WAL.

Never re-enable write archival to the source backup prefix from the
restored cluster. Configure a **new, separate** backup prefix for a
promoted production recovery cluster after human approval; do not bypass
CNPG's empty-archive safety check.

## Automatic failover / destructive staging drill

The primary cluster has three pods and the operator automatically
coordinates promotion via Kubernetes leases. To simulate a primary pod
loss without touching production, create the dedicated staging cluster:

```bash
kubectl apply -f ops/postgres-ha/drills/isolated-failover-cluster.yaml
kubectl -n interview-db-drill get cluster interview-db-drill

python -m src.infrastructure.operations.postgres_failover_drill \
  --namespace interview-db-drill \
  --cluster interview-db-drill \
  --approval I_AUTHORIZE_DESTRUCTIVE_DRILL_IN_ISOLATED_CLUSTER
```

The drill **refuses all namespaces/clusters except the exact dedicated
test pair**, requires three healthy pods and explicit approval, deletes
only the *test* primary Pod, then confirms that the operator reports a
different primary and the new pod accepts a writable SQL connection
(`NOT pg_is_in_recovery()`).

Do not run this command in a shared production namespace. The user
executing the drill needs `kubectl` permissions for get/delete pods,
get clusters and pod exec *in the test namespace only*.

## Real WAL replay validation in CI

`ops/postgres-ha/tests/pitr_docker_drill.sh` boots **two disposable
PostgreSQL 16.16 containers**, configures local WAL archiving, creates and
verifies a physical base backup with `pg_verifybackup`, inserts an
after-backup marker, creates a named restore point, then writes a later
undesired row. It restores the **physical** backup and replays archived WAL
to the named target, asserting rows **1 and 2 exist while row 3 does not**
and the restored server is promoted. It never accepts a production DSN.

```bash
bash ops/postgres-ha/tests/pitr_docker_drill.sh
```

The CI test proves PostgreSQL base-backup/WAL recovery mechanics on a
disposable host. It does **not** prove a Barman S3 recovery, a live CNPG
Kubernetes promotion, automatic operator failover, or the chosen object's
real RPO/RTO.

## Operations and disaster scenarios

- **Pod crash:** CNPG handles primary election within its configured
  Kubernetes availability boundary. The application must reconnect through
  the `-rw` service; in-flight requests may fail, retry and deduplicate.
- **Zone loss:** success depends on scheduling, replica health, quorum,
  shared infrastructure and surviving storage. With synchronous standby
  unavailable, writes may block until a standby recovers.
- **Accidental DELETE:** isolate the original cluster; restore a **separate**
  cluster to a verified target before the destructive transaction. Compare
  rows and authorise controlled cutover.
- **Total region/cluster failure:** recover in another region from an
  independently replicated backup/WAL archive. This is a **manual DR
  operation**, not an automatically configured cross-region failover.
- **Archive lag, credential expiry, bucket deletion:** fail closed on
  missing backup/WAL; monitor backup success, last archived WAL time,
  replication lag, free space and restore drill performance. Enforce
  offsite immutability where supported and test retention policy.

### Acceptance criteria before calling this production-ready

At minimum: observe a successful **real object-store restore**, perform
a **real Kubernetes primary failover drill**, measure end-to-end RTO/RPO
during failures, prove cloud bucket immutability/encryption and IAM
controls, verify cross-AZ placement, configure alerts for replication
lag/failed backup/last WAL, test identity/tenant isolation post-restore,
and validate an actual regional disaster exercise. The CI job alone does
not satisfy these requirements.

## References

- PostgreSQL 16: continuous WAL archiving and PITR,
  https://www.postgresql.org/docs/16/continuous-archiving.html
- CloudNativePG 1.30, backup/recovery,
  https://cloudnative-pg.io/docs/1.30/backup/
  https://cloudnative-pg.io/docs/1.30/recovery/
- Barman Cloud Plugin: object store, WAL and plugin restore,
  https://cloudnative-pg.io/plugin-barman-cloud/docs/usage/
