import math
from dataclasses import fields
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.domain.selection.scored_candidate import ScoredCandidate


class ScoredCandidateValidator:
    """
    ScoredCandidate domain snapshot modelinin metadata-driven invariant
    validation kurallarını yöneten validator sınıfıdır.

    Bu validator'ın temel amacı:
        Scoring aşamasından geçmiş fakat henüz ranking aşamasına girmemiş
        ScoredCandidate nesnesinin güvenli, tutarlı ve domain kurallarına
        uygun state taşımasını garanti etmektir.

    ----------------------------------------------------------------------
    SCORED CANDIDATE NEDİR?
    ----------------------------------------------------------------------

    ScoredCandidate:
        Ranking öncesi candidate state'idir.

    Bu model:
        - question bilgisini taşır
        - final score bilgisini taşır
        - explainable scoring breakdown bilgisini taşır

    Ancak:
        - rank taşımaz
        - sorting sonucu temsil etmez
        - final selection kararını temsil etmez

    Bu nedenle ScoredCandidate validation kuralları:
        score güvenliği ve field type consistency üzerine odaklanır.

    ----------------------------------------------------------------------
    METADATA-DRIVEN VALIDATION
    ----------------------------------------------------------------------

    Bu validator field isimlerini hard-code etmek yerine
    dataclass field metadata bilgisini okur.

    Örneğin ScoredCandidate içinde:

        score: float = field(
            metadata={
                "type": (int, float),
                "finite": True,
                "min_value": MIN_SELECTION_SCORE,
            }
        )

    gibi bir tanım varsa, validator runtime'da bu metadata'yı okuyarak
    ilgili validation kurallarını uygular.

    Bu yaklaşımın avantajları:

        - validator generic hale gelir
        - model self-documenting olur
        - validation behavior field declaration üzerinde görünür
        - yeni field eklemek kolaylaşır
        - Open/Closed Principle desteklenir

    ----------------------------------------------------------------------
    VALIDATION KAPSAMI
    ----------------------------------------------------------------------

    Bu validator şu kontrolleri yapar:

        1. Model type validation
            Validate edilen nesnenin gerçekten ScoredCandidate olup
            olmadığını kontrol eder.

        2. Runtime type validation
            Field metadata'sında belirtilen expected type'a göre
            value doğrulanır.

        3. Bool rejection
            Python'da bool int subclass'ı olduğu için numeric field'larda
            yanlışlıkla kabul edilmesini engeller.

        4. Finite validation
            NaN, infinity ve -infinity değerlerini reddeder.

        5. Minimum value validation
            score gibi alanların minimum boundary altında kalmasını engeller.

    ----------------------------------------------------------------------
    BU VALIDATOR NE YAPMAZ?
    ----------------------------------------------------------------------

    Bu validator:

        ✘ scoring hesaplamaz
        ✘ ranking yapmaz
        ✘ sorting yapmaz
        ✘ selection kararı vermez
        ✘ persistence işlemi yapmaz
        ✘ breakdown üretmez

    Sadece:
        ScoredCandidate invariant safety sağlar.

    ----------------------------------------------------------------------
    TYPE_CHECKING VE LAZY IMPORT
    ----------------------------------------------------------------------

    ScoredCandidate modeli __post_init__ içinde bu validator'ı import eder.

    Validator da runtime type check için ScoredCandidate tipine ihtiyaç duyar.

    Module-level karşılıklı import circular import oluşturabileceği için:

        if TYPE_CHECKING:
            ...

    sadece static type checker için kullanılır.

    Runtime import ise:
        _validate_model_type içinde local import olarak yapılır.

    Bu yaklaşım:
        - circular import riskini azaltır
        - type hint desteğini korur
        - runtime dependency loading'i kontrollü hale getirir

    ----------------------------------------------------------------------
    DOMAIN SAFETY
    ----------------------------------------------------------------------

    Bu validator şu invalid state'leri engeller:

        - score = math.nan
        - score = math.inf
        - score = -1
        - score = True
        - question = dict
        - breakdown = None

    Böylece ranking aşamasına yalnızca güvenli ScoredCandidate
    snapshot'ları geçebilir.
    """

    @classmethod
    def validate(
        cls,
        candidate: "ScoredCandidate",
    ) -> None:
        """
        ScoredCandidate nesnesini metadata kurallarına göre validate eder.

        Bu method validator'ın public entry point'idir.

        Validation akışı:

            1. model type validation
            2. field-level metadata validation

        şeklindedir.

        Args:
            candidate:
                Validate edilecek ScoredCandidate domain snapshot nesnesi.

        Raises:
            TypeError:
                candidate ScoredCandidate değilse
                veya herhangi bir field expected type'a uymuyorsa.

            ValueError:
                finite veya minimum value constraint ihlal edilirse.

        Not:
            Validation başarılıysa method herhangi bir değer döndürmez.
        """

        cls._validate_model_type(candidate)

        for model_field in fields(candidate):
            field_name = model_field.name
            value = getattr(candidate, field_name)
            metadata = model_field.metadata

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

            if "min_value" in metadata:
                cls._validate_min_value(
                    field_name=field_name,
                    value=value,
                    min_value=metadata["min_value"],
                )

    @staticmethod
    def _validate_model_type(
        candidate: "ScoredCandidate",
    ) -> None:
        """
        Runtime'da doğru domain model tipinin gönderildiğini doğrular.

        Bu kontrol field-level validation başlamadan önce yapılır.

        Bunun nedeni:
            fields(candidate) çağrısının yanlış tipteki nesnelerde
            daha düşük seviyeli ve daha belirsiz hata üretmesidir.

        Local import kullanılmasının nedeni:
            ScoredCandidate ile ScoredCandidateValidator arasındaki
            circular import riskini azaltmaktır.
        """

        from src.domain.selection.scored_candidate import ScoredCandidate

        if not isinstance(candidate, ScoredCandidate):
            raise TypeError(
                "candidate must be a ScoredCandidate instance."
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
            - Question
            - SelectionBreakdown
            - int
            - float
            - (int, float)

        expected_type None ise:
            o field için type validation tanımlanmamış kabul edilir.

        ------------------------------------------------------------------
        BOOL NEDEN REDDEDİLİYOR?
        ------------------------------------------------------------------

        Python'da bool tipi int'in subclass'ıdır.

        Bu nedenle:

            isinstance(True, int)

        sonucu True döner.

        Ancak domain açısından:

            score=True

        geçerli bir numeric score değildir.

        Bu yüzden bool explicit olarak reddedilir.

        Not:
            Bu kontrol tüm field'lar için uygulanır.
            Eğer ileride gerçekten bool field eklenecekse,
            bool kabul eden ayrı metadata kuralı tanımlanmalıdır.
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

        Bu method sadece metadata'sında:

            finite=True

        bulunan alanlar için çalışır.

        Reddedilen değerler:

            - math.nan
            - math.inf
            - -math.inf

        Bu değerler ranking/scoring pipeline için risklidir.

        Çünkü:
            - sorting behavior'ı bozabilir
            - comparison sonuçlarını anlamsız hale getirebilir
            - JSON serialization problemleri çıkarabilir
            - analytics/reporting verisini kirletebilir
            - explainability çıktısını bozabilir
        """

        if not math.isfinite(value):
            raise ValueError(
                f"{field_name} must be finite."
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

        Bu method sadece field metadata'sında:

            "min_value": ...

        tanımı varsa çalışır.

        Örneğin ScoredCandidate.score için:

            min_value = MIN_SELECTION_SCORE

        olabilir.

        Bu kural:
            selection score'un negatif olmasını engeller.

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