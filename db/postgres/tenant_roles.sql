-- Idempotent DBA-only bootstrap after "alembic upgrade head".
-- DO NOT grant LOGIN, SUPERUSER, BYPASSRLS, CREATEROLE or table ownership
-- to these group roles. Grant exactly one role to each tenant's DB login.
-- Requires a dedicated, trusted tenant login identity per isolated tenant.
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_catalog.pg_roles
        WHERE rolname = 'interview_monitor_reader'
    ) THEN
        CREATE ROLE interview_monitor_reader NOLOGIN;
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_catalog.pg_roles
        WHERE rolname = 'interview_monitor_writer'
    ) THEN
        CREATE ROLE interview_monitor_writer NOLOGIN;
    END IF;
    IF NOT EXISTS (
        SELECT 1 FROM pg_catalog.pg_roles
        WHERE rolname = 'interview_monitor_dispatcher'
    ) THEN
        CREATE ROLE interview_monitor_dispatcher NOLOGIN;
    END IF;
END
$$;

GRANT interview_monitor_reader TO
    interview_monitor_writer, interview_monitor_dispatcher;

GRANT USAGE ON SCHEMA public TO interview_monitor_reader;
GRANT USAGE ON SCHEMA monitoring_security TO interview_monitor_reader;
GRANT EXECUTE ON FUNCTION monitoring_security.current_tenant()
    TO interview_monitor_reader;

GRANT SELECT ON
    dataset_monitor_snapshots,
    dataset_monitor_alert_outbox,
    dataset_monitor_alert_receipts,
    dataset_monitor_alert_delivery_events
TO interview_monitor_reader;

GRANT INSERT ON
    dataset_monitor_snapshots,
    dataset_monitor_alert_outbox
TO interview_monitor_writer;

-- The dispatcher needs to change lease/retry state and append audit events.
-- The higher-level operator authorization for requeue is a separate API concern.
GRANT UPDATE ON dataset_monitor_alert_outbox
    TO interview_monitor_dispatcher;
GRANT INSERT ON
    dataset_monitor_alert_receipts,
    dataset_monitor_alert_delivery_events
TO interview_monitor_dispatcher;

-- Event sequence is GENERATED ALWAYS AS IDENTITY; insert uses no sequence
-- reference, so explicit sequence usage must not be broadly granted.

-- Provision each login OUTSIDE this file with a unique managed credential:
-- CREATE ROLE tenant_acme_writer LOGIN PASSWORD '<from secret manager>';
-- GRANT interview_monitor_writer TO tenant_acme_writer;
-- INSERT INTO monitoring_security.tenant_login_bindings(login_role,tenant_id)
-- VALUES ('tenant_acme_writer', 'acme');
-- Each tenant also needs distinct reader/dispatcher credentials as applicable.
-- NEVER grant tenant logins access to this binding table or migration role.
