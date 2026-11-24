"""End-to-end interview over HTTP, offline (no LLM key, no embedding model)."""

from __future__ import annotations

import json

import pytest

pytest.importorskip("fastapi")

from fastapi.testclient import TestClient  # noqa: E402

from src.api.app import create_app  # noqa: E402
from src.application.models.llm_response import LLMResponse  # noqa: E402
from src.application.ports.llm_client import LLMClient  # noqa: E402
from src.infrastructure.containers.service_container import (  # noqa: E402
    ServiceContainer,
)

BASE = "/api/v1/interview/sessions"
GOOD_ANSWER = (
    "It splits text into subword tokens. The context window limits input plus "
    "output tokens, so cost and latency scale with tokens and long inputs must "
    "be truncated or chunked. A tokenizer defines the vocabulary."
)


class StaticLLM(LLMClient):
    def generate(self, *, request):
        return LLMResponse(
            text=json.dumps(
                {"technical_accuracy": 9, "depth": 9, "communication": 9, "feedback": "Great."}
            )
        )


def client_for(**container_kwargs) -> TestClient:
    container_kwargs.setdefault("use_semantic_retrieval", False)
    app = create_app(container_factory=lambda: ServiceContainer(**container_kwargs))
    return TestClient(app)


def test_full_interview_flow_offline() -> None:
    with client_for() as client:
        started = client.post(BASE, json={"starting_level": "JR", "max_questions": 3})
        assert started.status_code == 201, started.text
        body = started.json()
        session_id = body["session_id"]
        assert body["question"]["level"] == "JR"
        assert body["progress"] == {
            "current_level": "JR",
            "answered": 0,
            "max_questions": 3,
            "finished": False,
        }

        seen = {body["question"]["id"]}
        for i in range(3):
            answered = client.post(f"{BASE}/{session_id}/answers", json={"answer": GOOD_ANSWER})
            assert answered.status_code == 200, answered.text
            result = answered.json()
            assert 0 <= result["evaluation"]["score"] <= 10
            assert result["evaluation"]["rubric_version"] == "keyword-coverage-v1"
            if i < 2:
                assert result["next_question"]["id"] not in seen
                seen.add(result["next_question"]["id"])
            else:
                assert result["next_question"] is None
                assert result["progress"]["finished"] is True

        summary = client.get(f"{BASE}/{session_id}").json()
        assert summary["progress"]["answered"] == 3
        assert len(summary["turns"]) == 3
        assert summary["categories"]


def test_llm_evaluator_is_used_and_promotes_level() -> None:
    with client_for(llm_client_factory=StaticLLM) as client:
        session_id = client.post(BASE, json={"starting_level": "MID", "max_questions": 4}).json()[
            "session_id"
        ]
        levels = []
        for _ in range(3):
            result = client.post(f"{BASE}/{session_id}/answers", json={"answer": "answer"}).json()
            levels.append(result["level_after"])
            assert result["evaluation"]["score"] == 9.0

        assert levels == ["MID", "MID", "SENIOR"]
        assert result["next_question"]["level"] == "SENIOR"


def test_answering_a_finished_interview_is_a_conflict() -> None:
    with client_for() as client:
        session_id = client.post(BASE, json={"max_questions": 1}).json()["session_id"]
        client.post(f"{BASE}/{session_id}/answers", json={"answer": GOOD_ANSWER})

        again = client.post(f"{BASE}/{session_id}/answers", json={"answer": GOOD_ANSWER})
        assert again.status_code == 409


def test_unknown_session_is_404() -> None:
    with client_for() as client:
        assert client.get(f"{BASE}/nope").status_code == 404
        assert client.post(f"{BASE}/nope/answers", json={"answer": "x"}).status_code == 404


@pytest.mark.parametrize(
    "payload",
    [
        {"answer": ""},
        {"answer": "x" * 8001},
    ],
)
def test_invalid_answers_are_rejected(payload) -> None:
    with client_for() as client:
        session_id = client.post(BASE, json={}).json()["session_id"]
        assert client.post(f"{BASE}/{session_id}/answers", json=payload).status_code == 422


def test_invalid_start_requests_are_rejected() -> None:
    with client_for() as client:
        assert client.post(BASE, json={"starting_level": "GURU"}).status_code == 422
        assert client.post(BASE, json={"max_questions": 0}).status_code == 422


def test_semantic_retrieval_path_runs(tmp_path) -> None:
    pytest.importorskip("chromadb")
    from pathlib import Path

    from src.scripts.index_question_bank import index_question_bank
    from tests.scripts.test_index_question_bank import BANK, HashEmbedder

    persist = str(Path(tmp_path) / "chroma")
    index_question_bank(
        bank_path=BANK,
        persist_directory=persist,
        collection_name="questions",
        embedding_provider=HashEmbedder(),
    )

    with client_for(
        use_semantic_retrieval=True,
        embedding_provider=HashEmbedder(),
        chroma_persist_directory=persist,
    ) as client:
        started = client.post(BASE, json={"starting_level": "SENIOR", "cv_skills": ["rag"], "max_questions": 2})
        assert started.status_code == 201, started.text
        assert started.json()["question"]["level"] == "SENIOR"
