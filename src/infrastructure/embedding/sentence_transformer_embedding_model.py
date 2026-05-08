from sentence_transformers import SentenceTransformer

from src.config.settings import settings
from src.interfaces.embedding_model import EmbeddingModel


class SentenceTransformerEmbeddingModel(
    EmbeddingModel,
):
    """
    sentence-transformers tabanlı embedding model implementation'ı.

    Bu sınıf:
        HuggingFace sentence-transformers ekosistemini kullanarak semantic
        text embedding üretir.

    Amaç:
        Text verilerini semantic vector representation'a dönüştürmek.

    Bu implementation hangi problemleri çözüyor?
        ✔ semantic search
        ✔ question retrieval
        ✔ vector similarity
        ✔ semantic clustering
        ✔ duplicate detection
        ✔ RAG retrieval
        ✔ CV skill matching
        ✔ semantic ranking

    sentence-transformers neden tercih ediliyor?
        Çünkü:
            - hızlıdır
            - local çalışabilir
            - yüksek semantic kalite sunar
            - production'da yaygın kullanılır
            - GPU desteği vardır
            - kolay fine-tune edilebilir

    Özellikle:
        all-MiniLM-L6-v2

    modeli:
        - hafif
        - hızlı
        - düşük latency
        - güçlü semantic quality

    sunduğu için Faz-1 için oldukça uygundur.

    Mimari yaklaşım:
        Bu sınıf:
            EmbeddingModel abstraction'ını implemente eder.

        Böylece application layer:
            sentence-transformers dependency'sini doğrudan bilmez.

    Mimari konum:
        Application / Retrieval Layer
                ↓
        EmbeddingModel interface
                ↓
        SentenceTransformerEmbeddingModel
                ↓
        sentence-transformers library

    Neden abstraction önemli?
        Çünkü ileride embedding backend'i değişebilir.

        Örneğin:
            - OpenAI embeddings
            - Cohere embeddings
            - local BGE models
            - Instructor models

        kullanılabilir.

    Bu implementation ne yapar?
        ✔ model loading
        ✔ single embedding generation
        ✔ batch embedding generation
        ✔ input validation
        ✔ numpy → Python list dönüşümü

    Bu implementation ne yapmaz?
        ✘ vector database storage
        ✘ semantic retrieval orchestration
        ✘ caching
        ✘ ranking
        ✘ embedding normalization
        ✘ async batching
        ✘ GPU lifecycle management

    Böylece Single Responsibility Principle korunur.

    Neden Python list dönüyoruz?
        Çünkü:
            numpy.ndarray

        doğrudan:
            - JSON serialize edilemez
            - API response için uygun değildir
            - bazı persistence layer'larla uyumsuz olabilir

        list[float]:
            ✔ serialization-friendly
            ✔ transport-safe
            ✔ persistence-friendly

    Önemli tasarım notu:
        Bu implementation:
            eager model loading

        kullanır.

        Yani:
            __init__ sırasında model memory'ye yüklenir.

        Avantaj:
            inference sırasında daha düşük latency

        Dezavantaj:
            startup cost oluşur

    Gelecekte eklenebilecek geliştirmeler:
        - lazy loading
        - GPU device selection
        - embedding normalization
        - async embedding
        - inference batching
        - caching layer
        - quantized models
        - ONNX acceleration
        - telemetry
        - retry strategy

    Example:
        model = SentenceTransformerEmbeddingModel()

        vector = model.embed(
            "Explain retrieval augmented generation."
        )

        print(len(vector))

    Output:
        384
    """

    def __init__(
        self,
        model_name: str | None = None,
    ) -> None:
        """
        SentenceTransformerEmbeddingModel instance'ı oluşturur.

        Args:
            model_name:
                Yüklenecek sentence-transformers model adı.

                Varsayılan:
                    settings.EMBEDDING_MODEL_NAME

                Bu model:
                    - hızlı
                    - hafif
                    - semantic olarak güçlü

                olduğu için Faz-1 retrieval sistemleri için uygundur.

                Alternatif örnekler:
                    - "all-mpnet-base-v2"
                    - "multi-qa-MiniLM-L6-cos-v1"
                    - "BAAI/bge-small-en"
                    - "intfloat/e5-base"

        Design Note:
            Model constructor sırasında memory'ye yüklenir.

            Böylece:
                - inference latency azalır
                - repeated load cost oluşmaz

            Ancak:
                startup süresi uzayabilir.

        Example:
            model = SentenceTransformerEmbeddingModel(
                model_name=settings.EMBEDDING_MODEL_NAME
            )
        """

        # ---------------------------------------------------------
        # MODEL LOADING
        # ---------------------------------------------------------
        # sentence-transformers modeli memory'ye yüklenir.
        #
        # Bu işlem:
        #   - model weights download
        #   - tokenizer loading
        #   - inference graph preparation        #
        # içerebilir.
        #
        # İlk çalıştırmada HuggingFace cache mekanizması kullanılabilir.
        self.model = SentenceTransformer(model_name or settings.EMBEDDING_MODEL_NAME)

    def embed(
        self,
        text: str,
    ) -> list[float]:
        """
        Tek bir text girdisi için embedding vector üretir.

        Akış:
            1. Input validation yapılır.
            2. sentence-transformers encode çalıştırılır.
            3. numpy array Python list'e dönüştürülür.
            4. embedding vector döndürülür.

        Args:
            text:
                Embedding üretilecek text girdisi.

                Örnek:
                    "How does vector search work?"

                Bu değer:
                    - question
                    - candidate answer
                    - CV skill
                    - retrieval query

                olabilir.

        Returns:
            list[float]:
                Text'in semantic embedding vector temsilidir.

                Örnek:
                    [0.123, -0.44, 0.98, ...]

                Vector dimension:
                    kullanılan modele bağlıdır.

                all-MiniLM-L6-v2 için:
                    384 dimension

        Raises:
            ValueError:
                text boş veya yalnızca whitespace içeriyorsa fırlatılır.

        Design Note:
            .tolist() dönüşümü bilinçlidir.

            Çünkü:
                numpy.ndarray

            doğrudan:
                - JSON serialize edilemez
                - bazı persistence layer'larla uyumsuz olabilir

            Python list:
                ✔ transport-safe
                ✔ API-friendly
                ✔ persistence-friendly

        Example:
            embedding = model.embed(
                "Explain embeddings."
            )

            print(len(embedding))

        Output:
            384
        """

        # ---------------------------------------------------------
        # INPUT VALIDATION
        # ---------------------------------------------------------
        # Boş text semantic embedding için anlamlı değildir.
        #
        # strip():
        #   yalnızca whitespace içeren string'leri de engeller.
        #
        # Bu validation:
        #   - invalid inference request
        #   - provider crash
        #   - meaningless vectors
        #
        # oluşmasını önler.
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        # ---------------------------------------------------------
        # EMBEDDING GENERATION
        # ---------------------------------------------------------
        # sentence-transformers encode() çağrılır.
        #
        # Bu işlem:
        #   text → dense semantic vector
        #
        # dönüşümünü gerçekleştirir.
        #
        # Dönen değer genellikle:
        #   numpy.ndarray
        embedding = self.model.encode(text)

        # ---------------------------------------------------------
        # NUMPY → LIST CONVERSION
        # ---------------------------------------------------------
        # numpy array Python list'e dönüştürülür.
        #
        # Böylece embedding:
        #   - serialize edilebilir
        #   - API response olarak kullanılabilir
        #   - vector DB'ye gönderilebilir
        return embedding.tolist()

    def embed_batch(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        """
        Birden fazla text için batch embedding üretir.

        Batch inference neden önemli?
            Çünkü production retrieval sistemlerinde:
                tek tek embedding üretmek

            ciddi performans problemi oluşturabilir.

        Batch inference avantajları:
            ✔ daha yüksek throughput
            ✔ daha iyi GPU utilization
            ✔ daha düşük toplam latency
            ✔ daha ölçeklenebilir retrieval pipeline

        Akış:
            1. Input validation yapılır.
            2. Batch encode çalıştırılır.
            3. Her embedding Python list'e dönüştürülür.
            4. Embedding listesi döndürülür.

        Args:
            texts:
                Embedding üretilecek text listesi.

                Örnek:
                    [
                        "What is RAG?",
                        "Explain embeddings.",
                        "How does vector search work?"
                    ]

        Returns:
            list[list[float]]:
                Her text için embedding vector listesi.

                Yapı:
                    [
                        [0.1, 0.2, ...],
                        [0.9, -0.4, ...],
                    ]

                Output sırası:
                    input sırasıyla aynı olmalıdır.

        Raises:
            ValueError:
                texts listesi boşsa fırlatılır.

        Design Note:
            Batch inference:
                production-scale semantic retrieval sistemlerinde kritik
                optimizasyonlardan biridir.

            Özellikle:
                - indexing
                - corpus ingestion
                - retrieval warmup

            sırasında büyük performans farkı yaratır.

        Example:
            embeddings = model.embed_batch([
                "What is RAG?",
                "Explain embeddings."
            ])

            print(len(embeddings))

        Output:
            2
        """

        # ---------------------------------------------------------
        # INPUT VALIDATION
        # ---------------------------------------------------------
        # Boş batch embedding isteği anlamsızdır.
        #
        # En az bir text bulunmalıdır.
        if not texts:
            raise ValueError("Texts cannot be empty.")

        # ---------------------------------------------------------
        # BATCH EMBEDDING GENERATION
        # ---------------------------------------------------------
        # sentence-transformers batch encode çalıştırılır.
        #
        # Bu yaklaşım:
        #   - daha hızlıdır
        #   - daha verimlidir
        #   - GPU kullanımını optimize eder
        #
        # Dönen yapı:
        #   numpy.ndarray collection
        embeddings = self.model.encode(texts)

        # ---------------------------------------------------------
        # NUMPY → LIST CONVERSION
        # ---------------------------------------------------------
        # Her embedding serialization-friendly Python list'e dönüştürülür.
        #
        # Böylece:
        #   - JSON transport
        #   - API response
        #   - vector DB persistence
        #
        # daha güvenli hale gelir.
        return [embedding.tolist() for embedding in embeddings]
