from abc import ABC, abstractmethod

from src.domain.retrieval.search_result import SearchResult


class VectorStore(ABC):
    """
    Semantic retrieval ve vector database işlemleri için tanımlanan ortak
    domain port abstraction'ıdır.

    Bu interface'in temel amacı, application/service katmanını belirli bir
    vector database teknolojisine bağımlı olmaktan kurtarmaktır.

    Temel fikir:
        Retrieval sistemi şunu bilmemelidir:

            - ChromaDB mi kullanılıyor?
            - Pinecone mu?
            - Qdrant mı?
            - FAISS mi?
            - pgvector mü?
            - in-memory vector index mi?

        Application layer yalnızca şu capability ile ilgilenmelidir:

            "embedding tabanlı semantic retrieval yapılabiliyor mu?"

    Bu nedenle application/service katmanı:
        concrete provider SDK'larına değil,
        VectorStore abstraction'ına bağımlı olur.

    Bu yaklaşım hangi mimari prensibi uygular?
        Bu yapı:
            - Dependency Inversion Principle
            - Ports and Adapters
            - Clean Architecture
            - Hexagonal Architecture

        prensipleriyle uyumludur.

    Mimari rol:
        VectorStore:
            domain/application port

        ChromaVectorStore:
            infrastructure adapter

        PineconeVectorStore:
            infrastructure adapter

        QdrantVectorStore:
            infrastructure adapter

    Böylece retrieval servisleri provider bağımsız çalışabilir.

    Neden gerekli?
        Eğer retrieval servisleri doğrudan:

            chromadb.Client(...)
            pinecone.Index(...)
            qdrant_client.search(...)

        kullanırsa:

            - provider lock-in oluşur
            - test yazımı zorlaşır
            - migration maliyetli hale gelir
            - service katmanı infrastructure'a bağımlı olur
            - fake/mock vector store yazmak zorlaşır

    VectorStore abstraction bu problemleri çözer.

    Bu abstraction sayesinde:
        - provider değiştirilebilir
        - fake vector store yazılabilir
        - in-memory test retrieval yapılabilir
        - retrieval servisleri sadeleşir
        - infrastructure detayları izole edilir

    Bu sınıf ne yapar?
        - vector persistence contract'ı tanımlar
        - semantic search contract'ı tanımlar
        - retrieval-oriented storage API sunar

    Bu sınıf ne yapmaz?
        - embedding üretmez
        - text encode etmez
        - reranking yapmaz
        - LLM çağırmaz
        - prompt oluşturmaz
        - semantic scoring hesaplamaz
        - retrieval strategy belirlemez
        - provider SDK import etmez

    Çok önemli tasarım kararı:
        VectorStore string query almaz.
        VectorStore embedding alır.

    Neden?
        Çünkü:
            text -> embedding

        dönüşümü vector database'in sorumluluğu değildir.

        Bu responsibility:
            EmbeddingModel abstraction'ına aittir.

    Doğru akış:
        text
            ↓
        EmbeddingModel.embed(text)
            ↓
        embedding vector
            ↓
        VectorStore.search(query_embedding=...)

    Bu ayrım neden çok önemli?
        Çünkü embedding modeli ile vector database birbirinden tamamen
        bağımsız hale gelir.

    Böylece:
        - OpenAI embeddings + Chroma
        - BGE embeddings + Qdrant
        - Instructor embeddings + pgvector

        gibi kombinasyonlar mümkün olur.

    Bu interface neden domain layer'a yakın?
        Çünkü semantic retrieval artık business/application capability'sidir.

        Yani:
            "semantic similarity search"

        application davranışının parçasıdır.

        Ancak bunun nasıl yapıldığı:
            infrastructure concern'dür.

    Bu abstraction özellikle:
        - RAG systems
        - semantic retrieval
        - AI interview systems
        - vector search pipelines
        - memory retrieval
        - embedding search

    için kritik öneme sahiptir. :contentReference[oaicite:0]{index=0}
    """


    @abstractmethod
    def add(
        self,
        *,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
    ) -> None:
        """
        Vector store içerisine tek bir semantic kayıt ekleme/upsert contract'ı.

        Bu metod semantic retrieval sistemine yeni embedding kayıtları
        eklemek için kullanılır.

        Tipik kullanım alanları:
            - question indexing
            - document chunk indexing
            - interview memory storage
            - semantic cache
            - RAG knowledge ingestion

        Bu metod neden embedding alıyor?
            Çünkü embedding üretimi VectorStore'un sorumluluğu değildir.

        Beklenen akış:
            text
                ↓
            EmbeddingModel.embed(text)
                ↓
            embedding vector
                ↓
            VectorStore.add(...)

        Böylece:
            embedding provider
                ile
            vector database
        birbirinden bağımsız kalır.

        id neden gerekli?
            Çünkü retrieval sonucu ile domain entity arasında mapping gerekir.

        Örnek:
            question.id
                ↔
            vector store document id

        text neden saklanıyor?
            Çünkü retrieval sonucunda:
                - preview
                - reranking
                - debugging
                - analytics

            için orijinal text gerekebilir.

        metadata neden gerekli?
            Çünkü semantic retrieval çoğu zaman hybrid filtering ile birlikte
            kullanılır.

        Örnek:
            semantic similarity +
            metadata filtering

        where:
            {
                "category": "RAG",
                "level": "MID"
            }

        Bu yaklaşım retrieval precision'ı artırır.

        Args:
            id:
                Semantic kaydın benzersiz identifier değeri.

            text:
                Embedding'in temsil ettiği ham metin.

            embedding:
                Önceden üretilmiş embedding vektörü.

            metadata:
                Retrieval filtering için kullanılacak metadata bilgisi.

        Raises:
            ValueError:
                Concrete implementasyonlar:
                    - boş id
                    - boş embedding
                    - invalid metadata
                    - dimension mismatch

                durumlarında hata fırlatabilir.
        """
        raise NotImplementedError


    @abstractmethod
    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Vector store içerisine batch semantic kayıt ekleme/upsert contract'ı.

        Bu metod özellikle indexing pipeline'larında kullanılır.

        Örnek kullanım:
            - question bank indexing
            - document ingestion
            - RAG corpus loading
            - bulk semantic memory creation

        Neden add_many ayrı method?
            Çünkü birçok vector database:
                batch insert
            işlemlerini daha performanslı yapabilir.

        Örneğin:
            - tek network request
            - bulk indexing
            - optimized persistence
            - transaction batching

        avantajları sağlayabilir.

        Beklenen invariant:
            ids
            texts
            embeddings
            metadatas
        aynı uzunlukta olmalıdır.

        Çünkü her index:
            tek semantic kaydı temsil eder.

        Örnek:
            ids[0]
                ↔
            texts[0]
                ↔
            embeddings[0]
                ↔
            metadatas[0]

        Args:
            ids:
                Semantic kayıt id listesi.

            texts:
                Ham text listesi.

            embeddings:
                Embedding vector listesi.

            metadatas:
                Metadata dictionary listesi.

        Raises:
            ValueError:
                Concrete implementasyonlar:
                    - length mismatch
                    - invalid embedding
                    - duplicate ids
                    - malformed metadata

                durumlarında hata fırlatabilir.
        """
        raise NotImplementedError


    @abstractmethod
    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """
        Query embedding üzerinden semantic similarity search contract'ı.

        Bu metod retrieval sisteminin merkezindeki semantic search
        davranışını temsil eder.

        Akış:
            query text
                ↓
            EmbeddingModel.embed(query)
                ↓
            query embedding
                ↓
            VectorStore.search(...)

        Semantic search nasıl çalışır?
            Vector database:
                query embedding ile
                indexed embeddings arasında

            similarity hesaplar.

        Bu similarity çoğu zaman:
            - cosine similarity
            - dot product
            - euclidean distance

        kullanılarak ölçülür.

        limit neden var?
            Çünkü semantic retrieval genellikle:
                top-k retrieval

            şeklinde çalışır.

        Örnek:
            top 5 benzer soru

        where parametresi neden var?
            Çünkü retrieval çoğu zaman:
                semantic similarity +
                metadata filtering

            kombinasyonu kullanır.

        Örnek:
            where={"category": "RAG"}

            yalnızca RAG soruları arasında semantic search yapabilir.

        SearchResult neden dönüyor?
            Çünkü retrieval sonucu yalnızca text değildir.

            Genellikle:
                - id
                - text
                - metadata
                - similarity score
                - distance

            gibi bilgiler gerekir.

        Returns:
            list[SearchResult]:
                Semantic similarity sonucu bulunan kayıtlar.

                Sonuç bulunamazsa:
                    []

        Raises:
            ValueError:
                Concrete implementasyonlar:
                    - empty embedding
                    - invalid limit
                    - malformed filter

                durumlarında hata fırlatabilir.
        """
        raise NotImplementedError


    @abstractmethod
    def count(self) -> int:
        """
        Vector store içindeki toplam semantic kayıt sayısını döndüren
        contract metodudur.

        Bu metod özellikle:
            - indexing validation
            - collection health check
            - retrieval diagnostics
            - ingestion verification
            - integration testing

        için kullanılır.

        Örnek:
            repository question count
                ==
            vector store indexed count

        doğrulaması yapılabilir.

        Returns:
            int:
                Vector store içindeki toplam kayıt sayısı.
        """
        raise NotImplementedError