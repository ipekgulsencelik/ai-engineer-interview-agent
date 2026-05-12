import pytest

from src.application.ports.llm_client import LLMClient
from src.domain.entities.question import Question
from src.application.ports.evaluator import Evaluator
from src.domain.llm.llm_response import LLMResponse
from src.domain.repositories.question_repository import QuestionRepository
from src.domain.retrieval.search_result import SearchResult
from src.domain.retrieval.vector_store import VectorStore
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.scoring.scoring_engine import ScoringEngine


def build_question(**overrides) -> Question:
    """
    Test senaryolarında kullanılmak üzere örnek Question nesnesi üretir.

    Amaç:
        Her test içinde tekrar tekrar aynı Question payload'unu
        yazmayı engellemek.

    Not:
        overrides sayesinde belirli alanlar test bazında değiştirilebilir.

    Örnek:
        build_question(level="MID")
    """

    payload = {
        "id": "q1",
        "text": "What is RAG?",
        "category": "RAG",
        "level": "JR",
        "difficulty": 1,
        "question_type": "conceptual",
        "expected_points": [],
        "keywords": [],
    }

    payload.update(overrides)

    return Question(**payload)


@pytest.mark.parametrize(
    "interface_class",
    [
        Evaluator,
        LLMClient,
        ScoringEngine,
        QuestionRepository,
        VectorStore,
    ],
)
def test_abstract_interfaces_cannot_be_instantiated(
    interface_class: type,
) -> None:
    """
    Abstract interface'lerin doğrudan instantiate
    edilemediğini doğrular.

    Amaç:
        ABC (Abstract Base Class) contract'lerinin
        gerçekten enforced edildiğini garanti etmek.

    Eğer bir interface instantiate edilebiliyorsa:
        - soyut mimari bozulmuş olabilir
        - abstract method eksik tanımlanmış olabilir
        - inheritance contract'i kırılmış olabilir
    """

    with pytest.raises(TypeError):
        interface_class()


class DummyEvaluator(Evaluator):
    """
    Evaluator interface'inin minimal test implementasyonu.

    Amaç:
        Interface contract'inin doğru çalıştığını
        doğrulamak.
    """

    def evaluate(
        self,
        question: Question,
        answer: str,
    ) -> dict:
        """
        Basit mock evaluation sonucu döndürür.
        """

        return {
            "score": 10,
            "feedback": "OK",
        }


class DummyLLMClient(LLMClient):
    """
    LLMClient interface'inin test implementasyonu.

    Gerçek API çağrısı yerine deterministic response döndürür.
    """

    def generate(
        self,
        prompt: str,
        *,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
        stop: list[str] | None = None,
    ) -> LLMResponse:
        """
        Mock LLM response üretir.
        """

        return LLMResponse(
            text="dummy response",
            model_name="dummy-model",
            tokens_used=0,
            latency_seconds=0.0,
        )


class DummyScoringEngine(ScoringEngine):
    """
    ScoringEngine interface'inin minimal implementasyonu.

    Sabit skor döndürerek contract test edilmesini sağlar.
    """

    def score(
        self,
        question: Question,
        context: ScoringContext,
    ) -> float:
        """
        Sabit skor döndürür.
        """

        return 1.0


class DummyQuestionRepository(QuestionRepository):
    """
    QuestionRepository interface'inin test implementasyonu.

    In-memory boş repository gibi davranır.
    """

    def list_all(self) -> list[Question]:
        """
        Tüm soruları döndürür.

        Test senaryosunda boş liste döner.
        """

        return []

    def get_by_id(
        self,
        question_id: str,
    ) -> Question | None:
        """
        ID bazlı soru getirir.

        Test senaryosunda None döner.
        """

        return None


class DummyVectorStore(VectorStore):
    """
    VectorStore interface'inin mock implementasyonu.

    Gerçek vector database yerine
    lightweight test davranışı sağlar.
    """

    def add(
        self,
        *,
        id: str,
        text: str,
        embedding: list[float],
        metadata: dict,
    ) -> None:
        """
        Embedding ekleme operasyonu.

        Test amaçlı no-op davranışı sergiler.
        """

        return None

    def add_many(
        self,
        *,
        ids: list[str],
        texts: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict],
    ) -> None:
        """
        Toplu embedding ekleme operasyonu.

        Test amaçlı no-op davranışı sergiler.
        """

        return None

    def search(
        self,
        *,
        query_embedding: list[float],
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        """
        Semantic similarity search operasyonu.

        Test senaryosunda boş liste döndürür.
        """

        return []

    def count(self) -> int:
        """
        Store içerisindeki kayıt sayısını döndürür.

        Test senaryosunda 0 döner.
        """

        return 0


def test_dummy_evaluator_implements_interface() -> None:
    """
    DummyEvaluator implementasyonunun
    Evaluator contract'ine uyduğunu doğrular.

    Doğrulananlar:
        - evaluate çağrılabiliyor mu
        - expected structure dönüyor mu
        - score alanı mevcut mu
        - feedback alanı mevcut mu
    """

    evaluator = DummyEvaluator()

    question = build_question()

    result = evaluator.evaluate(
        question=question,
        answer="RAG combines retrieval and generation.",
    )

    assert result["score"] == 10
    assert result["feedback"] == "OK"


def test_dummy_llm_client_implements_interface() -> None:
    """
    DummyLLMClient implementasyonunun
    LLMClient contract'ine uyduğunu doğrular.

    Doğrulananlar:
        - generate çalışıyor mu
        - response tipi doğru mu
        - response field'ları mevcut mu
    """

    client = DummyLLMClient()

    response = client.generate("Hello")

    assert response.text == "dummy response"
    assert response.model_name == "dummy-model"


def test_dummy_scoring_engine_implements_interface() -> None:
    """
    DummyScoringEngine implementasyonunun
    ScoringEngine contract'ine uyduğunu doğrular.

    Amaç:
        score metodunun beklenen şekilde
        float döndürdüğünü garanti etmek.
    """

    engine = DummyScoringEngine()

    question = build_question()

    context = ScoringContext()

    assert engine.score(question, context) == 1.0


def test_dummy_question_repository_implements_interface() -> None:
    """
    DummyQuestionRepository implementasyonunun
    repository contract'ini sağladığını doğrular.

    Doğrulananlar:
        - list_all çalışıyor mu
        - get_by_id çalışıyor mu
        - dönüş tipleri doğru mu
    """

    repository = DummyQuestionRepository()

    assert repository.list_all() == []
    assert repository.get_by_id("q1") is None


def test_dummy_vector_store_implements_interface() -> None:
    """
    DummyVectorStore implementasyonunun
    VectorStore contract'ine uyduğunu doğrular.

    Doğrulananlar:
        - add operasyonu çalışıyor mu
        - search operasyonu çalışıyor mu
        - count operasyonu çalışıyor mu
    """

    store = DummyVectorStore()

    store.add(
        id="q1",
        text="What is RAG?",
        embedding=[0.1, 0.2, 0.3],
        metadata={"category": "RAG"},
    )

    results = store.search(
        query_embedding=[0.1, 0.2, 0.3],
        limit=5,
    )

    assert results == []
    assert store.count() == 0