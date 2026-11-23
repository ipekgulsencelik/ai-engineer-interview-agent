"""The terminal interview runs end to end with scripted answers."""

from __future__ import annotations

from src.scripts.run_interview import main


def test_demo_interview_runs_and_changes_level(capsys) -> None:
    assert main(["--demo", "--level", "MID", "--questions", "6"]) == 0

    out = capsys.readouterr().out
    assert out.count("Q: ") == 6
    assert ">>> level MID -> SENIOR" in out
    assert ">>> level SENIOR -> MID" in out
    assert "Final level: MID" in out
