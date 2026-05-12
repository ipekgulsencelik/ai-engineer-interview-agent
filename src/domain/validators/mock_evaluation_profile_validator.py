import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.domain.evaluation.mock_evaluation_profile import (
        MockEvaluationProfile,
    )


class MockEvaluationProfileValidator:
    """
    MockEvaluationProfile domain modelinin metadata-driven invariant
    validation kurallarını yöneten validator sınıfıdır.

    Bu validator'ın temel amacı:
        MockEvaluator davranışını belirleyen MockEvaluationProfile
        configuration snapshot'ının her zaman güvenli, tutarlı ve
        beklenen domain sınırları içinde kalmasını sağlamaktır.

    ----------------------------------------------------------------------
    MOCK EVALUATION PROFILE VALIDATION NEDİR?
    ----------------------------------------------------------------------

    MockEvaluationProfile:
        deterministic mock evaluation çıktılarının nasıl üretileceğini
        tanımlayan immutable profile modelidir.

    Bu validator ise:
        profile içindeki her field'ın metadata kurallarına uygun olup
        olmadığını kontrol eder.

    Örneğin:
        - score finite mi?
        - score 0-10 aralığında mı?
        - confidence 0-1 aralığında mı?
        - feedback boş mu?
        - nullable alanlar doğru mu?
        - rubric_version geçerli mi?

    gibi kurallar burada uygulanır.

    ----------------------------------------------------------------------
    METADATA-DRIVEN VALIDATION
    ----------------------------------------------------------------------

    Bu validator field isimlerini hard-code etmek yerine
    dataclass field metadata bilgisini okur.

    Örneğin model tarafında:

        score: float = field(
            metadata={
                "type": (int, float),
                "finite": True,
                "min_value": 0.0,
                "max_value": 10.0,
            }
        )

    tanımı varsa, validator bu metadata bilgilerini runtime'da okuyarak
    ilgili validation kurallarını uygular.

    Bu yaklaşımın avantajları:

        - validator generic hale gelir
        - model self-documenting olur
        - validation behavior field declaration üzerinde görünür olur
        - yeni field eklemek kolaylaşır
        - Open/Closed Principle desteklenir
        - validation rule duplication azalır

    ----------------------------------------------------------------------
    VALIDATION KAPSAMI
    ----------------------------------------------------------------------

    Bu validator şu kontrolleri yapar:

        1. Model type validation
            Validate edilen nesnenin gerçekten MockEvaluationProfile
            olup olmadığını kontrol eder.

        2. Nullable handling
            nullable=True metadata'sı bulunan alanlarda None değerine
            izin verir.

        3. Runtime type validation
            Field metadata'sında belirtilen expected type'a göre
            value doğrulanır.

        4. Bool rejection
            Python'da bool int subclass'ı olduğu için numeric field'larda
            yanlışlıkla kabul edilmesini engeller.

        5. Finite validation
            NaN, infinity ve -infinity değerlerini reddeder.

        6. Non-empty string validation
            feedback ve rubric_version gibi string alanların boş
            olmamasını sağlar.

        7. Minimum value validation
            Numeric alanların minimum boundary altında kalmasını engeller.

        8. Maximum value validation
            Numeric alanların maximum boundary üstüne çıkmasını engeller.

    ----------------------------------------------------------------------
    NEDEN BOOL REDDEDİLİYOR?
    ----------------------------------------------------------------------

    Python'da bool tipi int'in subclass'ıdır.

    Bu nedenle:

        isinstance(True, int)

    sonucu True döner.

    Ancak domain açısından:

        score=True
        confidence=False

    geçerli numeric evaluation değerleri değildir.

    Bu validator bool değerleri explicit olarak reddeder.

    ----------------------------------------------------------------------
    NULLABLE FIELD DAVRANIŞI
    ----------------------------------------------------------------------

    Bazı alanlar bilinçli olarak nullable olabilir.

    Örneğin:

        follow_up_question: str | None

    Bu durumda metadata:

        "nullable": True

    olarak tanımlanır.

    Eğer value None ise:
        validator diğer type/non_empty/min/max kontrollerini çalıştırmaz.

    Eğer value None değilse:
        metadata'daki type ve diğer kurallar uygulanır.

    ----------------------------------------------------------------------
    DOMAIN SAFETY
    ----------------------------------------------------------------------

    Bu validator şu invalid state'leri engeller:

        - score = math.nan
        - score = math.inf
        - score = -1
        - score = 99
        - confidence = 2.5
        - feedback = ""
        - rubric_version = "   "
        - follow_up_question = 123

    Böylece MockEvaluator:
        her zaman güvenli ve predictable profile ile çalışır.

    ----------------------------------------------------------------------
    TYPE_CHECKING VE LAZY IMPORT
    ----------------------------------------------------------------------

    MockEvaluationProfile modeli __post_init__ içinde validator'ı import eder.

    Validator da runtime type check için MockEvaluationProfile tipine ihtiyaç
    duyar.

    Module-level karşılıklı import circular import oluşturabileceği için:

        if TYPE_CHECKING:
            ...

    sadece static type checker'lar için kullanılır.

    Runtime import ise:
        _validate_model_type içinde local import olarak yapılır.

    Bu yaklaşım:
        - circular import riskini azaltır
        - type hint desteğini korur
        - runtime dependency loading'i kontrollü hale getirir

    ----------------------------------------------------------------------
    BU VALIDATOR NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu validator:

        ✘ evaluation yapmaz
        ✘ score hesaplamaz
        ✘ feedback üretmez
        ✘ LLM çağrısı yapmaz
        ✘ test senaryosu seçmez
        ✘ persistence işlemi yapmaz

    Sadece:
        MockEvaluationProfile invariant safety sağlar.
    """

    @classmethod
    def validate(
        cls,
        profile: "MockEvaluationProfile",
    ) -> None:
        """
        MockEvaluationProfile nesnesini metadata kurallarına göre validate eder.

        Bu method validator'ın public entry point'idir.

        Validation akışı:

            1. model type validation
            2. field-level metadata validation

        şeklindedir.

        Args:
            profile:
                Validate edilecek MockEvaluationProfile domain modelidir.

        Raises:
            TypeError:
                profile MockEvaluationProfile değilse
                veya herhangi bir field expected type'a uymuyorsa.

            ValueError:
                finite, non_empty, min_value veya max_value constraint
                ihlal edilirse.

        Not:
            Validation başarılıysa method herhangi bir değer döndürmez.
        """

        cls._validate_model_type(profile)

        for model_field in fields(profile):

            field_name = model_field.name

            value = getattr(
                profile,
                field_name,
            )

            metadata = model_field.metadata

            # --------------------------------------------------------------
            # NULLABLE HANDLING
            # --------------------------------------------------------------
            #
            # nullable=True olan field'larda None geçerli kabul edilir.
            #
            # Eğer value None ise:
            #   diğer validation kuralları uygulanmaz.
            #
            # Eğer value None değilse:
            #   type, finite, non_empty, min/max gibi kurallar çalışır.
            #
            nullable = metadata.get(
                "nullable",
                False,
            )

            if value is None and nullable:
                continue

            cls._validate_expected_type(
                field_name=field_name,
                value=value,
                expected_type=metadata.get("type"),
            )

            if metadata.get("finite", False):
                cls._validate_finite(
                    field_name=field_name,
                    value=value,
                )

            if metadata.get("non_empty", False):
                cls._validate_non_empty(
                    field_name=field_name,
                    value=value,
                )

            if "min_value" in metadata:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=metadata["min_value"],
                )

            if "max_value" in metadata:
                cls._validate_max_value(
                    field_name=field_name,
                    value=value,
                    max_value=metadata["max_value"],
                )

    @staticmethod
    def _validate_model_type(
        profile: "MockEvaluationProfile",
    ) -> None:
        """
        Runtime'da doğru domain model tipinin gönderildiğini doğrular.

        Bu kontrol field-level validation başlamadan önce yapılır.

        Bunun nedeni:
            fields(profile) çağrısının yanlış tipteki nesnelerde
            daha belirsiz hata üretmesidir.

        Local import kullanılmasının nedeni:
            MockEvaluationProfile ile validator arasındaki circular import
            riskini azaltmaktır.
        """

        from src.domain.evaluation.mock_evaluation_profile import (
            MockEvaluationProfile,
        )

        if not isinstance(profile, MockEvaluationProfile):
            raise TypeError(
                "profile must be MockEvaluationProfile."
            )

    @staticmethod
    def _validate_expected_type(
        *,
        field_name: str,
        value: object,
        expected_type: Any,
    ) -> None:
        """
        Field value'nun metadata'da belirtilen expected type ile uyumlu
        olup olmadığını validate eder.

        expected_type:
            Field metadata'sından okunan runtime type contract'ıdır.

        Örnek expected_type değerleri:
            - str
            - list
            - int
            - float
            - (int, float)

        expected_type None ise:
            o field için type validation tanımlanmamış kabul edilir.

        ------------------------------------------------------------------
        BOOL REJECTION
        ------------------------------------------------------------------

        Python'da bool tipi int'in subclass'ıdır.

        Bu yüzden:

            isinstance(True, int)

        sonucu True döner.

        Ancak domain açısından:
            bool değerler numeric score veya confidence olarak kabul edilmez.

        Bu nedenle bool explicit olarak reddedilir.

        Not:
            Eğer ileride gerçekten bool field eklenirse,
            bu davranış için ayrı bir metadata kuralı tanımlamak daha sağlıklı
            olur.
        """

        if expected_type is None:
            return

        if isinstance(value, bool):
            raise TypeError(
                f"{field_name} cannot be bool."
            )

        if not isinstance(value, expected_type):
            raise TypeError(
                f"{field_name} must be {expected_type}."
            )

    @staticmethod
    def _validate_finite(
        *,
        field_name: str,
        value: float,
    ) -> None:
        """
        Numeric value'nun finite olup olmadığını validate eder.

        Bu method yalnızca metadata'sında:

            finite=True

        bulunan field'lar için çalışır.

        Reddedilen değerler:

            - math.nan
            - math.inf
            - -math.inf

        Bu değerler evaluation pipeline için risklidir.

        Çünkü:
            - analytics verisini bozabilir
            - JSON serialization problemleri oluşturabilir
            - scoring consistency'yi zayıflatabilir
            - test sonuçlarını nondeterministic hale getirebilir
        """

        if not math.isfinite(value):
            raise ValueError(
                f"{field_name} must be finite."
            )

    @staticmethod
    def _validate_non_empty(
        *,
        field_name: str,
        value: str,
    ) -> None:
        """
        String value'nun boş veya whitespace-only olmadığını validate eder.

        Bu method metadata'sında:

            non_empty=True

        bulunan string field'lar için çalışır.

        Örnek invalid değerler:

            ""
            "   "
            "\\n"
            "\\t"

        strip() kullanılması:
            whitespace-only değerleri de semantic olarak boş kabul eder.

        Bu özellikle:
            - feedback
            - rubric_version

        gibi explainability ve tracking alanları için önemlidir.
        """

        if not value.strip():
            raise ValueError(
                f"{field_name} cannot be empty."
            )

    @staticmethod
    def _validate_min_value(
        *,
        field_name: str,
        value: float,
        min_value: float,
    ) -> None:
        """
        Field value'nun tanımlanan minimum değerden küçük olmadığını
        validate eder.

        Bu method yalnızca field metadata'sında:

            "min_value": ...

        tanımı varsa çalışır.

        Örnek:
            score >= 0.0
            confidence >= 0.0

        Args:
            field_name:
                Validate edilen field adı.

            value:
                Validate edilen numeric value.

            min_value:
                Field için izin verilen minimum değer.

        Raises:
            ValueError:
                value, min_value değerinden küçükse fırlatılır.
        """

        if value < min_value:
            raise ValueError(
                f"{field_name} must be >= {min_value}."
            )

    @staticmethod
    def _validate_max_value(
        *,
        field_name: str,
        value: float,
        max_value: float,
    ) -> None:
        """
        Field value'nun tanımlanan maksimum değeri aşmadığını validate eder.

        Bu method yalnızca field metadata'sında:

            "max_value": ...

        tanımı varsa çalışır.

        Örnek:
            score <= 10.0
            confidence <= 1.0

        Args:
            field_name:
                Validate edilen field adı.

            value:
                Validate edilen numeric value.

            max_value:
                Field için izin verilen maksimum değer.

        Raises:
            ValueError:
                value, max_value değerinden büyükse fırlatılır.
        """

        if value > max_value:
            raise ValueError(
                f"{field_name} must be <= {max_value}."
            )