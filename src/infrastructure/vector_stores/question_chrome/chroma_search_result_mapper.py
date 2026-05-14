from typing import Any

from src.domain.retrieval.search_result import SearchResult


class ChromaSearchResultMapper:
    """
    ChromaDB query sonucunu domain-safe SearchResult listesine dönüştüren
    infrastructure mapper sınıfıdır.

    Bu sınıfın temel amacı, ChromaDB'nin provider-specific raw response
    formatını domain/application katmanından izole etmektir.

    ChromaDB query response genellikle nested list yapısı döndürür.

    Örnek raw response:
        {
            "ids": [["q1", "q2"]],
            "documents": [["Question text 1", "Question text 2"]],
            "metadatas": [[{...}, {...}]],
            "distances": [[0.12, 0.34]]
        }

    Domain/service katmanı bu formatı bilmemelidir.

    Neden?
        Eğer service layer doğrudan:
            raw["ids"][0][index]
            raw["documents"][0][index]
            raw["metadatas"][0][index]

        gibi ChromaDB-specific yapılarla çalışırsa:

            - provider bağımlılığı oluşur
            - service layer kirlenir
            - test yazımı zorlaşır
            - ChromaDB değiştirmek maliyetli hale gelir
            - raw response parsing logic'i dağılır

    Bu mapper bu problemi çözer.

    Responsibility ayrımı:
        ChromaVectorStore:
            ChromaDB SDK ile iletişim kurar

        ChromaSearchResultMapper:
            raw ChromaDB response -> SearchResult dönüşümü yapar

        SearchResult:
            domain-safe retrieval result modelidir

    Bu sınıf ne yapar?
        - raw ChromaDB response okur
        - nested response grubunu güvenli şekilde çözer
        - metadata alanlarını güvenli şekilde çıkarır
        - type conversion yapar
        - eksik alanlarda fallback uygular
        - SearchResult listesi döndürür

    Bu sınıf ne yapmaz?
        - ChromaDB query çalıştırmaz
        - embedding üretmez
        - semantic search hesaplamaz
        - reranking yapmaz
        - scoring yapmaz
        - vector store'a kayıt eklemez

    Defensive mapping yaklaşımı:
        Provider response'ları her zaman beklenen formatta olmayabilir.

        Örneğin:
            - documents eksik olabilir
            - metadatas boş olabilir
            - distances dönmeyebilir
            - metadata dict yerine None gelebilir
            - difficulty string gelebilir

        Bu mapper bu durumlarda pipeline'ı kırmak yerine güvenli fallback
        değerleri üretir.

    Bu yaklaşım production sistemlerde önemlidir.
    Çünkü retrieval pipeline'ın provider response edge-case'lerinde tamamen
    çökmesi istenmez.

    SearchResult neden gerekli?
        Çünkü service layer'ın ChromaDB formatını değil, provider bağımsız
        retrieval result modelini kullanması gerekir.

        Böylece ileride:
            - Qdrant
            - Pinecone
            - FAISS
            - pgvector

        gibi farklı vector store provider'ları aynı SearchResult modeline
        map edilebilir.
    """

    @classmethod
    def to_results(
        cls,
        raw: dict[str, Any],
    ) -> list[SearchResult]:
        """
        Raw ChromaDB query sonucunu SearchResult domain model listesine
        dönüştürür.

        Bu metod mapper'ın ana public entry-point'idir.

        Input:
            ChromaDB collection.query(...) çıktısı.

        Output:
            Provider-independent SearchResult listesi.

        Mapping akışı:
            1. ids ilk result group olarak alınır.
            2. ids boşsa boş liste döndürülür.
            3. documents, metadatas ve distances güvenli şekilde okunur.
            4. Her id için SearchResult oluşturulur.
            5. Eksik field'larda fallback değerler kullanılır.

        Neden ids boşsa direkt [] dönülüyor?
            Çünkü retrieval sonucunun ana belirleyicisi id listesidir.

            id yoksa anlamlı SearchResult üretilemez.

        Metadata nasıl kullanılıyor?
            Chroma metadata içindeki:
                - category
                - level
                - difficulty
                - question_type

            alanları SearchResult modeline aktarılır.

        Args:
            raw:
                ChromaDB collection.query(...) sonucu.

        Returns:
            list[SearchResult]:
                Domain-safe retrieval result listesi.

                Sonuç yoksa boş liste döner.
        """

        ids = cls._get_first_result_group(
            raw=raw,
            key="ids",
        )

        if not ids:
            return []

        documents = cls._get_first_result_group(
            raw=raw,
            key="documents",
        )

        metadatas = cls._get_first_result_group(
            raw=raw,
            key="metadatas",
        )

        distances = cls._get_first_result_group(
            raw=raw,
            key="distances",
        )

        results: list[SearchResult] = []

        for index, item_id in enumerate(ids):
            metadata = cls._safe_get(
                values=metadatas,
                index=index,
                default={},
            )

            if not isinstance(metadata, dict):
                metadata = {}

            result = SearchResult(
                id=str(item_id),
                text=str(
                    cls._safe_get(
                        values=documents,
                        index=index,
                        default="",
                    )
                ),
                category=str(metadata.get("category", "")),
                level=str(metadata.get("level", "")),
                difficulty=cls._to_int(
                    metadata.get("difficulty", 0),
                ),
                question_type=str(
                    metadata.get("question_type", ""),
                ),
                distance=cls._to_optional_float(
                    cls._safe_get(
                        values=distances,
                        index=index,
                        default=None,
                    )
                ),
            )

            results.append(result)

        return results


    @staticmethod
    def _get_first_result_group(
        raw: dict[str, Any],
        key: str,
    ) -> list[Any]:
        """
        ChromaDB'nin nested list response yapısından ilk result grubunu güvenli
        şekilde döndürür.

        ChromaDB çoğu query sonucunu şu formatta döndürür:

            raw[key] = [[...]]

        Bunun sebebi ChromaDB'nin batch query desteklemesidir.

        Örnek:
            ids = [["q1", "q2"]]

            burada:
                ids[0]

            ilk query'nin result grubudur.

        Bu projede çoğunlukla tek query embedding ile search yapıldığı için
        ilk result group alınır.

        Defensive davranış:
            Eğer key yoksa, değer list değilse veya ilk group list değilse
            boş liste döner.

        Bu sayede mapper provider response edge-case'lerinde kırılmaz.

        Args:
            raw:
                ChromaDB raw response dictionary'si.

            key:
                Okunacak response key'i.

                Örnek:
                    "ids"
                    "documents"
                    "metadatas"
                    "distances"

        Returns:
            list[Any]:
                İlk result group.

                Uygun format yoksa boş liste döner.
        """

        values = raw.get(key)

        if not values:
            return []

        if not isinstance(values, list):
            return []

        first_group = values[0]

        if not isinstance(first_group, list):
            return []

        return first_group


    @staticmethod
    def _safe_get(
        values: list[Any],
        index: int,
        default: Any,
    ) -> Any:
        """
        Liste içinden güvenli index okuma yapar.

        Bu helper IndexError riskini ortadan kaldırır.

        Neden gerekli?
            ChromaDB response içinde bazı alanların uzunluğu ids listesiyle
            birebir eşleşmeyebilir.

            Örneğin:
                ids var ama distances dönmemiş olabilir.

        Bu durumda direkt:
            values[index]

        kullanmak IndexError üretebilir.

        Bu helper:
            - index negatifse default döner
            - index liste dışında ise default döner
            - aksi halde values[index] döner

        Args:
            values:
                Okuma yapılacak liste.

            index:
                Okunacak index.

            default:
                Index geçersizse döndürülecek fallback değer.

        Returns:
            Any:
                Liste değeri veya default.
        """

        if index < 0:
            return default

        if index >= len(values):
            return default

        return values[index]


    @staticmethod
    def _to_int(
        value: Any,
    ) -> int:
        """
        Değeri güvenli şekilde int tipine dönüştürür.

        Bu helper özellikle metadata içindeki difficulty alanı için kullanılır.

        Neden gerekli?
            Metadata provider tarafından:
                - int
                - float
                - string number
                - None
                - invalid string

            olarak dönebilir.

        Geçerli örnekler:
            2 -> 2
            "3" -> 3

        Geçersiz örnek:
            "hard" -> 0

        Parse edilemeyen durumda 0 fallback döner.

        Args:
            value:
                Dönüştürülecek raw değer.

        Returns:
            int:
                Parse edilmiş integer veya fallback 0.
        """

        try:
            return int(value)
        except (TypeError, ValueError):
            return 0


    @staticmethod
    def _to_optional_float(
        value: Any,
    ) -> float | None:
        """
        Değeri güvenli şekilde optional float tipine dönüştürür.

        Bu helper özellikle distance alanı için kullanılır.

        distance neden optional?
            Çünkü bazı provider response'larında distance bilgisi dönmeyebilir.

        Geçerli örnekler:
            0.12 -> 0.12
            "0.34" -> 0.34

        Geçersiz örnek:
            "unknown" -> None

        Args:
            value:
                Dönüştürülecek raw değer.

        Returns:
            float | None:
                Parse edilmiş float değer veya None.
        """

        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None