from __future__ import annotations

from src.evaluation.reporting.interpreters.executive_summary_assessment_interpreter import ExecutiveSummaryAssessmentInterpreter


def test_interpret_maps_score_thresholds_to_assessment_labels() -> None:
    interpreter = ExecutiveSummaryAssessmentInterpreter()

    assert interpreter.interpret(overall_score=0.95) == "excellent"
    assert interpreter.interpret(overall_score=0.85) == "strong"
    assert interpreter.interpret(overall_score=0.75) == "acceptable"
    assert interpreter.interpret(overall_score=0.65) == "needs_improvement"
    assert interpreter.interpret(overall_score=0.5) == "high_risk"
