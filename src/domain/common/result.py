from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Result(Generic[T]):
    """
    Generic operation result wrapper.

    Bu model:
        operation outcome'larını explicit şekilde temsil etmek için kullanılan
        generic bir domain/application utility modelidir.

    Amaç:
        Exception tabanlı kontrol akışı yerine:
            explicit success/failure flow

        sağlamaktır.

    Geleneksel yaklaşım:
        try:
            result = operation()
        except Exception:
            ...

    Result yaklaşımı:
        result = operation()

        if result.success:
            ...
        else:
            ...

    Neden Result pattern kullanıyoruz?
        Çünkü büyük orchestration sistemlerinde yalnızca exception tabanlı akış:
            - kontrolü zorlaştırır
            - pipeline'ları kırılgan hale getirir
            - nested try/except oluşturur
            - error propagation'ı belirsizleştirir

    Result modeli sayesinde:
        ✔ predictable orchestration
        ✔ explicit failure handling
        ✔ safer pipelines
        ✔ composable workflows
        ✔ retry handling kolaylığı
        ✔ API response mapping
        ✔ test edilebilirlik
        ✔ deterministic flow

    Bu pattern özellikle:
        - pipeline orchestration
        - distributed systems
        - async workflows
        - retry mekanizmaları
        - API katmanları
        - LangGraph/state machine flow'ları

    için çok değerlidir.

    Generic[T] neden kullanılıyor?
        Çünkü Result:
            farklı veri tiplerini taşıyabilmelidir.

    Örnek:
        Result[Question]
        Result[PipelineResult]
        Result[EvaluationResult]
        Result[list[Question]]

    Böylece:
        - type safety korunur
        - IDE autocomplete çalışır
        - yanlış veri erişimi azalır

    Neden frozen=True?
        Çünkü Result immutable operation snapshot'ı temsil eder.

        Bir operation sonucu oluştuktan sonra:
            - success state
            - data
            - error

        değişmemelidir.

        Mutable olması:
            - inconsistent orchestration state
            - debugging zorluğu
            - accidental mutation
            - concurrency problemleri

        oluşturabilir.

    Result pattern avantajları:
        ✔ explicit state
        ✔ safer chaining
        ✔ orchestration readability
        ✔ easier retry systems
        ✔ API-friendly structure

    Dezavantajları:
        ✘ biraz daha verbose olabilir
        ✘ her operation için wrapper gerekir
        ✘ unwrap misuse exception üretebilir

    Bu tradeoff production pipeline'larda genellikle kabul edilir.

    Kullanım örneği:
        result = Result.ok(question)

        if result.success:
            print(result.data)

    Failure örneği:
        result = Result.fail("Question not found.")

        if not result.success:
            print(result.error)

    Gelecekte eklenebilecek özellikler:
        - map()
        - flat_map()
        - bind()
        - recover()
        - retry metadata
        - error codes
        - warning support
        - telemetry metadata
        - partial success support

    Mimari not:
        Bu model:
            operation state representation

        yapar.

        Şunları içermez:
            ✘ retry logic
            ✘ logging
            ✘ exception handling strategy
            ✘ transport mapping

        Çünkü bunlar orchestration veya infrastructure concern'dür.
    """

    # ---------------------------------------------------------
    # SUCCESS FLAG
    # ---------------------------------------------------------
    # Operation'ın başarılı olup olmadığını belirtir.
    #
    # True:
    #   operation başarıyla tamamlandı
    #
    # False:
    #   operation başarısız oldu
    #
    # Bu explicit flag sayesinde:
    #   - predictable branching
    #   - safer orchestration
    #   - exception-free flow
    #
    # sağlanabilir.
    success: bool

    # ---------------------------------------------------------
    # RESULT DATA
    # ---------------------------------------------------------
    # Başarılı operation sonucu üretilen veri.
    #
    # Generic[T] sayesinde:
    #   herhangi bir domain modeli taşınabilir.
    #
    # Örnek:
    #   Question
    #   PipelineResult
    #   EvaluationResult
    #   list[Question]
    #
    # Failure durumda genellikle None olur.
    data: T | None = None

    # ---------------------------------------------------------
    # ERROR MESSAGE
    # ---------------------------------------------------------
    # Operation başarısız olduğunda açıklayıcı hata mesajını içerir.
    #
    # Örnek:
    #   "Question not found."
    #   "Invalid interview state."
    #   "Evaluator timeout."
    #
    # Success durumda genellikle None olur.
    #
    # Bu alan:
    #   - UI feedback
    #   - API response mapping
    #   - telemetry
    #   - debugging
    #
    # için kullanılabilir.
    error: str | None = None

    @classmethod
    def ok(cls, data: T) -> "Result[T]":
        """
        Başarılı Result instance'ı oluşturur.

        Bu helper method:
            success=True

        olan standart success response üretir.

        Args:
            data:
                Başarılı operation sonucu oluşan veri.

        Returns:
            Result[T]:
                success=True olan Result instance'ı.

        Example:
            result = Result.ok(question)

            print(result.success)

        Output:
            True

        Design Note:
            Factory method kullanılması:
                - readability artırır
                - boilerplate azaltır
                - creation consistency sağlar
        """

        # ---------------------------------------------------------
        # SUCCESS RESULT CREATION
        # ---------------------------------------------------------
        # Başarılı operation sonucu oluşturulur.
        #
        # success=True
        # error=None
        #
        # explicit şekilde set edilir.
        return cls(
            success=True,
            data=data,
            error=None,
        )

    @classmethod
    def fail(cls, error: str) -> "Result[T]":
        """
        Başarısız Result instance'ı oluşturur.

        Bu helper method:
            success=False

        olan standart failure response üretir.

        Args:
            error:
                Operation sırasında oluşan hata mesajı.

        Returns:
            Result[T]:
                success=False olan Result instance'ı.

        Example:
            result = Result.fail("Question not found.")

            print(result.success)

        Output:
            False

        Design Note:
            Explicit failure object üretmek:
                - exception dependency azaltır
                - orchestration flow'u sadeleştirir
                - API mapping kolaylaştırır
        """

        # ---------------------------------------------------------
        # FAILURE RESULT CREATION
        # ---------------------------------------------------------
        # Başarısız operation sonucu oluşturulur.
        #
        # success=False
        # data=None
        #
        # explicit şekilde set edilir.
        return cls(
            success=False,
            data=None,
            error=error,
        )

    def unwrap(self) -> T:
        """
        Başarılı sonucu güvenli şekilde döndürür.

        Eğer Result:
            success=True

        ise:
            data döndürülür.

        Eğer Result:
            success=False

        ise:
            exception fırlatılır.

        Returns:
            T:
                Result içerisindeki başarılı data.

        Raises:
            ValueError:
                Result başarısızsa fırlatılır.

        Neden unwrap kullanıyoruz?
            Çünkü bazı durumlarda:
                "Bu operation kesin başarılı olmalı"

            varsayımı vardır.

        Örnek:
            result = repository.get(...)

            question = result.unwrap()

        Bu durumda:
            başarısız state fail-fast davranır.

        Design Note:
            unwrap dikkatli kullanılmalıdır.

            Çünkü:
                explicit Result flow'u
            tekrar
                exception flow'una

            dönüştürür.

            Production orchestration sistemlerinde çoğu zaman:
                if result.success:
                    ...
                else:
                    ...

            yaklaşımı daha güvenlidir.

        Example:
            result = Result.ok(42)

            value = result.unwrap()

            print(value)

        Output:
            42
        """

        # ---------------------------------------------------------
        # FAILURE CHECK
        # ---------------------------------------------------------
        # Result başarısızsa explicit exception fırlatılır.
        #
        # Böylece invalid unwrap engellenir.
        if not self.success:
            raise ValueError(self.error or "Unknown result error.")

        # ---------------------------------------------------------
        # TYPE SAFETY ASSERTION
        # ---------------------------------------------------------
        # success=True durumunda data'nın None olmaması beklenir.
        #
        # Bu assert:
        #   static analysis ve debugging açısından faydalıdır.
        assert self.data is not None

        # ---------------------------------------------------------
        # SUCCESS DATA RETURN
        # ---------------------------------------------------------
        # Güvenli şekilde unwrap edilmiş data döndürülür.
        return self.data
