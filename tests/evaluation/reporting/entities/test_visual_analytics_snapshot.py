from __future__ import annotations


def test_visual_analytics_snapshot_exposes_chart_properties(visual_snapshot) -> None:
    assert visual_snapshot.point_count == 2
    assert visual_snapshot.has_labels is True
    assert visual_snapshot.has_scores is True
    assert visual_snapshot.has_average_score is True
    assert visual_snapshot.has_trend_direction is True
    assert visual_snapshot.max_score == 0.9
    assert visual_snapshot.min_score == 0.7
    assert visual_snapshot.latest_score == 0.9
    assert visual_snapshot.is_improving is True
    assert visual_snapshot.has_metadata is True
    assert visual_snapshot.has_description is True
