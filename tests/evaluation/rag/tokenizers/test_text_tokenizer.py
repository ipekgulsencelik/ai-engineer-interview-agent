from __future__ import annotations

from src.evaluation.rag.tokenizers.text_tokenizer import TextTokenizer


def test_text_tokenizer_should_lowercase_split_and_remove_empty_tokens() -> None:
    assert TextTokenizer().tokenize("  RAG   Context RAG  ") == {"rag", "context"}
