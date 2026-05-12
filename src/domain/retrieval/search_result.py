from dataclasses import dataclass, field
from typing import Any

from src.domain.enums.level import Level
from src.domain.enums.question_type import QuestionType
from src.domain.validators.search_result_validator import (
    SearchResultValidator,
)


@dataclass(frozen=True)
class SearchResult:
    """
    Semantic retrieval sonucunda dönen tek bir kaydı temsil eden immutable
    domain modelidir.

    Bu modelin temel amacı, vector database provider'larının raw response
    formatını application/service katmanından tamamen izole etmektir.

    Temel fikir:
        Semantic retrieval sistemleri genellikle:
            - ChromaDB
            - Pinecone
            - Qdrant
            - FAISS
            - pgvector

        gibi provider'lar kullanır.

        Ancak bu provider'ların response formatları:
            - provider-specific
            - nested
            - type-safe olmayan
            - infrastructure odaklı

        yapılardır.

    Örnek ChromaDB response:
        {
            "ids": [["q1"]],
            "documents": [["Question text"]],
            "metadatas": [[{...}]],
            "distances": [[0.12]]
        }

    Service layer bu formatı bilmemelidir.

    Bunun yerine:
        raw provider response
            ↓
        mapper
            ↓
        SearchResult

    dönüşümü yapılır.

    Bu model neden gerekli?
        Çünkü raw provider response'ları:
            - provider bağımlıdır
            - nested dict/list yapısındadır
            - type-safe değildir
            - IDE autocomplete desteği zayıftır
            - test yazmayı zorlaştırır
            - service logic'i kirletir

    SearchResult bu problemleri çözer.

    Bu model neyi temsil eder?
        Semantic similarity sonucunda bulunan:
            - kayıt id'si
            - kayıt text'i
            - retrieval metadata'sı
            - similarity bilgisi

        gibi retrieval sonucu bilgilerini temsil eder.

    Bu model ne değildir?
        - ChromaDB response modeli değildir
        - provider SDK modeli değildir
        - reranking sonucu değildir
        - LLM output modeli değildir
        - Question entity değildir
        - persistence modeli değildir

    SearchResult neden Question değil?
        Çünkü retrieval sonucu:
            Question entity'sinden daha genel bir kavramdır.

        Aynı retrieval sistemi ileride:
            - document chunk
            - candidate note
            - interview memory
            - semantic cache item

        gibi farklı semantic kayıtları da döndürebilir.

    SearchResult:
        generic retrieval abstraction sağlar.

    Bu model neden immutable?
        Çünkü retrieval sonucu:
            runtime snapshot

        bilgisidir.

        Oluşturulduktan sonra mutate edilmesi:
            - retrieval consistency sorunları
            - cache problemleri
            - debugging zorluğu

        oluşturabilir.

    frozen=True avantajları:
        - immutable state
        - thread safety
        - predictable behavior
        - safer caching
        - deterministic debugging

    sağlar.

    Bu model ne yapar?
        - retrieval sonucu taşır
        - semantic metadata taşır
        - similarity bilgisi taşır
        - type-safe retrieval state sağlar

    Bu model ne yapmaz?
        - semantic search yapmaz
        - reranking yapmaz
        - embedding üretmez
        - provider query çalıştırmaz
        - scoring yapmaz
        - LLM çağırmaz

    Validation neden gerekli?
        Çünkü retrieval pipeline provider response'larına bağlıdır.

        Provider response'ları:
            - malformed olabilir
            - eksik alan içerebilir
            - yanlış type döndürebilir

        SearchResultValidator:
            model integrity sağlar.

    Bu model özellikle:
        - retrieval services
        - semantic search pipelines
        - RAG systems
        - AI interview systems
        - reranking pipelines

    için kritik abstraction sağlar.
    """

    id: str
    """
    Retrieval sonucu bulunan semantic kaydın benzersiz identifier değeri.

    Bu id genellikle:
        - question id
        - document chunk id
        - memory id
        - semantic entity id

    gibi retrieval target identifier'ını temsil eder.

    Örnek:
        "rag_mid_001"

    Bu alan retrieval sonucu ile domain entity arasında bağlantı kurmak için
    kritik öneme sahiptir.
    """

    text: str
    """
    Retrieval sonucu bulunan semantic kaydın ham text içeriği.

    Bu text:
        - semantic similarity
        - reranking
        - prompt building
        - debugging
        - analytics

    gibi işlemlerde kullanılabilir.

    Örnek:
        "Explain how vector embeddings work in semantic retrieval systems."
    """

    category: str
    """
    Retrieval sonucu kaydın category bilgisi.

    Bu alan genellikle:
        - retrieval filtering
        - analytics
        - reranking
        - interview balancing

    için kullanılır.

    Örnek:
        "RAG"
        "MLOps"
        "Vector DB"
    """

    level: Level | str
    """
    Retrieval sonucu kaydın seviye bilgisi.

    Genellikle:
        - JR
        - MID
        - SENIOR

    gibi interview level bilgisini temsil eder.

    Neden Level | str?
        Çünkü retrieval provider metadata'sı çoğu zaman raw string döndürür.

        Parsing/normalization daha sonra yapılabilir.
    """

    difficulty: int
    """
    Retrieval sonucu kaydın difficulty seviyesi.

    Bu alan:
        - adaptive pacing
        - difficulty balancing
        - scoring
        - fatigue-aware selection

    gibi mekanizmalarda kullanılabilir.

    Örnek:
        1 -> kolay
        2 -> orta
        3 -> zor
    """

    question_type: QuestionType | str
    """
    Retrieval sonucu kaydın question type bilgisi.

    Örnek:
        - conceptual
        - debugging
        - scenario
        - system_design

    Bu alan:
        - diversity balancing
        - fatigue detection
        - interview pacing

    için kullanılabilir.

    Neden QuestionType | str?
        Çünkü retrieval metadata provider'dan raw string olarak gelebilir.
    """

    similarity_score: float | None = None
    """
    Semantic similarity veya distance bazlı retrieval score değeri.

    Bu alan provider'a göre:
        - cosine similarity
        - semantic relevance
        - distance score
        - reranking score

    anlamına gelebilir.

    Neden optional?
        Çünkü bazı retrieval provider'ları score döndürmeyebilir.

    Örnek:
        0.91
        0.76

    Bu alan:
        - reranking
        - threshold filtering
        - analytics
        - explainability

    için kullanılabilir.
    """

    metadata: dict[str, Any] = field(default_factory=dict)
    """
    Retrieval sonucu kayda ait ek metadata bilgileri.

    Bu alan provider-specific veya retrieval-specific ek bilgileri taşıyabilir.

    Örnek:
        {
            "market_weight": 0.8,
            "followup_allowed": True,
        }

    Neden dict[str, Any]?
        Çünkü retrieval metadata esnek ve genişletilebilir olmalıdır.

    default_factory=dict neden kullanılıyor?
        Mutable default argument probleminden kaçınmak için.
    """

    def __post_init__(self) -> None:
        """
        SearchResult oluşturulduktan sonra domain validation çalıştırılır.

        Validation amacı:
            - retrieval result integrity sağlamak
            - malformed provider response'larını erken yakalamak
            - type consistency korumak

        SearchResultValidator tipik olarak:
            - id validation
            - text validation
            - similarity score validation
            - metadata validation
            - difficulty validation

        gibi kuralları çalıştırabilir.

        Neden burada validation yapılıyor?
            Çünkü retrieval pipeline:
                external provider response'larına dayanır.

            Bu nedenle defensive validation kritik öneme sahiptir.

        Fail-fast yaklaşımı:
            Invalid retrieval result bulunduğunda model creation aşamasında
            exception fırlatılır.
        """

        SearchResultValidator.validate(self)