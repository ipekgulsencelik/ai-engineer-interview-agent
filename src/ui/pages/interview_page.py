from __future__ import annotations

from typing import Any

import streamlit as st

from src.ui.exceptions.api_client_error import APIClientError
from src.ui.services.api_client import APIClient

LEVELS = ("JR", "MID", "SENIOR")
STATE_KEY = "interview"


def _state() -> dict[str, Any]:
    return st.session_state.setdefault(STATE_KEY, {})


def _reset() -> None:
    st.session_state[STATE_KEY] = {}


class InterviewPage:
    """
    Adaptive interview page backed by the /interview/sessions API.

    State lives in st.session_state["interview"]:
        session_id, question, progress, last (last answer result), summary
    """

    @staticmethod
    def render() -> None:
        st.title("AI Engineer Interview")
        state = _state()

        if not state.get("session_id"):
            InterviewPage._render_setup()
            return

        InterviewPage._render_progress(state["progress"])
        if state.get("last"):
            InterviewPage._render_last_result(state["last"])

        if state["progress"]["finished"]:
            InterviewPage._render_summary(state)
        else:
            InterviewPage._render_question(state)

        st.divider()
        if st.button("Start a new interview"):
            _reset()
            st.rerun()

    # ------------------------------------------------------------------

    @staticmethod
    def _render_setup() -> None:
        st.write(
            "An adaptive interview: the level moves up after three strong "
            "answers in a row and down after three weak ones."
        )
        with st.form("interview_setup"):
            level = st.selectbox("Starting level", LEVELS, index=0)
            skills = st.text_input("Your skills (comma-separated)", placeholder="python, langchain, rag")
            count = st.slider("Number of questions", min_value=3, max_value=20, value=8)
            submitted = st.form_submit_button("Start interview")

        if not submitted:
            return
        try:
            started = APIClient.start_interview(
                starting_level=level,
                cv_skills=[s.strip() for s in skills.split(",") if s.strip()],
                max_questions=count,
            )
        except APIClientError:
            st.error("Could not reach the interview API. Is it running on port 8000?")
            return

        _state().update(
            session_id=started["session_id"],
            question=started["question"],
            progress=started["progress"],
            last=None,
        )
        st.rerun()

    @staticmethod
    def _render_progress(progress: dict[str, Any]) -> None:
        answered, total = progress["answered"], progress["max_questions"]
        st.progress(answered / total, text=f"{answered}/{total} answered · level {progress['current_level']}")

    @staticmethod
    def _render_question(state: dict[str, Any]) -> None:
        question = state["question"]
        st.caption(f"{question['level']} · {question['category']} · {question['question_type']}")
        st.subheader(question["text"])

        with st.form(f"answer_{question['id']}", clear_on_submit=True):
            answer = st.text_area("Your answer", height=220)
            submitted = st.form_submit_button("Submit answer")

        if not submitted:
            return
        if not answer.strip():
            st.warning("Write an answer first.")
            return
        try:
            with st.spinner("Evaluating..."):
                result = APIClient.submit_interview_answer(
                    session_id=state["session_id"],
                    answer=answer,
                )
        except APIClientError:
            st.error("Evaluation failed. Please try again.")
            return

        state.update(
            last={"question": question, **result},
            progress=result["progress"],
            question=result["next_question"],
        )
        if result["progress"]["finished"]:
            state["summary"] = APIClient.get_interview(session_id=state["session_id"])
        st.rerun()

    @staticmethod
    def _render_last_result(last: dict[str, Any]) -> None:
        evaluation = last["evaluation"]
        with st.container(border=True):
            st.markdown(f"**Previous question:** {last['question']['text']}")
            cols = st.columns(4)
            cols[0].metric("Score", f"{evaluation['score']:.1f}/10")
            cols[1].metric("Technical", f"{evaluation['technical_accuracy']:.1f}")
            cols[2].metric("Depth", f"{evaluation['depth']:.1f}")
            cols[3].metric("Communication", f"{evaluation['communication']:.1f}")
            st.write(evaluation["feedback"])
            if evaluation.get("follow_up_question"):
                st.caption(f"Follow-up to think about: {evaluation['follow_up_question']}")
            if last["level_before"] != last["level_after"]:
                direction = "up" if LEVELS.index(last["level_after"]) > LEVELS.index(last["level_before"]) else "down"
                st.info(f"Level {direction}: {last['level_before']} → {last['level_after']}")

    @staticmethod
    def _render_summary(state: dict[str, Any]) -> None:
        summary = state.get("summary") or APIClient.get_interview(session_id=state["session_id"])
        st.header("Interview summary")
        cols = st.columns(2)
        cols[0].metric("Final level", summary["progress"]["current_level"])
        average = summary["average_score"]
        cols[1].metric("Average score", f"{average:.1f}/10" if average is not None else "-")

        categories = summary["categories"]
        if categories:
            st.subheader("By category")
            st.bar_chart(
                {
                    "category": [c["category"] for c in categories],
                    "average score": [c["average_score"] for c in categories],
                },
                x="category",
                y="average score",
                horizontal=True,
            )
            weakest = categories[0]
            st.write(f"Weakest area: **{weakest['category']}** ({weakest['average_score']:.1f}/10).")

        with st.expander("All answers"):
            for i, turn in enumerate(summary["turns"], start=1):
                st.markdown(f"**{i}. {turn['question']['text']}**  \nScore {turn['evaluation']['score']:.1f}/10")
                st.write(turn["answer"])
