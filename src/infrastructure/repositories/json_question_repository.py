from __future__ import annotations

import json
from pathlib import Path

from src.domain.entities.question import Question
from src.domain.repositories.question_repository import QuestionRepository
from src.infrastructure.mappers.question_mapper import QuestionMapper
from src.domain.validators.question_record_validator import (
    QuestionRecordValidator,
)


class JsonQuestionRepository(QuestionRepository):
    """
    JSON tabanlı QuestionRepository implementasyonudur.

    Bu sınıfın temel amacı, JSON dosyasında tutulan question bank verisini
    okuyup domain-safe Question entity listesine dönüştürmektir.

    Mimari rolü:
        JsonQuestionRepository bir infrastructure adapter'dır.

        Domain/application katmanı QuestionRepository abstraction'ına
        bağımlıdır.

        Bu concrete sınıf ise:
            - JSON dosyası okur
            - raw kayıtları doğrular
            - raw kayıtları Question entity'sine map eder
            - repository contract'ını uygular

    Bu yapı Clean Architecture / Hexagonal Architecture açısından önemlidir.

    Çünkü application layer:
        - JSON dosyasının path'ini
        - dosya okuma detaylarını
        - json.load kullanımını
        - raw dict formatını

    bilmek zorunda kalmaz.

    Application layer yalnızca şunu bilir:
        QuestionRepository üzerinden Question entity'leri alınabilir.

    Bu sınıfın sorumlulukları:
        - JSON question bank dosyasını okumak
        - JSON root yapısını doğrulamak
        - her raw question record'unu validator'a göndermek
        - her raw record'u mapper ile Question entity'sine çevirmek
        - duplicate question id kontrolü yapmak
        - list_all contract'ını sağlamak
        - get_by_id contract'ını sağlamak

    Bu sınıfın sorumluluğu değildir:
        - Question domain validation yapmak
        - enum parsing yapmak
        - scoring yapmak
        - question selection yapmak
        - evaluator çalıştırmak
        - vector store indexing yapmak
        - API response üretmek

    Validation pipeline:
        JSON file
            ↓
        _load_raw_items()
            ↓
        QuestionRecordValidator
            ↓
        QuestionMapper
            ↓
        Question entity
            ↓
        QuestionFieldParser + QuestionValidator

    Bu pipeline neden önemli?
        Çünkü:
            - raw structure validation
            - mapping
            - domain parsing
            - domain validation

        farklı sorumluluklardır.

    Duplicate id kontrolü neden repository'de?
        Çünkü duplicate id kontrolü tek bir Question entity üzerinden yapılamaz.

        Bunun için tüm question collection'ını görmek gerekir.

        Bu nedenle duplicate kontrolü collection-level responsibility olarak
        repository loading sürecinde yapılır.

    Bu implementation ne zaman yeterli?
        - MVP
        - local development
        - static question bank
        - seed data
        - offline test
        - CLI demo

    İleride aynı QuestionRepository contract'ı korunarak:
        - SqlQuestionRepository
        - MongoQuestionRepository
        - ApiQuestionRepository
        - CachedQuestionRepository

    gibi farklı implementasyonlar eklenebilir.
    """

    def __init__(
        self,
        file_path: str | Path,
    ) -> None:
        """
        JsonQuestionRepository instance'ını oluşturur.

        Args:
            file_path:
                Question bank JSON dosyasının path'i.

                str veya Path kabul edilir.

        Neden Path'e çevriliyor?
            Çünkü pathlib.Path:
                - platform bağımsız path yönetimi sağlar
                - okunabilir dosya işlemleri sunar
                - exists/open gibi methodlarla çalışmayı kolaylaştırır

        Örnek:
            repository = JsonQuestionRepository(
                file_path="data/questions.json",
            )
        """
        self.file_path = Path(file_path)

    def list_all(self) -> list[Question]:
        """
        JSON question bank içindeki tüm kayıtları Question entity listesine
        dönüştürerek döndürür.

        Bu metod QuestionRepository contract'ını uygular.

        Akış:
            1. JSON dosyasından raw item listesi okunur.
            2. Her raw item QuestionRecordValidator ile doğrulanır.
            3. Her raw item QuestionMapper ile Question entity'sine çevrilir.
            4. Tüm question id'lerinin unique olduğu kontrol edilir.
            5. Domain-safe Question listesi döndürülür.

        Neden her çağrıda dosya tekrar okunuyor?
            Bu implementation basit ve deterministic MVP yaklaşımıdır.

            Avantaj:
                - cache invalidation problemi yoktur
                - dosya değişiklikleri hemen yansır
                - testlerde davranış nettir

            Dezavantaj:
                - büyük dataset'lerde performans maliyeti olabilir

        İleride gerekirse:
            - lazy cache
            - explicit reload
            - file watcher
            - in-memory index

        eklenebilir.

        Returns:
            list[Question]:
                JSON dosyasından üretilmiş domain-safe Question listesi.

        Raises:
            FileNotFoundError:
                JSON dosyası bulunamazsa fırlatılır.

            ValueError:
                JSON root list değilse, record bozuksa veya duplicate id
                varsa fırlatılır.
        """
        raw_items = self._load_raw_items()

        questions = [
            self._build_question(
                item=item,
                index=index,
            )
            for index, item in enumerate(raw_items)
        ]

        self._validate_unique_ids(questions)

        return questions

    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """
        Verilen question_id değerine sahip Question entity'sini döndürür.

        Bu metod QuestionRepository contract'ını uygular.

        Akış:
            1. question_id validate edilir.
            2. list_all() ile tüm Question entity'leri yüklenir.
            3. id eşleşmesi aranır.
            4. Bulunursa Question döner.
            5. Bulunamazsa None döner.

        Neden None döner?
            Çünkü question bulunamaması normal bir lookup sonucudur.

            Bu durumda exception fırlatmak yerine None dönmek service layer'da
            daha sade kontrol sağlar.

        Not:
            Bu implementation her lookup için list_all() çağırır.

            MVP ve küçük JSON dosyaları için yeterlidir.

            Büyük question bank'lerde performans için:
                - id index cache
                - dictionary lookup
                - preloaded repository

            gibi optimizasyonlar eklenebilir.

        Args:
            question_id:
                Aranacak Question id değeri.

        Returns:
            Question | None:
                Eşleşen Question entity'si.

                Bulunamazsa None.

        Raises:
            ValueError:
                question_id string değilse veya boşsa fırlatılır.
        """
        self._validate_question_id(question_id)

        for question in self.list_all():
            if question.id == question_id:
                return question

        return None

    def exists(self) -> bool:
        """
        Repository'nin bağlı olduğu JSON question bank dosyasının var olup
        olmadığını döndürür.

        Bu helper özellikle:
            - startup health check
            - CLI diagnostics
            - test setup
            - repository readiness control

        için kullanılabilir.

        Returns:
            bool:
                True:
                    dosya mevcut

                False:
                    dosya mevcut değil
        """
        return self.file_path.exists()

    def _load_raw_items(self) -> list[dict]:
        """
        JSON dosyasını okuyarak raw question item listesini döndürür.

        Bu metod file system ve JSON parsing sorumluluğunu izole eder.

        Akış:
            1. Dosyanın var olup olmadığı kontrol edilir.
            2. Dosya UTF-8 encoding ile açılır.
            3. json.load ile parse edilir.
            4. JSON root'un list olup olmadığı kontrol edilir.
            5. Raw item listesi döndürülür.

        JSON root neden list olmalı?
            Çünkü question bank birden fazla question record içerir.

            Beklenen format:
                [
                    {
                        "id": "...",
                        "text": "...",
                        ...
                    }
                ]

        Eğer root dict olursa:
            repository collection mantığı bozulur.

        Returns:
            list[dict]:
                Raw question record listesi.

        Raises:
            FileNotFoundError:
                JSON dosyası bulunamazsa fırlatılır.

            ValueError:
                JSON root list değilse fırlatılır.

            json.JSONDecodeError:
                JSON parse edilemezse fırlatılabilir.
        """
        if not self.exists():
            raise FileNotFoundError(
                f"Question bank file not found: {self.file_path}"
            )

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError("Question bank JSON root must be a list.")

        return data

    def _build_question(
        self,
        item: dict,
        index: int,
    ) -> Question:
        """
        Tek bir raw question record'unu validate edip Question entity'sine
        dönüştürür.

        Bu metod record-level pipeline'ı temsil eder.

        Akış:
            1. Raw record structural validation'dan geçer.
            2. Mapper ile Question entity oluşturulur.
            3. Question entity kendi __post_init__ sürecinde parsing ve domain
               validation çalıştırır.

        Neden validator ve mapper ayrı?
            Çünkü:
                - validator raw record güvenli mi kontrol eder
                - mapper raw record'u domain entity'ye dönüştürür

            Bu iki sorumluluğun ayrılması kodu daha test edilebilir ve
            sürdürülebilir yapar.

        Args:
            item:
                Raw question dictionary.

            index:
                Dataset içindeki kayıt index değeri.

        Returns:
            Question:
                Domain-safe Question entity.

        Raises:
            ValueError:
                Record validation veya mapping başarısız olursa fırlatılır.
        """
        QuestionRecordValidator.validate(
            item=item,
            index=index,
        )

        return QuestionMapper.from_mapping(
            payload=item,
            index=index,
        )

    @staticmethod
    def _validate_question_id(
        question_id: str,
    ) -> None:
        """
        get_by_id için gelen question_id parametresini doğrular.

        Kurallar:
            - string olmalıdır
            - boş string olamaz
            - whitespace-only olamaz

        Neden gerekli?
            Repository lookup işlemlerinde invalid id ile arama yapmak
            anlamsızdır.

            Bu validation erken hata yakalamayı sağlar.

        Args:
            question_id:
                Doğrulanacak Question id değeri.

        Raises:
            ValueError:
                question_id string değilse veya boşsa fırlatılır.
        """
        if not isinstance(question_id, str):
            raise ValueError("question_id must be a string.")

        if not question_id.strip():
            raise ValueError("question_id cannot be empty.")

    @staticmethod
    def _validate_unique_ids(
        questions: list[Question],
    ) -> None:
        """
        Yüklenen Question listesi içinde duplicate id olup olmadığını kontrol
        eder.

        Bu validation collection-level bir validation'dır.

        Neden QuestionValidator içinde değil?
            Çünkü tek bir Question entity kendi id'sinin collection içinde
            unique olup olmadığını bilemez.

            Duplicate id kontrolü tüm question listesine ihtiyaç duyar.

        Duplicate id neden kritik?
            Çünkü duplicate id:
                - get_by_id sonucunu belirsizleştirir
                - asked_question_ids tracking'i bozar
                - vector store metadata eşleşmesini bozar
                - interview history'yi güvenilmez hale getirir
                - analytics sonuçlarını kirletir

        Akış:
            1. seen_ids set'i oluşturulur.
            2. Her question id kontrol edilir.
            3. Daha önce görülen id tekrar gelirse duplicate_ids'e eklenir.
            4. Duplicate varsa ValueError fırlatılır.

        Args:
            questions:
                Kontrol edilecek Question entity listesi.

        Raises:
            ValueError:
                Duplicate question id bulunursa fırlatılır.
        """
        seen_ids: set[str] = set()
        duplicate_ids: set[str] = set()

        for question in questions:
            if question.id in seen_ids:
                duplicate_ids.add(question.id)

            seen_ids.add(question.id)

        if duplicate_ids:
            raise ValueError(
                f"Duplicate question ids found: {sorted(duplicate_ids)}"
            )