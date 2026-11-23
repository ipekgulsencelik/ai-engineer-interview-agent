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


def test_default_retrieval_embedding_provider_is_fully_wired(monkeypatch) -> None:
    from unittest.mock import Mock

    from src.config.settings import settings
    from src.infrastructure.containers.retrieval_container import RetrievalContainer
    from src.infrastructure.embedding.sentence_transformer_model_loader import (
        SentenceTransformerModelLoader,
    )

    model = Mock()
    model.encode.return_value.tolist.return_value = [1.0, 0.0]
    loader = Mock(return_value=model)
    monkeypatch.setattr(SentenceTransformerModelLoader, "load", loader)

    provider = RetrievalContainer().embedding_provider
    assert provider.embed_text(text="RAG question") == [1.0, 0.0]
    loader.assert_called_once_with(model_name=settings.EMBEDDING_MODEL_NAME)
    model.encode.assert_called_once()


def test_chromadb_is_dev_only_not_a_runtime_requirement() -> None:
    import tomllib

    project = tomllib.loads(Path("pyproject.toml").read_text(encoding="utf-8"))
    runtime = project["project"]["dependencies"]
    dev = project["dependency-groups"]["dev"]
    assert not any(dep.startswith("chromadb") for dep in runtime)
    assert any(dep.startswith("chromadb") for dep in dev)

    lock = tomllib.loads(Path("uv.lock").read_text(encoding="utf-8"))
    root = next(
        package for package in lock["package"]
        if package["name"] == "ai-engineer-interview-agent"
    )
    assert not any(dep["name"] == "chromadb" for dep in root["dependencies"])
    assert any(
        dep["name"] == "chromadb"
        for dep in root["dev-dependencies"]["dev"]
    )
