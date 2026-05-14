import math
from collections.abc import Sequence


class ChromaEmbeddingValidator:
    """
    ChromaDB'ye gönderilecek embedding vektörlerini doğrulayan merkezi
    validator sınıfıdır.

    Bu sınıfın temel amacı, ChromaVectorStore adapter'ına geçmeden önce
    embedding verisinin teknik olarak güvenli ve provider tarafından kabul
    edilebilir formatta olduğunu doğrulamaktır.

    Neden gerekli?
        Vector database sistemleri embedding verisi konusunda oldukça hassastır.

        Hatalı embedding örnekleri:
            - boş embedding
            - string/bytes değer
            - farklı dimension'a sahip batch embedding'ler
            - NaN içeren vektör
            - infinity içeren vektör
            - numeric olmayan item
            - bool değer

        Bu tür hatalar ChromaDB tarafında:
            - runtime exception
            - indexing failure
            - search failure
            - silent data corruption
            - dimension mismatch

        gibi problemlere yol açabilir.

    Bu validator bu hataları ChromaDB'ye veri gönderilmeden önce yakalar.

    Bu sınıf neden ayrı tutuldu?
        Eğer embedding validation logic doğrudan ChromaVectorStore içine
        yazılırsa:

            - ChromaVectorStore şişer
            - validation logic tekrar kullanılmaz
            - test yazımı zorlaşır
            - batch validation kuralları dağılır
            - adapter'ın sorumluluğu artar

        Bu nedenle embedding validation ayrı bir sınıfa taşınmıştır.

    Responsibility ayrımı:
        ChromaEmbeddingValidator:
            embedding formatını doğrular

        ChromaVectorStore:
            ChromaDB ile persistence/search işlemlerini yönetir

        EmbeddingModel:
            text -> embedding dönüşümü yapar

    Bu ayrım neden önemli?
        Çünkü:
            embedding üretimi
                ile
            embedding doğrulama
                ile
            vector store persistence

        farklı sorumluluklardır.

    Bu sınıf ne yapar?
        - tekil embedding doğrular
        - batch embedding listesi doğrular
        - dimension consistency kontrol eder
        - NaN değerleri reddeder
        - infinity değerleri reddeder
        - bool değerleri reddeder
        - numeric olmayan değerleri reddeder

    Bu sınıf ne yapmaz?
        - embedding üretmez
        - text encode etmez
        - ChromaDB'ye kayıt eklemez
        - semantic search yapmaz
        - metadata map etmez
        - SearchResult üretmez
        - vector similarity hesaplamaz

    Sequence kullanımı:
        list yerine Sequence kabul edilmiştir.

        Böylece:
            - list
            - tuple
            - numpy array benzeri sequence davranışı gösteren yapılar

        desteklenebilir.

        Ancak string ve bytes özellikle reddedilir.

    Neden string/bytes reddediliyor?
        Çünkü Python'da str ve bytes da Sequence kabul edilir.

        Örneğin:
            isinstance("abc", Sequence) == True

        Ancak embedding olarak string anlamsızdır.

    Neden bool reddediliyor?
        Çünkü Python'da bool, int'in subclass'ıdır.

        Yani:
            isinstance(True, int) == True

        Ancak embedding içinde True/False numeric embedding değeri olarak
        kabul edilmemelidir.

    Neden NaN ve infinity reddediliyor?
        Çünkü vector database sistemlerinde finite numeric değerler beklenir.

        NaN veya infinity:
            - similarity computation'ı bozabilir
            - index corruption oluşturabilir
            - arama sonuçlarını anlamsız hale getirebilir

    Bu validator özellikle:
        - ChromaVectorStore.add
        - ChromaVectorStore.add_many
        - ChromaVectorStore.search

    öncesinde kullanılmalıdır.
    """

    @classmethod
    def validate_embedding(
        cls,
        embedding: Sequence[float],
        *,
        field_name: str = "embedding",
    ) -> None:
        """
        Tek bir embedding vektörünü doğrular.

        Bu metod ChromaDB'ye gönderilecek tekil vector payload'ın geçerli
        olup olmadığını kontrol eder.

        Kurallar:
            1. embedding Sequence olmalıdır.
            2. embedding str veya bytes olamaz.
            3. embedding boş olamaz.
            4. her item int veya float olmalıdır.
            5. bool item kabul edilmez.
            6. NaN item kabul edilmez.
            7. infinity item kabul edilmez.

        Geçerli örnek:
            [0.12, -0.4, 0.88]

        Geçersiz örnekler:
            []
            "not-an-embedding"
            [0.1, "x", 0.3]
            [0.1, True]
            [0.1, float("nan")]
            [0.1, float("inf")]

        field_name neden var?
            Çünkü bu metod hem tekil hem batch validation içinde kullanılır.

            Batch validation sırasında hata mesajı şu şekilde üretilebilir:

                embeddings[2] cannot contain NaN values.

            Bu debugging'i kolaylaştırır.

        Args:
            embedding:
                Doğrulanacak embedding vector.

            field_name:
                Hata mesajlarında kullanılacak alan adı.

        Raises:
            TypeError:
                embedding sequence değilse veya str/bytes ise fırlatılır.

            ValueError:
                embedding boşsa veya geçersiz numeric değer içeriyorsa
                fırlatılır.
        """

        if isinstance(embedding, str | bytes):
            raise TypeError(f"{field_name} must be a sequence of numbers.")

        if not isinstance(embedding, Sequence):
            raise TypeError(f"{field_name} must be a sequence of numbers.")

        if len(embedding) == 0:
            raise ValueError(f"{field_name} cannot be empty.")

        for index, value in enumerate(embedding):
            cls._validate_numeric_value(
                value=value,
                field_name=field_name,
                index=index,
            )

    @classmethod
    def validate_embeddings(
        cls,
        embeddings: Sequence[Sequence[float]],
        *,
        expected_count: int | None = None,
        field_name: str = "embeddings",
    ) -> None:
        """
        Batch embedding listesini doğrular.

        Bu metod özellikle add_many veya bulk indexing süreçlerinde kullanılır.

        Kurallar:
            1. embeddings Sequence olmalıdır.
            2. embeddings str veya bytes olamaz.
            3. embeddings boş olamaz.
            4. her item geçerli embedding olmalıdır.
            5. tüm embedding dimension değerleri aynı olmalıdır.
            6. expected_count verilirse batch length bununla eşleşmelidir.

        Dimension consistency neden önemli?
            Vector store collection'larında tüm embedding'lerin aynı dimension'a
            sahip olması gerekir.

        Örnek:
            Geçerli:
                [
                    [0.1, 0.2, 0.3],
                    [0.4, 0.5, 0.6],
                ]

            Geçersiz:
                [
                    [0.1, 0.2],
                    [0.4, 0.5, 0.6],
                ]

        expected_count neden var?
            Batch insert sırasında genellikle:

                ids
                texts
                embeddings
                metadatas

            listelerinin aynı uzunlukta olması gerekir.

            expected_count bu invariant'ın embedding tarafında da
            doğrulanmasını sağlar.

        Args:
            embeddings:
                Doğrulanacak embedding batch'i.

            expected_count:
                Beklenen embedding sayısı.

            field_name:
                Hata mesajlarında kullanılacak alan adı.

        Raises:
            TypeError:
                embeddings sequence değilse veya str/bytes ise fırlatılır.

            ValueError:
                batch boşsa, expected_count uyuşmuyorsa, item geçersizse
                veya dimension mismatch varsa fırlatılır.
        """

        if isinstance(embeddings, str | bytes):
            raise TypeError(f"{field_name} must be a sequence of embeddings.")

        if not isinstance(embeddings, Sequence):
            raise TypeError(f"{field_name} must be a sequence of embeddings.")

        if len(embeddings) == 0:
            raise ValueError(f"{field_name} cannot be empty.")

        if expected_count is not None and len(embeddings) != expected_count:
            raise ValueError(
                f"{field_name} count must match expected_count. "
                f"Expected {expected_count}, got {len(embeddings)}."
            )

        first_dimension = len(embeddings[0])

        for index, embedding in enumerate(embeddings):
            cls.validate_embedding(
                embedding=embedding,
                field_name=f"{field_name}[{index}]",
            )

            if len(embedding) != first_dimension:
                raise ValueError(
                    f"All embeddings must have the same dimension. "
                    f"Expected {first_dimension}, got {len(embedding)} "
                    f"at index {index}."
                )

    @staticmethod
    def _validate_numeric_value(
        value: object,
        field_name: str,
        index: int,
    ) -> None:
        """
        Embedding içindeki tek bir numeric değeri doğrular.

        Bu helper validate_embedding tarafından her embedding item için
        çağrılır.

        Kurallar:
            - int veya float olmalıdır
            - bool kabul edilmez
            - NaN kabul edilmez
            - infinity kabul edilmez

        Neden ayrı helper?
            Çünkü numeric item validation:
                - okunabilirliği artırır
                - test edilebilirliği kolaylaştırır
                - hata mesajlarını merkezi hale getirir

        Args:
            value:
                Doğrulanacak embedding item değeri.

            field_name:
                Hata mesajlarında kullanılacak parent field adı.

            index:
                Embedding içindeki item index'i.

        Raises:
            ValueError:
                value numeric değilse, bool ise, NaN ise veya infinity ise
                fırlatılır.
        """

        if isinstance(value, bool) or not isinstance(value, int | float):
            raise ValueError(
                f"{field_name} must contain only numeric values. "
                f"Invalid value at index {index}: {value!r}."
            )

        numeric_value = float(value)

        if math.isnan(numeric_value):
            raise ValueError(
                f"{field_name} cannot contain NaN values. "
                f"Invalid value at index {index}."
            )

        if math.isinf(numeric_value):
            raise ValueError(
                f"{field_name} cannot contain infinite values. "
                f"Invalid value at index {index}."
            )