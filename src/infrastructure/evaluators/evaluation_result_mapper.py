from __future__ import annotations

from src.domain.results.evaluation_result import EvaluationResult
from src.infrastructure.evaluator.evaluation_metadata import (
    EvaluationMetadata,
)


class EvaluationResultMapper:
    """
    Raw evaluator/provider çıktısını domain-safe EvaluationResult ve
    EvaluationMetadata modellerine dönüştüren mapper sınıfı.

    Bu sınıf infrastructure katmanında yer alır.

    Çünkü bu sınıfın temel sorumluluğu:
        - raw dict okumak
        - provider response parsing yapmak
        - bozuk/veri eksikliği içeren payload'ları normalize etmek
        - güvenli type conversion uygulamak
        - fallback üretmek
        - provider metadata'yı ayrıştırmak
    gibi teknik/integration odaklı işlemlerdir.

    Bu işlemler domain concern değildir.

    Bu mapper neden gerekli?
        LLM/provider çıktıları çoğu zaman:
            - eksik field içerebilir
            - yanlış type dönebilir
            - malformed JSON olabilir
            - null field içerebilir
            - beklenmeyen format üretebilir

        Örneğin evaluator şu çıktıları dönebilir:

            {
                "score": "9",
                "confidence": "0.82"
            }

        veya:

            {
                "score": null,
                "feedback": ""
            }

        veya:

            {
                "technical_accuracy": "high"
            }

        Domain modeli bu tip bozuk/veri kalitesi düşük payload'ları
        doğrudan bilmemelidir.

        Çünkü domain katmanı:
            - temiz
            - deterministic
            - provider-independent
        kalmalıdır.

    Bu sınıf ne yapar?
        - raw provider dict okur
        - güvenli type conversion uygular
        - score değerlerini clamp eder
        - confidence değerini normalize eder
        - fallback değerler üretir
        - metadata modelini ayrıştırır
        - EvaluationResult oluşturur

    Bu sınıf ne yapmaz?
        - evaluator inference çalıştırmaz
        - OpenAI/Groq request göndermez
        - prompt üretmez
        - business rule yönetmez
        - interview flow yönetmez
        - scoring logic üretmez
        - persistence işlemi yapmaz

    Mapper vs Validator farkı:
        Mapper:
            unsafe/raw data -> safe domain object

        Validator:
            safe domain object -> rule checking

    Önemli tasarım yaklaşımı:
        Bu mapper defensive programming yaklaşımıyla yazılmıştır.

        Çünkü LLM/provider çıktıları tamamen güvenilir kabul edilmez.

        Örneğin:
            - string yerine int gelebilir
            - None gelebilir
            - field hiç olmayabilir
            - sayı yerine metin gelebilir

        Bu nedenle mapper:
            - exception fırlatmak yerine
            - mümkün olduğunca güvenli fallback üretmeye çalışır

    Örnek:
        "score": "999"

            -> clamp edilir
            -> 10.0 olur

        "confidence": "abc"

            -> parse edilemez
            -> 0.0 fallback uygulanır

    Bu yaklaşım neden önemli?
        Çünkü evaluator pipeline'ın:
            - provider hatalarında tamamen çökmesi
            yerine
            - degrade olarak çalışmaya devam etmesi
        production sistemlerde daha güvenlidir.
    """

    DEFAULT_FEEDBACK = "No feedback."
    """
    feedback alanı eksik veya boş geldiğinde kullanılacak default değer.

    Neden gerekli?
        Bazı provider response'ları feedback üretmeyebilir.
        Domain modelde ise boş feedback istenmeyebilir.

    Böylece:
        None yerine anlamlı fallback sağlanır.
    """

    DEFAULT_RUBRIC_VERSION = "v1"
    """
    rubric_version eksik olduğunda kullanılacak varsayılan rubric versiyonu.

    Bu alan:
        - analytics
        - evaluation reproducibility
        - audit trail

    açısından önemlidir.
    """

    @classmethod
    def to_result(
        cls,
        data: dict,
    ) -> EvaluationResult:
        """
        Raw evaluator/provider çıktısını EvaluationResult domain modeline
        dönüştürür.

        Bu metod:
            - unsafe input'u normalize eder
            - güvenli fallback üretir
            - numeric alanları clamp eder
            - string alanları sanitize eder

        Örnek:
            raw_data = {
                "score": "9",
                "feedback": None,
            }

            result = EvaluationResultMapper.to_result(raw_data)

        Sonuç:
            score -> 9.0
            feedback -> "No feedback."

        Args:
            data:
                Raw provider response dict'i.

        Returns:
            EvaluationResult:
                Domain-safe evaluation sonucu.
        """

        # Bu metodun sorumluluğu yalnızca domain result üretmektir.
        # Provider metadata'sını ayrıştırmaz.
        return EvaluationResult(
            score=cls._clamp_score(data.get("score", 0.0)),
            feedback=cls._to_non_empty_string(
                value=data.get("feedback"),
                fallback=cls.DEFAULT_FEEDBACK,
            ),
            technical_accuracy=cls._clamp_score(
                data.get("technical_accuracy", 0.0),
            ),
            depth=cls._clamp_score(data.get("depth", 0.0)),
            communication=cls._clamp_score(
                data.get("communication", 0.0),
            ),
            missing_keywords=cls._to_string_list(
                data.get("missing_keywords"),
            ),
            follow_up_question=cls._to_optional_non_empty_string(
                data.get("follow_up_question"),
            ),
            confidence=cls._clamp_confidence(
                data.get("confidence", 0.0),
            ),
            rubric_version=cls._to_non_empty_string(
                value=data.get("rubric_version"),
                fallback=cls.DEFAULT_RUBRIC_VERSION,
            ),
        )


    @classmethod
    def to_metadata(
        cls,
        data: dict,
    ) -> EvaluationMetadata:
        """
        Raw provider çıktısından EvaluationMetadata nesnesi üretir.

        Bu metod provider execution bilgilerini domain result'tan ayırır.

        Böylece:
            - provider telemetry
            - observability
            - debugging
            - analytics
        bilgileri ayrı tutulabilir.

        Metadata neden ayrı model?
            Çünkü:
                tokens_used
                latency_seconds
                raw_output
            gibi alanlar domain sonucu değildir.

            Bunlar evaluator execution bilgisi taşır.

        Args:
            data:
                Raw provider response dict'i.

        Returns:
            EvaluationMetadata:
                Infrastructure metadata modeli.
        """

        # Bu metodun sorumluluğu yalnızca metadata üretmektir.
        # Domain result üretmez.
        return EvaluationMetadata(
            raw_output=cls._to_optional_string(data.get("raw_output")),
            model_name=cls._to_optional_string(data.get("model_name")),
            tokens_used=cls._to_optional_int(data.get("tokens_used")),
            latency_seconds=cls._to_optional_float(
                data.get("latency_seconds"),
            ),
        )


    @classmethod
    def to_result_with_metadata(
        cls,
        data: dict,
    ) -> tuple[EvaluationResult, EvaluationMetadata]:
        """
        Raw provider çıktısını hem domain result hem metadata olarak döndürür.

        Bu helper metod özellikle service layer için kullanışlıdır.

        Böylece caller:
            - tek mapper çağrısıyla
            - hem domain sonucu
            - hem telemetry metadata'sını
        elde edebilir.

        Args:
            data:
                Raw provider response dict'i.

        Returns:
            tuple[EvaluationResult, EvaluationMetadata]:
                Domain result ve infrastructure metadata.
        """

        # Bu metodun sorumluluğu hem domain result hem metadata üretmektir.
        return cls.to_result(data), cls.to_metadata(data)


    @staticmethod
    def _clamp_score(
        value: object,
    ) -> float:
        """
        Score değerini güvenli şekilde numeric tipe dönüştürür ve
        0.0 - 10.0 aralığına sıkıştırır.

        Clamp neden gerekli?
            Çünkü provider bazen:
                - negatif değer
                - aşırı büyük değer
                - string sayı
            döndürebilir.

        Örnek:
            "15"
                -> 10.0

            "-5"
                -> 0.0

            "abc"
                -> 0.0

        Bu yaklaşım evaluator pipeline'ın çökmesini önler.

        Args:
            value:
                Raw score değeri.

        Returns:
            float:
                Normalize edilmiş score değeri.
        """

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            numeric_value = 0.0

        return max(0.0, min(10.0, numeric_value))


    @staticmethod
    def _clamp_confidence(
        value: object,
    ) -> float:
        """
        Confidence değerini güvenli şekilde numeric tipe dönüştürür ve
        0.0 - 1.0 aralığına sıkıştırır.

        Confidence semantics:
            0.0:
                düşük evaluator güveni

            1.0:
                yüksek evaluator güveni

        Örnek:
            "2.0"
                -> 1.0

            "-1"
                -> 0.0

            "abc"
                -> 0.0

        Args:
            value:
                Raw confidence değeri.

        Returns:
            float:
                Normalize edilmiş confidence değeri.
        """

        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            numeric_value = 0.0

        return max(0.0, min(1.0, numeric_value))


    @staticmethod
    def _to_non_empty_string(
        *,
        value: object,
        fallback: str,
    ) -> str:
        """
        Değeri güvenli şekilde boş olmayan string'e dönüştürür.

        Bu metod:
            - None kontrolü yapar
            - strip uygular
            - boş string kontrolü yapar
            - fallback üretir

        Örnek:
            None -> fallback
            "" -> fallback
            "   " -> fallback
            123 -> "123"

        Args:
            value:
                Dönüştürülecek raw değer.

            fallback:
                Geçersiz durumda kullanılacak varsayılan değer.

        Returns:
            str:
                Güvenli normalize edilmiş string.
        """

        if value is None:
            return fallback

        normalized_value = str(value).strip()

        if not normalized_value:
            return fallback

        return normalized_value


    @staticmethod
    def _to_optional_non_empty_string(
        value: object,
    ) -> str | None:
        """
        Değeri optional string formatına dönüştürür.

        Boş veya whitespace-only string durumunda None döner.

        Bu yaklaşım özellikle optional alanlar için önemlidir.

        Örnek:
            "" -> None
            "   " -> None
            None -> None
            "hello" -> "hello"

        Args:
            value:
                Raw değer.

        Returns:
            str | None:
                Normalize edilmiş optional string.
        """

        if value is None:
            return None

        normalized_value = str(value).strip()

        if not normalized_value:
            return None

        return normalized_value


    @staticmethod
    def _to_optional_string(
        value: object,
    ) -> str | None:
        """
        Değeri optional string'e dönüştürür.

        None ise None döner.
        Aksi halde str(...) uygulanır.

        Bu metod özellikle metadata alanlarında kullanılır.

        Args:
            value:
                Raw değer.

        Returns:
            str | None:
                String dönüşümü yapılmış değer.
        """

        if value is None:
            return None

        return str(value)


    @staticmethod
    def _to_optional_int(
        value: object,
    ) -> int | None:
        """
        Değeri güvenli şekilde optional int'e dönüştürür.

        Parse edilemeyen durumlarda exception yerine None döner.

        Bu yaklaşım evaluator pipeline robustness'ını artırır.

        Örnek:
            "123" -> 123
            "abc" -> None

        Args:
            value:
                Raw değer.

        Returns:
            int | None:
                Parse edilmiş integer veya None.
        """

        if value is None:
            return None

        try:
            return int(value)
        except (TypeError, ValueError):
            return None


    @staticmethod
    def _to_optional_float(
        value: object,
    ) -> float | None:
        """
        Değeri güvenli şekilde optional float'a dönüştürür.

        Parse başarısız olursa None döner.

        Bu metod özellikle:
            - latency_seconds
            - numeric metadata

        alanlarında kullanılır.

        Args:
            value:
                Raw değer.

        Returns:
            float | None:
                Parse edilmiş float veya None.
        """

        if value is None:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return None


    @staticmethod
    def _to_string_list(
        value: object,
    ) -> list[str]:
        """
        Değeri güvenli şekilde list[str] formatına dönüştürür.

        Bu metod:
            - None kontrolü yapar
            - list type kontrolü yapar
            - item'ları string'e çevirir
            - strip uygular
            - boş item'ları filtreler

        Örnek:
            [" rag ", "", "embedding"]

        dönüşür:

            ["rag", "embedding"]

        Neden defensive yaklaşım kullanılıyor?
            Çünkü provider response'ları tamamen güvenilir kabul edilmez.

        Args:
            value:
                Raw liste değeri.

        Returns:
            list[str]:
                Normalize edilmiş string listesi.
        """

        if value is None:
            return []

        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]

        if isinstance(value, str) and value.strip():
            return [value.strip()]

        return []