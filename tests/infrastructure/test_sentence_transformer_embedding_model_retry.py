import importlib
import sys
import types

import pytest


class DummyVector:
    def __init__(self, values: list[float]) -> None:
        self._values = values

    def tolist(self) -> list[float]:
        return self._values


class FlakySentenceTransformer:
    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self.calls = 0

    def encode(self, payload, **kwargs):  # noqa: ANN001
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("transient")
        if isinstance(payload, str):
            return DummyVector([0.1, 0.2])
        return [DummyVector([0.1]), DummyVector([0.2])]


def _load_model_module_with_fake_dependency(monkeypatch: pytest.MonkeyPatch):
    fake_module = types.ModuleType("sentence_transformers")
    fake_module.SentenceTransformer = FlakySentenceTransformer
    monkeypatch.setitem(sys.modules, "sentence_transformers", fake_module)
    fake_settings_module = types.ModuleType("src.config.settings")
    fake_settings_module.settings = types.SimpleNamespace(EMBEDDING_MODEL_NAME="dummy-model")
    monkeypatch.setitem(sys.modules, "src.config.settings", fake_settings_module)

    import src.infrastructure.embedding.sentence_transformer_embedding_model as model_module

    return importlib.reload(model_module)


def test_embed_retries_and_returns_list(monkeypatch: pytest.MonkeyPatch) -> None:
    model_module = _load_model_module_with_fake_dependency(monkeypatch)
    model = model_module.SentenceTransformerEmbeddingModel(retry_count=1)

    embedding = model.embed("hello")

    assert embedding == [0.1, 0.2]


def test_embed_batch_uses_validator_and_returns_lists(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    model_module = _load_model_module_with_fake_dependency(monkeypatch)
    model = model_module.SentenceTransformerEmbeddingModel(retry_count=1)

    embeddings = model.embed_batch([" a ", "b "])

    assert embeddings == [[0.1], [0.2]]