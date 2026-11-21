# PostgreSQL Production Readiness and Security — opt-in hardening

This increment builds on CloudNativePG HA/PITR PR #34, but **does not**
deploy to production, measure a real operational SLA, or grant production
credentials. Kubernetes/network and External Secrets resources must be
reviewed by the infrastructure team and applied separately.

## Scope and SOLID boundaries

- `ops/postgres-ha/security/network-policy.yaml`: opt-in, **ingress-only**
  Kubernetes NetworkPolicy for the *primary* CNPG cluster's pods.
  Replication (5432) is restricted to matching peers; operator status
  (8000) is limited to `cnpg-system`; application SQL (5432) requires an
  explicitly approved namespace label and workload label; metrics (9187)
  are limited to the monitoring namespace. Review and change selectors
  to match the actual platform before enabling. The namespace labels
  and network plugin must be admin-controlled. This does NOT restrict
  outgoing S3 calls, DNS or Kubernetes API access. Do not apply egress
  default-deny without a live operator failover, DNS and backup drill.
- `security/read-only-rbac.yaml`: namespace-scoped auditor ServiceAccount
  and Role. Only get/list/watch of cluster, backups, scheduled backups,
  object stores and pods. No writes, secrets, exec or deletion rights.
  `automountServiceAccountToken: false` is the ServiceAccount's default;
  an authorized service must explicitly obtain and attach a token if used.
- `security/*-external-secret.yaml`: **optional** External Secrets
  Operator v1 templates for the writer and *separate restore reader*.
  They are intentionally **not deployable as-is**: the ClusterSecretStore
  and remote credential paths all start with `REPLACE_WITH_`. Use an
  approved vault and access control boundary to fill them. No secret
  values are stored in the repo. Backup-writer permissions must be
  scoped to the exact archive; restore identity must be read-only.
  Before a production release, review provider-specific encryption,
  rotation, secret deletion semantics, RBAC and vault audit trails.
- `src/application/operations/dr_readiness.py`: pure deterministic
  fail-closed readiness evaluator with immutable policy/report objects.
  Does not depend on kubectl, CloudNativePG, Prometheus or the SDK.
- `src/infrastructure/operations/dr_readiness_cli.py`: separate
  evidence file adapter; never mutates a cluster and suppresses sensitive
  source content in validation errors. Automation may use exit status
  to prevent promotion.
- `monitoring/postgres-recovery-alerts.yml`: Barman Cloud Plugin
  and CNPG backup freshness, failed backup and replica connection alerts.

## NetworkPolicy application prerequisites

The operator namespace is assumed `cnpg-system` and the metrics
namespace `monitoring`. The application must have both:
- namespace label `db-access.ai-interview/approved=true`, controlled by a
  cluster administrator; and
- pod label `app.kubernetes.io/name=ai-engineer-interview-agent`.

These selectors are **deployment-dependent**. Confirm real CNPG
`cnpg.io/cluster` labels and traffic through ports 5432/8000/9187.
Kubernetes NetworkPolicies require an enforcing CNI, and ingress and
egress decisions can be affected by other policies. Test CNPG operator
reconciliation, failover, replication, Prometheus scraping and app DB
writes before accepting the policy. A deployment should supply explicit
database TLS/auth controls; NetworkPolicy alone does not authenticate
callers or encrypt packets.

Do not automatically apply to recovery namespaces; review a distinct
recovery security policy with read-only object-store egress and explicit
operator access before rollout.

## Secret management

Install and verify the trusted External Secrets Operator CRDs and
ClusterSecretStore before applying templates. Keep remote paths
and all credentials outside version control. An external secret
controller must not have cluster-wide privileges beyond its authorized
scope. Check event/log scrubbing, refresh and rotation behavior and
secret recovery in a staging drill.

The source writer and restore reader are separate principals:
- `interview-db-s3-writer` in `interview-db`;
- `interview-db-s3-restore-reader` in `interview-db-restore`.

The restore principal must not overwrite, delete or append to source
backup archives. Validate S3 bucket versioning, encryption and
object-lock configuration in the actual cloud; YAML templates do not
prove those cloud-side controls exist.

## Monitoring and alert rules

The alert file targets an **external Kubernetes Prometheus instance**
scraping CNPG's port 9187. The repository's local Compose Prometheus
**does not** automatically discover CNPG metrics. Before installing the
rules, inspect live series labels (namespace, cluster), actual Barman
plugin metrics, and cardinality:

- `barman_cloud_cloudnative_pg_io_last_available_backup_timestamp`
  (last successful base backup);
- `barman_cloud_cloudnative_pg_io_last_failed_backup_timestamp`
  (last unsuccessful backup);
- `cnpg_pg_replication_streaming_replicas`
  (replica connectivity; not proof of zero data loss).

Rules alert for missing plugin/replication telemetry, backup older than
26 hours, backup failure more recent than success, and fewer than
two streaming standbys. Values are **example operational thresholds**
for a daily backup and 3-instance cluster, not approved SLOs. Missing
series checks can fire when traffic/metrics ingestion is not configured.

**No fabricated WAL freshness metric:** the plugin's documented
last-available-backup timestamp is not a WAL archival freshness signal.
WAL archive continuity must be independently observed through object
storage, log analysis and restore drills. A last WAL timestamp may be
reported as evidence only when actually measured at the archive.

## DR evidence and RPO/RTO

`ReadinessEvaluator` needs a trusted, time-stamped input, for example:

```json
{
  "observed_at": "2026-11-22T12:00:00Z",
  "instances_desired": 3,
  "instances_ready": 3,
  "primary_known": true,
  "last_successful_backup_at": "2026-11-22T02:00:00Z",
  "last_archived_wal_at": "2026-11-22T11:55:00Z",
  "restore_drill": {
    "independently_verified": true,
    "incident_declared_at": "2026-11-22T11:20:00Z",
    "service_writable_at": "2026-11-22T11:25:00Z",
    "latest_committed_at": "2026-11-22T11:19:00Z",
    "latest_recovered_commit_at": "2026-11-22T11:18:00Z"
  }
}
```

These are **synthetic example timestamps, not live evidence**.
Never copy sample dates into a production readiness report.
Collect timestamps from an actual independently verified drill. The
evaluator computes:
- **Observed drill RTO** = first recovered writable service time minus
  incident declaration time;
- **Observed drill RPO** = latest committed transaction timestamp
  before loss minus latest transaction recovered;
- **Backup age** and **WAL evidence age** = observation timestamp minus
  independently supplied source timestamps.

Run with independently collected JSON:

```bash
python -m src.infrastructure.operations.dr_readiness_cli \
  --evidence /path/to/verified-dr-evidence.json \
  --max-rpo-seconds 300 --max-rto-seconds 900
```

Exit 0 = all checks pass, 1 = valid evidence with failed checks,
2 = invalid or inconsistent evidence. The report excludes arbitrary
input metadata, DSNs and secret-bearing error strings.

A passed report **does not prove SLO compliance**: accuracy depends on
the independently verified source evidence and correct clocks, network
topology and representative workload. The local disposable Docker PITR
CI test provides a useful mechanism test, but is **not** production
RPO/RTO evidence or a Barman S3 recovery validation.

## CI and deployment gates

The `postgres-production-readiness` GitHub Actions job validates
network isolation boundaries, read-only RBAC, ExternalSecret references
and monitoring alerts; it runs the real `promtool check rules` parser.
The default full Pytest job exercises the pure DR evaluator/CLI.
Existing PostgreSQL 16 integration, real PITR Docker drill and
observability jobs remain required.

Before actual deployment: validate CRDs and versions in staging, enforce
code owner review and branch protection, pin image digests, review
Kyverno/Gatekeeper policy where available, verify S3 recovery using
read-only credentials, test automatic failover under the policy, document
measured RTO/RPO, verify backups with retention/immutability, alert to
on-call, and test the fail-closed security policy under real tenant roles.

This PR intentionally does NOT change production credentials, install
operators, create cloud resources or run destructive cluster operations.
