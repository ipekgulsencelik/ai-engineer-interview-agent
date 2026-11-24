"""Streamlit interview page flow with the API client stubbed."""

from __future__ import annotations

import pytest

pytest.importorskip("streamlit")

from streamlit.testing.v1 import AppTest  # noqa: E402


def _app() -> None:
    from src.ui.pages import interview_page
    from src.ui.services.api_client import APIClient

    question = {
        "id": "q1",
        "text": "What is RAG?",
        "category": "rag",
        "level": "JR",
        "question_type": "conceptual",
        "difficulty": 1,
    }
    evaluation = {
        "score": 8.0,
        "technical_accuracy": 8.0,
        "depth": 8.0,
        "communication": 8.0,
        "feedback": "Good answer.",
        "missing_keywords": [],
        "follow_up_question": "Why?",
        "rubric_version": "test",
    }
    progress = {"current_level": "JR", "answered": 0, "max_questions": 1, "finished": False}
    done = {**progress, "answered": 1, "finished": True}

    APIClient.start_interview = classmethod(  # type: ignore[method-assign]
        lambda cls, **_: {"session_id": "s1", "progress": progress, "question": question}
    )
    APIClient.submit_interview_answer = classmethod(  # type: ignore[method-assign]
        lambda cls, **_: {
            "evaluation": evaluation,
            "level_before": "JR",
            "level_after": "JR",
            "progress": done,
            "next_question": None,
        }
    )
    APIClient.get_interview = classmethod(  # type: ignore[method-assign]
        lambda cls, **_: {
            "session_id": "s1",
            "progress": done,
            "average_score": 8.0,
            "categories": [{"category": "rag", "average_score": 8.0, "answered": 1}],
            "turns": [{"question": question, "answer": "a", "evaluation": evaluation, "level_after": "JR"}],
        }
    )
    interview_page.InterviewPage.render()


def test_setup_start_answer_and_summary() -> None:
    at = AppTest.from_function(_app).run()
    assert not at.exception
    assert at.button[0].label == "Start interview"

    at.button[0].click().run()
    assert any("What is RAG?" in s.value for s in at.subheader)

    at.text_area[0].input("RAG retrieves context and grounds generation.")
    at.button[0].click().run()

    assert not at.exception
    assert any("Interview summary" in h.value for h in at.header)
    assert any(m.value == "8.0/10" for m in at.metric)
