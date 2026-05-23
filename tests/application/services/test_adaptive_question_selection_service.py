from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType, SimpleNamespace


def _stub_module(name: str, **attrs: object) -> None:
    module = ModuleType(name)
    for key, value in attrs.items():
        setattr(module, key, value)
    sys.modules[name] = module


def _load_service_module():
    class QuestionRankingService: ...

    class QuestionRetrievalService: ...

    class QuestionSelectionPolicy:
        def select_best_candidate(self, *, ranked_candidates):
            return ranked_candidates[0]

    class AskedQuestionFilterPolicy:
        @staticmethod
        def filter(*, search_results, asked_question_ids):
            return [x for x in search_results if x not in asked_question_ids]

    _stub_module("src.application.services.question_ranking_service", QuestionRankingService=QuestionRankingService)
    _stub_module("src.application.services.question_retrieval_service", QuestionRetrievalService=QuestionRetrievalService)
    _stub_module("src.domain.policies.asked_question_filter_policy", AskedQuestionFilterPolicy=AskedQuestionFilterPolicy)
    _stub_module("src.domain.policies.difficulty_window_policy", DifficultyWindowPolicy=object)
    _stub_module("src.domain.policies.question_selection_policy", QuestionSelectionPolicy=QuestionSelectionPolicy)
    _stub_module("src.domain.results.selection_result", SelectionResult=object)
    _stub_module("src.domain.value_objects.search_filters", SearchFilters=object)
    _stub_module("src.domain.value_objects.interview_state", InterviewState=object)

    spec = importlib.util.spec_from_file_location(
        "adaptive_service_under_test",
        Path("src/application/services/adaptive_question_selection_service.py"),
    )
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_select_next_question_orchestrates_dependencies() -> None:
    module = _load_service_module()
    service_cls = module.AdaptiveQuestionSelectionService

    class RetrievalFake:
        def __init__(self) -> None:
            self.called_with = None

        def retrieve(self, *, query, context, top_k):
            self.called_with = (query, context, top_k)
            return ["q-1", "q-2"]

    class RankingFake:
        def __init__(self) -> None:
            self.called_with = None

        def rank_candidates(self, *, search_results, target_difficulty):
            self.called_with = (search_results, target_difficulty)
            return ["ranked-q"]

    class SelectionFake:
        def __init__(self) -> None:
            self.called_with = None

        def select_best_candidate(self, *, ranked_candidates):
            self.called_with = ranked_candidates
            return "selected-q"

    retrieval = RetrievalFake()
    ranking = RankingFake()
    selection = SelectionFake()

    state = SimpleNamespace(asked_question_ids=("q-1",), target_difficulty="medium")

    service = service_cls(retrieval_service=retrieval, ranking_service=ranking, selection_policy=selection)
    result = service.select_next_question(query="python", state=state, top_k=5)

    assert result == "selected-q"
    assert retrieval.called_with == ("python", state, 5)
    assert ranking.called_with == (["q-2"], "medium")
    assert selection.called_with == ["ranked-q"]
