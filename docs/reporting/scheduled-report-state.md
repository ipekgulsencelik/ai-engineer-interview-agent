# Scheduled reporting: execution state and re-scheduling

Scheduled report state is immutable. After a run, the state service records
the execution timestamp and clears the stored next-run timestamp if that
deadline has already elapsed. This prevents both invalid timestamps
(`next_run_at` earlier than `last_run_at`) and accidental repeated
execution of the same overdue schedule.

This state service **does not parse cron or compute the next occurrence**.
A separate scheduling policy or persistence adapter must provide and persist
the next upcoming `next_run_at` to enable recurrence. A cleared timestamp
represents a schedule that is not currently due, not a successful future
rescheduling. Existing early or manual executions retain a future deadline.

`ScheduledReport.is_due` compares aware deadlines to an aware UTC clock;
for legacy naive timestamps it uses the UTC-naive interpretation. New
integrations should prefer aware UTC datetimes. Mixed aware/naive inputs to
state transitions are rejected rather than silently shifted.
