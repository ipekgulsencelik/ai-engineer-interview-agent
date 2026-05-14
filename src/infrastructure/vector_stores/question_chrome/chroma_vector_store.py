import json
from pathlib import Path
from typing import Any

import chromadb

from src.domain.retrieval.search_result import SearchResult
from src.domain.retrieval.vector_store import VectorStore
from src.infrastructure.vector_stores.chroma.chroma_embedding_validator import (
    ChromaEmbeddingValidator,
)
from src.infrastructure.vector_stores.chroma.chroma_search_result_mapper import (
    ChromaSearchResultMapper,
)


class ChromaVectorStore(VectorStore):
    """
    ChromaDB tabanlı VectorStore implementasyonudur.

    Bu sınıf domain katmanındaki VectorStore abstraction contract'ını
    ChromaDB provider'ı ile gerçekleyen infrastructure adapter'dır.

    Temel amaç:
        Semantic retrieval işlemlerini ChromaDB üzerinden gerçekleştirmek.

    Mimari rol:
        VectorStore:
            domain/application port abstraction

        ChromaVectorStore:
            infrastructure adapter

    Böylece application/service katmanı:
        - chromadb SDK'sını
        - collection.query API'sini
        - Chroma response formatını
        - persistence detaylarını

    bilmek zorunda kalmaz.

    Bu yaklaşım:
        - Dependency Inversion Principle
        - Clean Architecture
        - Ports & Adapters
        - Hexagonal Architecture

    prensipleriyle uyumludur.

    Bu sınıfın sorumlulukları:
        - ChromaDB client oluşturmak
        - Collection oluşturmak veya mevcut collection'ı almak
        - Tekil vector kayıtlarını upsert etmek
        - Batch vector kayıtlarını upsert etmek
        - Query embedding ile semantic search yapmak
        - Raw Chroma sonucunu SearchResult modeline map etmek
        - Metadata validation yapmak
        - Input integrity doğrulamak

    Bu sınıfın sorumluluğu değildir:
        - embedding üretmek
        - Question -> metadata dönüşümü yapmak
        - reranking yapmak
        - scoring yapmak
        - LLM çağrısı yapmak
        - prompt oluşturmak
        - semantic similarity hesaplamak

    Neden generic tutuldu?
        Bu adapter yalnızca Question retrieval için tasarlanmamıştır.

        Aynı VectorStore ileride:
            - interview memory
            - RAG document chunks
            - candidate notes
            - semantic cache
            - retrieval memory

        gibi farklı semantic kayıt türleri için de kullanılabilir.

    Validation yaklaşımı:
        ChromaDB provider seviyesinde runtime error almamak için:
            - embedding validation
            - metadata validation
            - batch consistency validation
            - limit validation

        gibi kontroller persistence öncesinde yapılır.

    Bu neden önemli?
        Çünkü vector database sistemleri:
            - dimension mismatch
            - malformed metadata
            - invalid embeddings
            - NaN/infinity values

        gibi durumlarda runtime failure üretebilir.

    Bu adapter defensive programming yaklaşımı uygular.
    """

    def __init__(
        self,
        persist_directory: str | Path = "data/chroma",
        collection_name: str = "ai_engineer_questions",
    ) -> None:
        """
        ChromaVectorStore instance'ı oluşturur.

        Akış:
            1. persist_directory doğrulanır
            2. collection_name normalize edilir
            3. PersistentClient oluşturulur
            4. collection alınır veya oluşturulur

        persist_directory neyi temsil eder?
            ChromaDB persistent storage path'i.

            Chroma embedding index'i ve metadata burada tutulur.

        collection_name neyi temsil eder?
            Chroma collection identifier değeri.

            Aynı database içinde farklı semantic koleksiyonlar
            oluşturmak için kullanılır.

        Örnek:
            - ai_engineer_questions
            - interview_memory
            - rag_documents

        Args:
            persist_directory:
                Chroma persistent storage path'i.

            collection_name:
                Chroma collection adı.
        """

        self.persist_directory = self._validate_persist_directory(
            persist_directory,
        )

        self.collection_name = self._validate_collection_name(
            collection_name,
        )

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
        )

    def add(
        self,
        *,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
    ) -> None:
        """
        Tek bir semantic vector kaydını ChromaDB'ye ekler veya günceller.

        upsert davranışı:
            Eğer id mevcutsa:
                kayıt güncellenir

            Eğer id mevcut değilse:
                yeni kayıt oluşturulur

        Validation akışı:
            1. id validate edilir
            2. text validate edilir
            3. metadata validate edilir
            4. embedding validate edilir
            5. collection.upsert çağrılır

        Neden validation burada yapılıyor?
            Çünkü provider'a invalid payload göndermek:
                - runtime failure
                - corrupted index
                - provider-specific error

            oluşturabilir.

        Args:
            id:
                Semantic kayıt identifier değeri.

            text:
                Embedding'in temsil ettiği ham text.

            embedding:
                Önceden üretilmiş embedding vector.

            metadata:
                Retrieval filtering metadata dictionary'si.
        """

        self._validate_id(id)

        self._validate_text(text)

        self._validate_metadata(metadata)

        ChromaEmbeddingValidator.validate_embedding(
            embedding=embedding,
            field_name="embedding",
        )

        self.collection.upsert(
            ids=[id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
        )

    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Batch semantic kayıtları ChromaDB'ye ekler veya günceller.

        Bu metod özellikle:
            - indexing pipeline
            - question bank ingestion
            - bulk document loading

        için optimize edilmiştir.

        Batch yaklaşım avantajları:
            - daha az provider çağrısı
            - daha hızlı indexing
            - daha düşük overhead
            - toplu persistence

        Validation akışı:
            1. Batch input listeleri doğrulanır
            2. Embedding batch doğrulanır
            3. Chroma upsert çağrılır

        Batch invariant:
            ids
            texts
            embeddings
            metadatas

        listeleri aynı uzunlukta olmalıdır.

        Args:
            ids:
                Vector kayıt id listesi.

            texts:
                Text listesi.

            embeddings:
                Embedding vector listesi.

            metadatas:
                Metadata dictionary listesi.
        """

        self._validate_batch_inputs(
            ids=ids,
            texts=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        ChromaEmbeddingValidator.validate_embeddings(
            embeddings=embeddings,
            expected_count=len(ids),
            field_name="embeddings",
        )

        self.collection.upsert(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """
        Query embedding üzerinden semantic similarity search yapar.

        Akış:
            query embedding
                ↓
            Chroma collection.query(...)
                ↓
            raw Chroma response
                ↓
            ChromaSearchResultMapper
                ↓
            SearchResult listesi

        Semantic search nasıl çalışır?
            ChromaDB query embedding ile indexed embedding'ler arasında
            similarity hesaplar.

        limit neyi temsil eder?
            Döndürülecek maksimum sonuç sayısı.

        where ne için kullanılır?
            Metadata filtering.

        Örnek:
            where={
                "category": "RAG",
                "level": "MID",
            }

        Böylece semantic similarity belirli metadata filtreleriyle birlikte
        çalışabilir.

        Args:
            query_embedding:
                Semantic search embedding vector'ü.

            limit:
                Döndürülecek maksimum sonuç sayısı.

            where:
                Metadata filtering dictionary'si.

        Returns:
            list[SearchResult]:
                Semantic retrieval sonucu bulunan domain-safe sonuç listesi.
        """

        ChromaEmbeddingValidator.validate_embedding(
            embedding=query_embedding,
            field_name="query_embedding",
        )

        self._validate_limit(limit)

        if where is not None:
            self._validate_metadata(where, field_name="where")

        raw_result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            where=where,
        )

        return ChromaSearchResultMapper.to_results(raw_result)

    def count(self) -> int:
        """
        Collection içindeki toplam semantic kayıt sayısını döndürür.

        Kullanım alanları:
            - indexing validation
            - ingestion verification
            - test assertion
            - diagnostics

        Returns:
            int:
                Collection içindeki kayıt sayısı.
        """

        return int(self.collection.count())

    def reset(self) -> None:
        """
        Collection'ı silip yeniden oluşturur.

        Bu metod production runtime business flow'u için değil,
        infrastructure utility amacıyla tasarlanmıştır.

        Tipik kullanım alanları:
            - test reset
            - local development
            - re-indexing
            - corrupted index cleanup

        Dikkat:
            Bu işlem collection içindeki tüm semantic kayıtları siler.
        """

        self.client.delete_collection(
            name=self.collection_name,
        )

        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
        )