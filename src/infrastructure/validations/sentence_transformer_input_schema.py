from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SentenceTransformerTextSchema:
    text: str

    @classmethod
    def parse(cls, text: str) -> "SentenceTransformerTextSchema":
        if text is None or not isinstance(text, str):
            raise TypeError("Text must be a string.")

        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Text cannot be empty.")

        return cls(text=cleaned_text)


@dataclass(frozen=True)
class SentenceTransformerBatchTextSchema:
    texts: list[str]

    @classmethod
    def parse(cls, texts: list[str]) -> "SentenceTransformerBatchTextSchema":
        if not isinstance(texts, list):
            raise TypeError("Texts must be a list of strings.")

        if not texts:
            raise ValueError("Texts cannot be empty.")

        normalized_texts = [SentenceTransformerTextSchema.parse(text).text for text in texts]

        return cls(texts=normalized_texts)