"""Compatibility layer for legacy/new Chroma package layouts.

This module avoids eager hard imports so partial environments still work.
"""

from __future__ import annotations

from typing import Any


def _safe_import(path: str, name: str) -> Any:
    module = __import__(path, fromlist=[name])
    return getattr(module, name)


ChromaMetadataMapper = None
ChromaVectorStore = None
ChromaQuestionVectorStore = None

for module_path, symbol in [
    (
        "src.infrastructure.vector_stores.chroma.chroma_metadata_mapper",
        "ChromaMetadataMapper",
    ),
    (
        "src.infrastructure.vector_stores.question_chrome.chroma_metadata_mapper",
        "ChromaMetadataMapper",
    ),
]:
    try:
        ChromaMetadataMapper = _safe_import(module_path, symbol)
        break
    except ModuleNotFoundError:
        continue

for module_path, symbol in [
    (
        "src.infrastructure.vector_stores.chroma.chroma_vector_store",
        "ChromaVectorStore",
    ),
    (
        "src.infrastructure.vector_stores.question_chrome.chroma_vector_store",
        "ChromaVectorStore",
    ),
]:
    try:
        ChromaVectorStore = _safe_import(module_path, symbol)
        break
    except ModuleNotFoundError:
        continue

# Optional: not required by indexing scripts.
for module_path, symbol in [
    (
        "src.infrastructure.vector_stores.chroma.chroma_question_vector_store",
        "ChromaQuestionVectorStore",
    ),
    (
        "src.infrastructure.vector_stores.question_chrome.chroma_question_vector_store",
        "ChromaQuestionVectorStore",
    ),
]:
    try:
        ChromaQuestionVectorStore = _safe_import(module_path, symbol)
        break
    except ModuleNotFoundError:
        continue

__all__ = [
    "ChromaMetadataMapper",
    "ChromaVectorStore",
    "ChromaQuestionVectorStore",
]