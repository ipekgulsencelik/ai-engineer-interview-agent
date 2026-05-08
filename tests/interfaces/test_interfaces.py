from src.domain.question.question import Question
from src.domain.results.evaluation_result import EvaluationResult
from src.domain.scoring.scoring_context import ScoringContext
from src.domain.search.search_result import SearchResult
from src.interfaces.evaluator import Evaluator
from src.interfaces.llm_client import LLMClient
from src.interfaces.question_repository import QuestionRepository
from src.interfaces.scoring_engine import ScoringEngine
from src.interfaces.vector_store import VectorStore


class DummyEvaluator(Evaluator):
    def evaluate(self, question: Question, answer: str) -> EvaluationResult:
        return EvaluationResult(score=10, feedback="OK")


class DummyLLMClient(LLMClient):
    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        return "dummy response"


class DummyScoringEngine(ScoringEngine):
    def score(self, question: Question, context: ScoringContext) -> float:
        return 1.0


class DummyQuestionRepository(QuestionRepository):
    def list_all(self) -> list[Question]:
        return []

    def get_by_id(self, question_id: str) -> Question | None:
        return None


class DummyVectorStore(VectorStore):
    def add(self, id: str, text: str, metadata: dict) -> None:
        return None

    def search(
        self,
        query: str,
        limit: int = 5,
        where: dict | None = None,
    ) -> list[SearchResult]:
        return []


def test_dummy_evaluator_implements_interface() -> None:
    evaluator = DummyEvaluator()
    question = Question(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[],
        keywords=[],
    )

    result = evaluator.evaluate(question, "RAG combines retrieval and generation.")

    assert result.score == 10


def test_dummy_llm_client_implements_interface() -> None:
    client = DummyLLMClient()

    assert client.generate("Hello") == "dummy response"


def test_dummy_scoring_engine_implements_interface() -> None:
    engine = DummyScoringEngine()
    question = Question(
        id="q1",
        text="What is RAG?",
        category="RAG",
        level="JR",
        difficulty=1,
        question_type="conceptual",
        expected_points=[],
        keywords=[],
    )
    context = ScoringContext()

    assert engine.score(question, context) == 1.0


def test_dummy_question_repository_implements_interface() -> None:
    repository = DummyQuestionRepository()

    assert repository.list_all() == []
    assert repository.get_by_id("q1") is None


def test_dummy_vector_store_implements_interface() -> None:
    store = DummyVectorStore()

    store.add(id="q1", text="What is RAG?", metadata={})

    assert store.search("RAG") == []
