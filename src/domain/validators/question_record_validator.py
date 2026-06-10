from __future__ import annotations

from typing import Any, Mapping

from src.domain.enums.level import Level


class QuestionRecordValidator:
    """
    JSON, YAML, API payload veya benzeri external kaynaklardan gelen raw
    question record'larını doğrulayan infrastructure-level validator sınıfıdır.

    Bu validator'ın temel amacı, raw veri kaydının Question entity'sine
    dönüştürülebilecek minimum yapısal güvenilirliğe sahip olup olmadığını
    kontrol etmektir.

    Önemli mimari karar:
        Bu validator domain entity validation yapmaz.

        Yani:
            - business rule validation
            - semantic validation
            - domain invariant kontrolü

        burada yapılmaz.

    Bu validator yalnızca:
        raw record structure validation

    yapar.

    Neden gerekli?
        External veri kaynakları çoğu zaman güvenilir değildir.

        Örneğin:
            - eksik field
            - yanlış type
            - malformed payload
            - bozuk JSON
            - invalid primitive değerler

        içerebilir.

    Örnek invalid kayıt:
        {
            "id": 123,
            "difficulty": "hard"
        }

        Bu veri doğrudan Question entity oluşturulurken kullanılırsa:
            - runtime exception oluşabilir
            - parsing pipeline kırılabilir
            - repository yükleme işlemi durabilir

    QuestionRecordValidator bu problemleri erken aşamada yakalar.

    Validation pipeline ayrımı:
        Bu projede validation bilinçli olarak katmanlara ayrılmıştır.

    1. Raw record validation:
        QuestionRecordValidator

        Amaç:
            external payload temel olarak geçerli mi?

    2. Domain parsing:
        QuestionFieldParser

        Amaç:
            raw value -> domain-safe value conversion

    3. Domain validation:
        QuestionValidator

        Amaç:
            business/domain rule checking

    Bu ayrım neden önemli?
        Çünkü:
            structural validation
                ile
            domain validation

        aynı sorumluluk değildir.

    Örnek:
        {
            "difficulty": "3"
        }

        structurally:
            yanlış type olabilir

        domain açısından:
            belki parse edilebilir olabilir

    Bu nedenle validation pipeline katmanlı tasarlanmıştır.

    Bu validator ne yapar?
        - record dict mi kontrol eder
        - required field kontrolü yapar
        - primitive type kontrolü yapar
        - malformed payload'ları erken yakalar

    Bu validator ne yapmaz?
        - Question entity oluşturmaz
        - parsing yapmaz
        - enum normalization yapmaz
        - business rule validation yapmaz
        - scoring logic çalıştırmaz

    Bu validator neden infrastructure tarafına daha yakın?
        Çünkü external/raw payload ile çalışır.

        Domain entity ile değil,
        henüz parse edilmemiş ham veriyle ilgilenir.

    Fail-fast yaklaşımı:
        İlk invalid alan bulunduğunda exception fırlatılır.

        Böylece:
            - bozuk dataset erken yakalanır
            - debugging kolaylaşır
            - corrupted repository yüklenmez

    index parametresi neden var?
        Çünkü JSON question bank gibi büyük veri setlerinde:
            hangi kaydın bozuk olduğunu

        hızlı bulmak gerekir.

    Örnek hata:
        Question item at index 42 is missing required fields: ['id']

    Bu yaklaşım debugging açısından çok değerlidir.

    Bu validator özellikle:
        - JSON repository loading
        - seed script validation
        - import pipeline safety
        - dataset integrity checking

    açısından önemlidir.
    """

    REQUIRED_FIELDS = frozenset(
        {
            "id",
            "text",
            "category",
            "level",
            "difficulty",
            "question_type",
        }
    )
    """
    Raw question record içinde bulunması zorunlu alanları temsil eder.

    Bu alanlar olmadan bir Question entity oluşturulamaz.

    Neden merkezi constant olarak tutuluyor?
        Çünkü:
            - required field listesi tek yerde yönetilir
            - maintainability artar
            - duplication önlenir
            - test yazımı kolaylaşır

    Bu alanlar Question entity'nin minimum creation contract'ını temsil eder.
    """

    FIELD_TYPES = {
        "id": str,
        "text": str,
        "category": str,
        "question_type": str,
    }
    """
    Raw question record içindeki primitive field'ların beklenen tiplerini tanımlar.

    Bu mapping, her field'ın hangi primitive type'ta olması gerektiğini belirtir.

    Neden bu mapping kullanılıyor?
        - type validation tek bir yerden yönetilir
        - maintainability artar
        - yeni field eklemek kolaylaşır
        - validation logic merkezi hale gelir

    Bu mapping, _validate_field_types metodunda kullanılarak her field'ın type'ını doğrulamak için referans alınır.
    """

    @classmethod
    def validate(
        cls,
        item: Mapping[str, Any],
        index: int,
    ) -> None:
        """
        Raw question record üzerinde tüm validation kurallarını çalıştıran
        ana orchestration metodudur.

        Bu metod validator'ın public entry-point'idir.

        Validation akışı:
            1. record gerçekten dict mi?
            2. required field'lar mevcut mu?
            3. primitive field type'ları doğru mu?

        Bu metod neden önemli?
            Çünkü malformed external payload'ların:
                domain layer'a ulaşmasını

            engeller.

        Örnek kullanım:
            for index, item in enumerate(records):
                QuestionRecordValidator.validate(item, index)

        Args:
            item:
                Doğrulanacak raw question record'u.

            index:
                Dataset içindeki kayıt index'i.

                Hata mesajlarında debugging amacıyla kullanılır.

        Raises:
            ValueError:
                Record validation başarısız olursa fırlatılır.
        """

        cls._validate_record_type(
            item=item,
            index=index,
        )

        cls._validate_required_fields(
            item=item,
            index=index,
        )

        cls._validate_string_field_types(
            item=item,
            index=index,
        )

        cls._validate_level_type(
            item=item,
            index=index,
        )

        cls._validate_difficulty_type(
            item=item,
            index=index,
        )


    @staticmethod
    def _validate_record_type(
        item: object,
        index: int,
    ) -> None:
        """
        Raw question record'un dict tipinde olup olmadığını doğrular.

        Neden gerekli?
            Çünkü external dataset içinde:
                - string
                - list
                - int
                - malformed object

            bulunabilir.

        Question record temel olarak key-value yapı taşımalıdır.

        Bu nedenle dict zorunludur.

        Geçersiz örnek:
            [
                "hello",
                123,
                []
            ]

        Args:
            item:
                Doğrulanacak raw record.

            index:
                Dataset index değeri.

        Raises:
            ValueError:
                item dict değilse fırlatılır.
        """

        if not isinstance(item, Mapping):
            raise TypeError(
                f"Question item at index {index} must be a mapping."
            )


    @classmethod
    def _validate_required_fields(
        cls,
        item: Mapping[str, Any],
        index: int,
    ) -> None:
        """
        Raw question record içinde zorunlu alanların mevcut olup olmadığını
        doğrular.

        Validation yaklaşımı:
            REQUIRED_FIELDS
                -
            mevcut item key'leri

        ile eksik alanlar hesaplanır.

        Örnek:
            item = {
                "id": "q1",
                "text": "..."
            }

        eksik field:
            [
                "category",
                "level",
                ...
            ]

        Bu validation neden önemli?
            Çünkü eksik alanlar:
                - entity creation failure
                - parsing error
                - inconsistent dataset

            oluşturabilir.

        Args:
            item:
                Doğrulanacak raw record.

            index:
                Dataset index değeri.

        Raises:
            ValueError:
                Required field eksikse fırlatılır.
        """

        missing_fields = cls.REQUIRED_FIELDS - set(item.keys())

        if missing_fields:
            raise ValueError(
                f"Question item at index {index} is missing required fields: "
                f"{sorted(missing_fields)}"
            )


    @classmethod
    def _validate_string_field_types(
        cls,
        item: Mapping[str, Any],
        index: int,
    ) -> None:
        """
        String olması gereken primitive alanları doğrular.
        """

        for field_name, expected_type in cls.FIELD_TYPES.items():
            value = item[field_name]

            if not isinstance(value, expected_type):
                raise TypeError(
                    f"Invalid {field_name} type at index {index}. "
                    f"Expected {expected_type.__name__}, "
                    f"got {type(value).__name__}."
                )
                
                
    @staticmethod
    def _validate_level_type(
        item: Mapping[str, Any],
        index: int,
    ) -> None:
        """
        level alanının raw string veya Level enum olduğunu doğrular.
        """

        value = item["level"]

        if not isinstance(value, str | Level):
            raise TypeError(
                f"Invalid level type at index {index}. "
                f"Expected str or Level, got {type(value).__name__}."
            )
            
            
    @staticmethod
    def _validate_difficulty_type(
        item: Mapping[str, Any],
        index: int,
    ) -> None:
        """
        difficulty alanının bool olmayan int olduğunu doğrular.
        """

        value = item["difficulty"]

        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"Invalid difficulty type at index {index}. "
                f"Expected int, got {type(value).__name__}."
            )