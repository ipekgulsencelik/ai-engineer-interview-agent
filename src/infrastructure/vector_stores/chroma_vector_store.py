import chromadb

from src.config.settings import settings
from src.domain.search.search_result import SearchResult
from src.interfaces.vector_store import VectorStore


class ChromaVectorStore(VectorStore):
    """
    ChromaDB tabanlı vector store implementation'ı.

    Bu sınıfın amacı:
        Embedding vector'lerini persistent şekilde saklamak ve semantic
        similarity search işlemleri gerçekleştirmektir.

    Vector store nedir?
        Vector store:
            embedding vector'lerini saklayan ve similarity search yapabilen
            specialized storage sistemidir.

        Geleneksel database'lerden farkı:
            exact keyword search yerine
            semantic similarity search yapabilmesidir.

    Örnek:
        Query:
            "How does retrieval work?"

        Sistem:
            exact keyword eşleşmesi yerine
            semantic olarak benzer içerikleri bulur.

    Interview sisteminde vector store neden önemli?
        Çünkü semantic-aware interview sistemleri:
            - intelligent question retrieval
            - semantic duplicate detection
            - CV matching
            - adaptive retrieval
            - semantic coverage analysis

        gibi yeteneklere ihtiyaç duyar.

    Bu implementation hangi problemleri çözüyor?
        ✔ semantic question retrieval
        ✔ vector persistence
        ✔ similarity search
        ✔ retrieval-augmented interview flow
        ✔ semantic ranking
        ✔ embedding-based lookup

    Neden ChromaDB kullanıyoruz?
        Çünkü ChromaDB:
            ✔ lightweight
            ✔ local-first
            ✔ easy setup
            ✔ Python-native
            ✔ embedding-friendly
            ✔ retrieval-focused

        olduğu için Faz-1 için oldukça uygundur.

    Mimari yaklaşım:
        Bu sınıf:
            VectorStore abstraction'ını implemente eder.

        Böylece application layer:
            doğrudan ChromaDB dependency'sine bağımlı olmaz.

    Mimari konum:
        Retrieval Layer
                ↓
        VectorStore interface
                ↓
        ChromaVectorStore
                ↓
        ChromaDB

    Bu implementation ne yapar?
        ✔ collection management
        ✔ vector persistence
        ✔ semantic search
        ✔ embedding storage
        ✔ similarity lookup

    Bu implementation ne yapmaz?
        ✘ embedding generation
        ✘ reranking
        ✘ hybrid retrieval
        ✘ caching
        ✘ query expansion
        ✘ semantic scoring strategy
        ✘ retrieval orchestration

    Böylece Single Responsibility Principle korunur.

    Neden persistent storage kullanıyoruz?
        Çünkü embedding corpus:
            uygulama restart olduğunda kaybolmamalıdır.

        PersistentClient sayesinde:
            - vector index disk'e yazılır
            - restart sonrası tekrar kullanılabilir
            - ingestion tekrar gerekmez

    Önemli tasarım notu:
        Bu implementation:
            vector similarity retrieval

        sağlar.

        Ancak production-scale sistemlerde:
            - reranking
            - metadata filtering
            - hybrid search
            - ANN tuning
            - sharding

        gibi gelişmiş katmanlar eklenebilir.

    Gelecekte eklenebilecek geliştirmeler:
        - metadata filtering
        - async search
        - hybrid BM25 + vector search
        - reranking pipeline
        - namespace support
        - collection versioning
        - caching layer
        - ANN optimization
        - telemetry
        - pagination

    Example:
        store = ChromaVectorStore()

        store.add(
            id="q1",
            text="What is RAG?",
            metadata={"category": "RAG"},
            embedding=[...],
        )

        results = store.search([...])
    """

    def __init__(
        self,
        collection_name: str | None = None,
        persist_directory: str | None = None,
    ) -> None:
        """
        ChromaVectorStore instance'ı oluşturur.

        Args:
            collection_name:
                Kullanılacak Chroma collection adı.

                Varsayılan:
                    "questions"

                Collection:
                    semantic vector namespace'i gibi düşünülebilir.

            persist_directory:
                ChromaDB verilerinin disk üzerinde saklanacağı dizin.

                Varsayılan:
                    "data/chroma"

        Design Note:
            PersistentClient kullanılması bilinçlidir.

            Böylece:
                - vector data disk'e yazılır
                - restart sonrası korunur
                - ingestion tekrar gerekmez

        Example:
            store = ChromaVectorStore(
                collection_name="interview_questions"
            )
        """

        # ---------------------------------------------------------
        # CHROMA CLIENT INITIALIZATION
        # ---------------------------------------------------------
        # Persistent ChromaDB client oluşturulur.
        #
        # path:
        #   embedding index'in disk üzerinde tutulacağı dizindir.
        #
        # Persistent yapı sayesinde:
        #   - vector corpus restart sonrası korunur
        #   - semantic index tekrar oluşturulmak zorunda kalmaz
        self.client = chromadb.PersistentClient(
            path=(persist_directory or settings.CHROMA_PERSIST_DIR),
        )

        # ---------------------------------------------------------
        # COLLECTION INITIALIZATION
        # ---------------------------------------------------------
        # Collection:
        #   vector namespace gibi davranır.
        #
        # Eğer collection mevcut değilse oluşturulur.
        #
        # Eğer mevcutsa reuse edilir.
        #
        # Bu yaklaşım:
        #   - idempotent startup
        #   - safer initialization        #
        # sağlar.
        self.collection = self.client.get_or_create_collection(
            name=(collection_name or settings.CHROMA_COLLECTION_NAME),
        )

    def add(
        self,
        id: str,
        text: str,
        metadata: dict,
        embedding: list[float],
    ) -> None:
        """
        Vector store içerisine yeni semantic kayıt ekler.

        Bu method:
            embedding indexing

        işlemini temsil eder.

        Args:
            id:
                Vector kaydının unique identifier'ı.

                Örnek:
                    "rag_jr_001"

            text:
                Embedding'e karşılık gelen ham text.

                Genellikle:
                    - question text
                    - document chunk
                    - interview content

                olabilir.

            metadata:
                Retrieval sırasında kullanılabilecek ek metadata bilgileri.

                Örnek:
                    {
                        "category": "RAG",
                        "level": "JR"
                    }

            embedding:
                Text'e ait semantic embedding vector.

                Örnek:
                    [0.12, -0.88, 0.44, ...]

        Returns:
            None

        Design Note:
            ChromaDB API:
                batch-oriented

            çalışır.

            Bu yüzden:
                tek kayıt bile olsa

            liste formatında gönderilir.

        Example:
            store.add(
                id="q1",
                text="Explain embeddings.",
                metadata={"category": "Embedding"},
                embedding=[...],
            )
        """

        # ---------------------------------------------------------
        # VECTOR INSERTION
        # ---------------------------------------------------------
        # Embedding vector Chroma collection içerisine eklenir.
        #
        # Saklanan bilgiler:
        #   - ids
        #   - raw text
        #   - metadata
        #   - embedding vector
        #
        # Böylece semantic retrieval sırasında:
        #   - similarity search
        #   - metadata access
        #
        # mümkün olur.
        self.collection.add(
            ids=[id],
            documents=[text],
            metadatas=[metadata],
            embeddings=[embedding],
        )

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[SearchResult]:
        """
        Semantic similarity search gerçekleştirir.

        Bu method:
            vector similarity retrieval

        işlemini temsil eder.

        Akış:
            1. Query embedding ChromaDB'ye gönderilir.
            2. En benzer vector'ler bulunur.
            3. Raw sonuçlar SearchResult modeline dönüştürülür.
            4. Structured sonuç listesi döndürülür.

        Args:
            query_embedding:
                Arama query'sinin embedding vector'ü.

                Bu embedding genellikle:
                    EmbeddingModel.embed()

                ile üretilir.

            limit:
                Döndürülecek maksimum sonuç sayısı.

                Varsayılan:
                    5

        Returns:
            list[SearchResult]:
                Semantic similarity sonuç listesi.

                Her sonuç:
                    - id
                    - text
                    - similarity score

                içerir.

        Design Note:
            ChromaDB:
                distance-based retrieval

            döndürür.

            Ancak application layer için:
                similarity score

            daha anlamlıdır.

            Bu yüzden:
                score = 1 - distance

            dönüşümü yapılır.

        Similarity score:
            Daha yüksek skor:
                → daha semantically benzer

            Daha düşük skor:
                → daha az benzer

        Example:
            results = store.search(
                query_embedding=[...],
                limit=3,
            )

            for result in results:
                print(result.text)
        """

        # ---------------------------------------------------------
        # VECTOR SIMILARITY QUERY
        # ---------------------------------------------------------
        # Query embedding kullanılarak semantic nearest-neighbor search
        # yapılır.
        #
        # Chroma:
        #   embedding similarity'ye göre en yakın kayıtları döndürür.
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
        )

        # ---------------------------------------------------------
        # RESULT CONTAINER
        # ---------------------------------------------------------
        # Structured SearchResult domain modelleri burada biriktirilir.
        search_results: list[SearchResult] = []

        # ---------------------------------------------------------
        # NULL CHECK
        # ---------------------------------------------------------
        # ChromaDB bazı durumlarda None döndürebilir.
        #
        # Bu durumlar:
        #   - collection boşsa
        #   - beklenmedik bir hata oluştuysa
        #   - query embedding ile ilgili bir sorun varsa
        #   - ChromaDB'nin iç işleyişi sırasında edge case'ler ortaya çıktıysa
        # olabilir.
        #
        # Bu kontrol:
        #   - typo kaynaklı hataları
        #   - normalize edilmemiş inputları
        #   - invalid state oluşmasını
        # önler.
        if (
            results["ids"] is None
            or results["documents"] is None
            or results["distances"] is None
            or results["metadatas"] is None
        ):
            return []

        # ---------------------------------------------------------
        # RAW RESULT EXTRACTION
        # ---------------------------------------------------------
        # Chroma batch-oriented response döndürür.
        #
        # Bu yüzden:
        #   ilk query sonucu alınır.
        ids = results["ids"][0]
        documents = results["documents"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        # ---------------------------------------------------------
        # DOMAIN RESULT MAPPING
        # ---------------------------------------------------------
        # Raw Chroma response'u SearchResult domain modeline dönüştürülür.
        #
        # distance:
        #   küçüldükçe similarity artar.
        #
        # Application tarafında daha anlaşılır olması için:
        #   similarity score = 1 - distance
        #
        # dönüşümü yapılır.
        #
        # Böylece:
        #   yüksek score → yüksek benzerlik
        for id_, document, distance, metadata in zip(
            ids,
            documents,
            distances,
            metadatas,
            strict=False,
        ):
            search_results.append(
                SearchResult(
                    id=id_,
                    text=document,
                    score=max(0.0, 1 - distance),
                    metadata=dict(metadata or {}),
                )
            )

        # ---------------------------------------------------------
        # FINAL SEARCH RESULTS
        # ---------------------------------------------------------
        # Structured semantic search sonuçları döndürülür.
        return search_results
