from __future__ import annotations

from datetime import timezone
from uuid import UUID

from src.evaluation.ops.providers.run_id_provider import RunIdProvider
from src.evaluation.ops.providers.utc_datetime_provider import UTCDateTimeProvider


def test_run_id_provider_should_generate_uuid_string() -> None:
    run_id = RunIdProvider.generate()

    assert str(UUID(run_id)) == run_id


def test_utc_datetime_provider_should_return_timezone_aware_utc_datetime() -> None:
    current_time = UTCDateTimeProvider.now()

    assert current_time.tzinfo == timezone.utc
