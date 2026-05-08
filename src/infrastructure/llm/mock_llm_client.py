from src.domain.config.provider_config import ProviderConfig
from src.interfaces.llm_client import LLMClient


class MockLLMClient(LLMClient):
    """
    Test ve local development için kullanılan sahte LLM client.

    Bu sınıf gerçek bir LLM provider'a bağlanmaz.
    Yani:
        - Groq API
        - OpenAI API
        - Anthropic API
        - Ollama server
        - local inference engine

    gibi external sistemlerle iletişim kurmaz.

    Amaç:
        LLM bağımlılığı olan servislerin gerçek API çağrısı yapılmadan
        test edilebilmesini sağlamaktır.

    Bu client özellikle şu durumlarda kullanılır:
        - unit test yazarken
        - local development sırasında
        - internet bağlantısı olmadan geliştirme yaparken
        - API key olmadan sistemi çalıştırırken
        - CI/CD pipeline testlerinde
        - deterministic output gereken senaryolarda
        - hızlı demo akışlarında

    Neden MockLLMClient gerekli?
        Gerçek LLM provider kullanıldığında:
            - API maliyeti oluşur
            - response süresi uzayabilir
            - network bağımlılığı oluşur
            - rate limit problemleri yaşanabilir
            - nondeterministic output üretilebilir
            - testler flaky hale gelebilir

        MockLLMClient bu problemlerin tamamını ortadan kaldırır.

    Bu sayede:
        - Service layer güvenli şekilde test edilir.
        - Prompt pipeline doğrulanabilir.
        - Evaluation flow çalıştırılabilir.
        - LLM entegrasyonu olmadan sistem ayağa kaldırılabilir.
        - CLI/UI hızlı şekilde demo yapılabilir.

    Mimari konum:
        Interface:
            LLMClient

        Concrete test implementation:
            MockLLMClient

        Kullanıldığı yerler:
            - Evaluator testleri
            - Prompt service testleri
            - Interview pipeline integration testleri
            - Local CLI demo akışı

    Tasarım notu:
        MockLLMClient gerçek provider davranışını birebir taklit etmeye
        çalışmaz.

        Bunun yerine:
            - stabil
            - hızlı
            - deterministic
            - predictable

        davranış sunmayı hedefler.

    Deterministic output neden önemli?
        Çünkü testlerde aynı input için her zaman aynı output alınmalıdır.

        Bu sayede:
            - assertion yazmak kolaylaşır
            - flaky testler azalır
            - CI pipeline daha güvenilir çalışır

    Önemli:
        Bu sınıf production kullanım için tasarlanmamıştır.

        Gerçek semantic generation, reasoning veya evaluation yeteneği yoktur.

    İleride eklenebilecek gelişmiş mock varyasyonları:
        - ConfigurableMockLLMClient
        - DelayedMockLLMClient
        - ErrorSimulationMockLLMClient
        - ScenarioBasedMockLLMClient
        - StreamingMockLLMClient

    Örnek kullanım:
        llm_client = MockLLMClient()

        response = llm_client.generate(
            prompt="Explain how RAG works."
        )

        print(response)

    Beklenen çıktı:
        "Mock LLM response."
    """

    def __init__(
        self,
        config: ProviderConfig | None = None,
    ) -> None:
        self.config = config or ProviderConfig(
            provider_name="mock",
            model_name="mock-llm",
            temperature=0.0,
            max_tokens=128,
            timeout_seconds=5,
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> str:
        """
        Deterministic mock text response üretir.

        Bu method gerçek bir LLM inference işlemi yapmaz.
        Bunun yerine sabit ve tahmin edilebilir bir string döndürür.

        Args:
            prompt:
                LLM'e gönderilecek ana kullanıcı prompt'udur.

                Boş olmamalıdır.

                Gerçek provider implementasyonlarında bu değer:
                    - chat completion
                    - prompt template
                    - evaluation request
                    - summarization request
                    - question generation

                gibi işlemler için kullanılabilir.

            system_prompt:
                Model davranışını yönlendiren opsiyonel sistem prompt'udur.

                Mock implementation içerisinde aktif kullanılmaz.
                Ancak interface contract'ına uyum sağlamak için parametre
                korunur.

                Gerçek örnek:
                    "You are a strict technical interviewer."

            temperature:
                Generation randomness seviyesini temsil eder.

                Mock implementation deterministic çalıştığı için bu parametre
                sonucu değiştirmez.

                Ancak gerçek provider implementasyonlarıyla aynı method
                signature'ını korumak için burada bulunur.

            max_tokens:
                Maksimum output token limiti.

                Mock implementation içinde aktif kullanılmaz.

                Ancak gerçek provider implementasyonlarıyla contract uyumu
                için parametre korunur.

        Returns:
            str:
                Sabit mock response döndürür.

                Varsayılan çıktı:
                    "Mock LLM response."

                Bu response:
                    - deterministic
                    - hızlı
                    - test dostu

                olacak şekilde bilinçli olarak sabit tutulmuştur.

        Raises:
            ValueError:
                prompt boş veya yalnızca whitespace karakterlerinden oluşuyorsa
                fırlatılır.

        Design Note:
            Bu methodun amacı semantic kalite üretmek değil,
            LLM bağımlı sistemlerin çalıştığını doğrulamaktır.

            Örneğin:
                - service orchestration
                - dependency injection
                - pipeline akışı
                - exception handling
                - response parsing

            gibi sistem davranışları bu mock client ile güvenli şekilde
            test edilebilir.

        Example:
            client = MockLLMClient()

            result = client.generate(
                prompt="Explain vector databases."
            )

            print(result)

        Output:
            "Mock LLM response."
        """

        # ---------------------------------------------------------
        # PROMPT VALIDATION
        # ---------------------------------------------------------
        # Boş prompt anlamlı bir generation isteği değildir.
        #
        # strip() kullanmamızın nedeni:
        #   "   " gibi sadece whitespace içeren string'leri de
        #   geçersiz kabul etmektir.
        #
        # Gerçek provider implementasyonlarında da benzer validation
        # yapılması beklenir.
        if not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        # ---------------------------------------------------------
        # DETERMINISTIC MOCK RESPONSE
        # ---------------------------------------------------------
        # Sabit response döndürülür.
        #
        # Neden sabit?
        #   - predictable test output sağlamak için
        #   - flaky testleri önlemek için
        #   - hızlı local development için
        #   - gerçek API maliyetinden kaçınmak için
        #
        # Bu response gerçek semantic generation temsil etmez.
        return "Mock LLM response."
