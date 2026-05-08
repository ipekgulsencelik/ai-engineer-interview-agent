import pytest

from src.domain.search.search_result import SearchResult


def test_search_result_can_be_created() -> None:
    result = SearchResult(
        id="q1",
        text="What is RAG?",
        score=0.92,
        metadata={"category": "RAG"},
    )

    assert result.id == "q1"
    assert result.text == "What is RAG?"
    assert result.score == 0.92
    assert result.metadata["category"] == "RAG"


def test_search_result_empty_id_raises_error() -> None:
    with pytest.raises(ValueError, match="Search result id cannot be empty"):
        SearchResult(id="", text="Valid text", score=0.5, metadata={})


def test_search_result_empty_text_raises_error() -> None:
    with pytest.raises(ValueError, match="Search result text cannot be empty"):
        SearchResult(id="q1", text="", score=0.5, metadata={})


def test_search_result_negative_score_raises_error() -> None:
    with pytest.raises(ValueError, match="Search result score cannot be negative"):
        SearchResult(id="q1", text="Valid text", score=-0.1, metadata={})
