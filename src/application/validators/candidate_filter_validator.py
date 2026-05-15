from src.domain.entities.question import Question
from src.application.policies.filter_policy import (
    FilterPolicy,
)


class CandidateFilterValidator:
    """
    Candidate filtering pipeline'ına giren input değerlerinin
    domain contract'a uygunluğunu validate eden validator sınıfıdır.

    Bu validator'ın temel amacı:
        Candidate filtering sürecine gönderilen strategy listesi,
        question listesi ve asked_question_ids set'inin güvenli,
        tutarlı ve beklenen tiplerde olmasını garanti etmektir.

    Bu sınıf:
        - filtering rule uygulamaz
        - question elemez
        - scoring yapmaz
        - ranking yapmaz
        - selection kararı vermez

    Sadece filtering pipeline başlamadan önce input validation yapar.

    ----------------------------------------------------------------------
    NEDEN AYRI VALIDATOR SINIFI VAR?
    ----------------------------------------------------------------------

    Candidate filtering sürecinde birden fazla input vardır:

        - strategies
        - questions
        - asked_question_ids

    Bu input'ların her biri farklı domain contract'a sahiptir.

    Eğer validation logic doğrudan CandidateFilter veya orchestration
    sınıfının içine yazılırsa:

        - filtering orchestration büyür
        - SRP ihlal edilir
        - validation logic tekrar edebilir
        - test yazmak zorlaşır
        - error handling dağınık hale gelir

    Bu nedenle validation ayrı bir sınıfa alınır.

    Böylece:
        - validation merkezi hale gelir
        - CandidateFilter sade kalır
        - reusable validation yapısı oluşur
        - unit test yazmak kolaylaşır
        - domain input contract'ları netleşir

    ----------------------------------------------------------------------
    VALIDATION KAPSAMI
    ----------------------------------------------------------------------

    Bu validator üç temel input grubunu validate eder:

        1. strategies
            Filtering pipeline'da çalıştırılacak FilterStrategy
            implementasyonlarını temsil eder.

        2. questions
            Filtering uygulanacak candidate Question pool'dur.

        3. asked_question_ids
            Daha önce sorulmuş question ID'lerini temsil eden set'tir.

    ----------------------------------------------------------------------
    BU VALIDATOR NEYİ KONTROL ETMEZ?
    ----------------------------------------------------------------------

    Bu validator intentionally minimum input contract validation yapar.

    Şunları kontrol etmez:

        ✘ question listesi boş mu?
        ✘ duplicate question var mı?
        ✘ asked_question_ids içindeki ID'ler gerçekten question pool'da var mı?
        ✘ strategy sıralaması doğru mu?
        ✘ filtering sonrası en az bir question kalacak mı?

    Bu kurallar daha üst seviye business policy veya orchestration
    kararları olabilir.

    Örneğin:
        Bazı senaryolarda empty questions listesi valid olabilir.
        Çünkü retrieval sonucu hiç candidate dönmemiş olabilir.

    Bu nedenle validate_questions method'u boş listeyi reddetmez.

    ----------------------------------------------------------------------
    DEFENSIVE DOMAIN PROGRAMMING
    ----------------------------------------------------------------------

    Python dynamically typed bir dil olduğu için runtime'da yanlış
    input tipleri pipeline'a kolayca girebilir.

    Örneğin:

        strategies = None
        strategies = [object()]
        questions = [{"id": "q1"}]
        asked_question_ids = ["q1", "q2"]

    gibi durumlar mümkündür.

    Bu validator bu invalid input'ları erken aşamada yakalayarak
    daha anlamlı hata mesajları üretir.

    ----------------------------------------------------------------------
    DESIGN PRINCIPLES
    ----------------------------------------------------------------------

    Bu sınıf şu prensipleri destekler:

        - SRP
        - fail-fast validation
        - explicit domain contracts
        - reusable validation logic
        - clean orchestration layer
    """

    @staticmethod
    def validate_policies(
        policies: list[FilterPolicy],
    ) -> None:
        """
        Filtering pipeline'da kullanılacak policy collection'ını validate eder.

        Bu method:
            CandidateFilter'a gönderilen policy listesinin
            gerçekten çalıştırılabilir FilterPolicy instance'larından
            oluştuğunu garanti eder.

        ------------------------------------------------------------------
        VALIDATION KURALLARI
        ------------------------------------------------------------------

        1. policies list olmalıdır.
        2. policies boş olmamalıdır.
        3. Her item FilterPolicy instance'ı olmalıdır.

        ------------------------------------------------------------------
        NEDEN POLICIES BOŞ OLAMAZ?
        ------------------------------------------------------------------

        CandidateFilter'ın temel görevi:
            bir veya daha fazla filtering policy'yi sırayla uygulamaktır.

        Policy listesi boşsa:
            filtering pipeline semantic olarak anlamsız hale gelir.

        Eğer hiç filtering yapılmayacaksa:
            CandidateFilter kullanılmamalı veya ayrı bir NoOpFilterPolicy
            tanımlanmalıdır.

        ------------------------------------------------------------------
        NEDEN FilterPolicy INSTANCE KONTROLÜ VAR?
        ------------------------------------------------------------------

        Filtering pipeline polymorphic çalışır.

        Orchestration katmanı concrete policy class'ını bilmez.
        Sadece FilterPolicy contract'ına güvenir.

        Bu yüzden listedeki her elemanın:
            FilterPolicy abstraction'ını implemente etmesi gerekir.

        Raises:
            TypeError:
                policies list değilse veya item'lar FilterPolicy değilse.

            ValueError:
                policies boşsa.
        """

        if not isinstance(policies, list):
            raise TypeError(
                "policies must be a list."
            )

        if not policies:
            raise ValueError(
                "policies cannot be empty."
            )

        for policy in policies:
            if not isinstance(policy, FilterPolicy):
                raise TypeError(
                    "All policies must be FilterPolicy instances."
                )


    @staticmethod
    def validate_questions(
        questions: list[Question],
    ) -> None:
        """
        Filtering uygulanacak candidate question listesini validate eder.

        Bu method:
            questions parametresinin gerçekten list olduğunu ve listedeki
            tüm item'ların Question domain entity'si olduğunu garanti eder.

        ------------------------------------------------------------------
        VALIDATION KURALLARI
        ------------------------------------------------------------------

        1. questions list olmalıdır.
        2. Listedeki her item Question instance'ı olmalıdır.

        ------------------------------------------------------------------
        NEDEN BOŞ LİSTE REDDEDİLMİYOR?
        ------------------------------------------------------------------

        Filtering pipeline açısından boş question listesi bazı senaryolarda
        geçerli olabilir.

        Örneğin:
            - retrieval sonucu hiç question dönmemiş olabilir
            - önceki filter'lar tüm candidate'ları elemiş olabilir
            - test senaryosunda empty pool davranışı kontrol ediliyor olabilir

        Bu yüzden validate_questions method'u empty list'i invalid saymaz.

        Eğer business requirement olarak:
            "selection aşamasına mutlaka en az bir question gitmeli"

        gibi bir kural varsa, bu validation CandidateFilterValidator'dan
        ziyade selection/ranking pipeline katmanında uygulanmalıdır.

        Raises:
            TypeError:
                questions list değilse veya listedeki item'lar Question değilse.
        """

        if not isinstance(questions, list):
            raise TypeError(
                "questions must be a list."
            )

        for question in questions:
            if not isinstance(question, Question):
                raise TypeError(
                    "All questions must be Question instances."
                )


    @staticmethod
    def validate_asked_question_ids(
        asked_question_ids: set[str],
    ) -> None:
        """
        Daha önce sorulmuş question ID set'ini validate eder.

        Bu method:
            asked_question_ids değerinin set olduğunu ve içerisindeki tüm
            elemanların string question ID olduğunu garanti eder.

        ------------------------------------------------------------------
        VALIDATION KURALLARI
        ------------------------------------------------------------------

        1. asked_question_ids set olmalıdır.
        2. Set içindeki her item str olmalıdır.

        ------------------------------------------------------------------
        NEDEN SET KULLANILIYOR?
        ------------------------------------------------------------------

        asked_question_ids lookup için kullanılır.

        Örneğin:

            if question.id in asked_question_ids

        gibi membership check işlemleri yapılır.

        set veri yapısı bu senaryo için uygundur çünkü:
            - average O(1) lookup sağlar
            - duplicate ID tutmaz
            - membership intent'ini açık ifade eder

        Liste kullanılsaydı:
            - lookup O(n) olurdu
            - duplicate değerler mümkün olurdu
            - semantic intent daha zayıf kalırdı

        ------------------------------------------------------------------
        NEDEN STRING ID ZORUNLU?
        ------------------------------------------------------------------

        Question.id alanı domain içerisinde string olarak kabul edilir.

        Bu nedenle asked_question_ids içindeki değerlerin de string olması
        gerekir.

        Eğer int veya başka tipler kabul edilirse:
            lookup işlemi sessizce yanlış sonuç verebilir.

        Örneğin:

            question.id == "123"
            asked_question_ids == {123}

        Bu durumda ID mantıken aynı gibi görünse bile Python açısından
        eşleşmez.

        Bu validator bu tür subtle bug'ları engeller.

        Raises:
            TypeError:
                asked_question_ids set değilse veya içindeki item'lar str değilse.
        """

        if not isinstance(asked_question_ids, set):
            raise TypeError(
                "asked_question_ids must be a set."
            )

        for question_id in asked_question_ids:
            if not isinstance(question_id, str):
                raise TypeError(
                    "All asked question IDs must be strings."
                )