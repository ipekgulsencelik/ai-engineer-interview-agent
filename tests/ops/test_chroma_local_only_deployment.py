"""Fail-closed guardrails against accidentally exposing unpatched ChromaDB."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch


def test_chroma_factory_is_embedded_local_only(monkeypatch) -> None:
    from src.config.settings import settings

    monkeypatch.setattr(settings, "LEGACY_CHROMA_ENABLED", True)
    from src.infrastructure.vector_stores.chroma.chroma_client_factory import (
        create_chroma_client,
    )

    with patch(
        "src.infrastructure.vector_stores.chroma.chroma_client_factory."
        "chromadb.PersistentClient"
    ) as factory:
        returned = create_chroma_client(persist_directory="data/chroma")
        assert returned is factory.return_value
        factory.assert_called_once_with(path="data/chroma")


def test_all_chroma_infrastructure_code_disallows_remote_client() -> None:
    root = Path("src/infrastructure")
    offenders = []
    for filename in root.rglob("*.py"):
        source = filename.read_text(encoding="utf-8")
        if (
            "chromadb.HttpClient(" in source
            or "chromadb.AsyncHttpClient(" in source
            or "chromadb.CloudClient(" in source
        ):
            offenders.append(str(filename))
    assert offenders == []


def test_embedded_store_has_no_published_chroma_service() -> None:
    code = Path(
        "src/infrastructure/vector_stores/chroma/chroma_vector_store.py"
    ).read_text(encoding="utf-8")
    assert "chromadb.PersistentClient(" in code
    dockerfile = Path("Dockerfile.release").read_text(encoding="utf-8")
    compose = Path("docker-compose.yml").read_text(encoding="utf-8")
    assert "chroma run" not in dockerfile
    assert "chroma run" not in compose
    assert "8000" in dockerfile
    assert "chroma:" not in compose


def test_chroma_policy_blocks_production_and_staging(monkeypatch) -> None:
    import pytest

    from src.config.settings import settings
    from src.infrastructure.errors.vector_store_error import VectorStoreError
    from src.infrastructure.vector_stores.chroma.chroma_client_factory import (
        create_chroma_client,
    )

    monkeypatch.setattr(settings, "LEGACY_CHROMA_ENABLED", True)
    for environment in ("production", "staging", "PRODUCTION"):
        monkeypatch.setattr(settings, "ENV", environment)
        with pytest.raises(VectorStoreError, match="disabled"):
            create_chroma_client(persist_directory="data/chroma")


def test_default_retrieval_composition_is_chroma_free(tmp_path, monkeypatch) -> None:
    from src.config.settings import settings
    from src.infrastructure.containers.retrieval_container import RetrievalContainer
    from src.infrastructure.vector_stores.sqlite.sqlite_question_vector_store import (
        SqliteQuestionVectorStore,
    )

    monkeypatch.setattr(settings, "QUESTION_VECTOR_DB_PATH", str(tmp_path / "index.db"))
    assert isinstance(RetrievalContainer().vector_store, SqliteQuestionVectorStore)


def test_legacy_chroma_disabled_by_default_even_in_dev(monkeypatch) -> None:
    import pytest

    from src.config.settings import settings
    from src.infrastructure.errors.vector_store_error import VectorStoreError
    from src.infrastructure.vector_stores.chroma.chroma_client_factory import (
        create_chroma_client,
    )

    monkeypatch.setattr(settings, "ENV", "development")
    monkeypatch.setattr(settings, "LEGACY_CHROMA_ENABLED", False)
    with pytest.raises(VectorStoreError, match="disabled"):
        create_chroma_client(persist_directory="data/chroma")
