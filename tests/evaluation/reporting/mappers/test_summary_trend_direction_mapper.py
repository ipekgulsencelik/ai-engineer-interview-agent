from __future__ import annotations

from src.evaluation.reporting.enums.summary_trend_direction import SummaryTrendDirection
from src.evaluation.reporting.mappers.summary_trend_direction_mapper import SummaryTrendDirectionMapper


def test_from_string_normalizes_known_and_unknown_directions() -> None:
    mapper = SummaryTrendDirectionMapper()

    assert mapper.from_string(direction="improving") == SummaryTrendDirection.IMPROVING
    assert mapper.from_string(direction="regressing") == SummaryTrendDirection.DECLINING
    assert mapper.from_string(direction="declining") == SummaryTrendDirection.DECLINING
    assert mapper.from_string(direction="volatile") == SummaryTrendDirection.VOLATILE
    assert mapper.from_string(direction="stable") == SummaryTrendDirection.STABLE
    assert mapper.from_string(direction="unexpected") == SummaryTrendDirection.UNKNOWN
