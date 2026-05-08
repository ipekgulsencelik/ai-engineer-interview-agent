from dataclasses import dataclass


@dataclass(frozen=True)
class SearchResult:
    """
    Vector store veya semantic search sonucunu temsil eden domain model.
    """

    id: str
    text: str
    score: float
    metadata: dict

    def __post_init__(self) -> None:
        if not self.id.strip():
            raise ValueError("Search result id cannot be empty.")

        if not self.text.strip():
            raise ValueError("Search result text cannot be empty.")

        if self.score < 0:
            raise ValueError("Search result score cannot be negative.")
