from abc import ABC, abstractmethod


class EmbeddingModel(ABC):
    """
    Text embedding üreten modeller için abstraction layer.

    Bu interface'in amacı:
        Farklı embedding provider ve framework'lerini ortak bir contract
        altında birleştirmektir.

    Embedding nedir?
        Embedding:
            text verisinin yüksek boyutlu sayısal vektör temsiline
            dönüştürülmesidir.

        Bu vektörler sayesinde sistem:
            - semantic similarity
            - retrieval
            - clustering
            - reranking
            - recommendation
            - vector search

        gibi işlemleri gerçekleştirebilir.

    Interview sisteminde embedding neden önemli?
        Çünkü semantic-aware interview sistemleri:
            yalnızca keyword matching kullanmamalıdır.

        Bunun yerine:
            semantic understanding

        kullanmalıdır.

    Örnek kullanım alanları:
        ✔ semantic question retrieval
        ✔ CV skill matching
        ✔ weak area detection
        ✔ duplicate question prevention
        ✔ semantic diversity scoring
        ✔ vector database indexing
        ✔ retrieval-augmented interview flow

    Neden abstraction layer kullanıyoruz?
        Çünkü embedding backend'i zamanla değişebilir.

        Sistem bugün:
            sentence-transformers

        kullanırken yarın:
            OpenAI embeddings
            Cohere embeddings
            local embedding models

        kullanabilir.

    Eğer abstraction olmazsa:
        - application layer provider'a bağımlı olur
        - provider migration zorlaşır
        - test yazmak zorlaşır
        - tight coupling oluşur

    Bu interface sayesinde:
        ✔ provider independence
        ✔ loose coupling
        ✔ easier testing
        ✔ interchangeable embedding backends
        ✔ cleaner architecture
        ✔ scalable retrieval infrastructure

    Desteklenebilecek provider örnekleri:
        - sentence-transformers
        - OpenAI embeddings
        - Cohere embeddings
        - VoyageAI embeddings
        - Instructor embeddings
        - Ollama embeddings
        - local HuggingFace models

    Mimari konum:
        Application / Retrieval Layer
                ↓
        EmbeddingModel interface
                ↓
        Concrete implementations

    Örnek implementasyonlar:
        - SentenceTransformerEmbeddingModel
        - OpenAIEmbeddingModel
        - CohereEmbeddingModel
        - MockEmbeddingModel

    Bu interface hangi problemleri çözüyor?
        ✔ semantic infrastructure standardization
        ✔ retrieval portability
        ✔ model swapping
        ✔ experimentation flexibility
        ✔ provider isolation

    Önemli tasarım notu:
        Bu interface:
            embedding generation contract'ını tanımlar.

        Şunları içermez:
            ✘ vector database logic
            ✘ retrieval orchestration
            ✘ similarity scoring
            ✘ caching
            ✘ batching strategy internals
            ✘ model loading lifecycle

        Çünkü bunlar farklı katmanların sorumluluğudur.

    Gelecekte eklenebilecek method'lar:
        - dimension()
        - normalize()
        - similarity()
        - async_embed()
        - stream_embeddings()
        - token_count()
        - embedding_metadata()

    Neden tekil ve batch method ayrı?
        Çünkü:
            batch embedding

        production sistemlerinde ciddi performans avantajı sağlar.

        Batch inference:
            ✔ GPU utilization artırır
            ✔ throughput artırır
            ✔ latency amortization sağlar
            ✔ API maliyetini azaltabilir

    Example:
        model = SentenceTransformerEmbeddingModel()

        vector = model.embed(
            "How does RAG work?"
        )

        print(len(vector))
    """

    @abstractmethod
    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Tek bir text girdisi için embedding vector üretir.

        Bu method:
            semantic representation generation

        işlemini temsil eder.

        Input:
            doğal dil text

        Output:
            yüksek boyutlu dense vector

        Args:
            text:
                Embedding üretilecek ham text girdisi.

                Örnek:
                    "How does retrieval-augmented generation work?"

                Bu text:
                    - question
                    - CV skill
                    - interview answer
                    - documentation
                    - search query

                olabilir.

        Returns:
            list[float]:
                Text'in embedding vector temsilidir.

                Örnek:
                    [0.123, -0.88, 0.441, ...]

                Vector dimension:
                    kullanılan modele göre değişir.

                Örnek:
                    - 384
                    - 768
                    - 1024
                    - 1536

        Design Note:
            Bu interface yalnızca vector üretimini tanımlar.

            Şunları tanımlamaz:
                ✘ normalization strategy
                ✘ distance metric
                ✘ vector storage
                ✘ retrieval ranking

            Çünkü bunlar retrieval layer concern'dür.

        Example:
            embedding = model.embed(
                "Explain vector databases."
            )

            print(len(embedding))

        Output:
            384
        """

    @abstractmethod
    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Birden fazla text girdisi için batch embedding üretir.

        Bu method:
            high-throughput embedding generation

        işlemini temsil eder.

        Batch embedding neden önemli?
            Çünkü production-scale retrieval sistemlerinde:
                tek tek inference yapmak

            oldukça maliyetlidir.

        Batch inference avantajları:
            ✔ daha yüksek throughput
            ✔ daha iyi GPU utilization
            ✔ daha düşük toplam latency
            ✔ daha düşük API overhead
            ✔ daha ölçeklenebilir retrieval pipeline

        Args:
            texts:
                Embedding üretilecek text listesi.

                Örnek:
                    [
                        "What is RAG?",
                        "Explain embeddings.",
                        "How does vector search work?"
                    ]

                Liste:
                    - question bank
                    - CV skill chunks
                    - retrieval documents
                    - semantic search corpus

                içerebilir.

        Returns:
            list[list[float]]:
                Her input text için embedding vector listesi.

                Yapı:
                    [
                        [0.1, 0.2, ...],
                        [0.7, -0.4, ...],
                        ...
                    ]

                Output sırası:
                    input sırasıyla aynı olmalıdır.

        Design Note:
            Batch processing implementation detayları:
                - batching size
                - async execution
                - GPU scheduling
                - provider chunking

            gibi konular concrete implementation'a bırakılmıştır.

        Example:
            embeddings = model.embed_batch([
                "What is RAG?",
                "Explain embeddings."
            ])

            print(len(embeddings))

        Output:
            2
        """
