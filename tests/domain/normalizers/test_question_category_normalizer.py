from src.domain.normalizers.implementations.question_category_normalizer import (
    QuestionCategoryNormalizer,
)


def test_normalize_trims_and_collapses_whitespace() -> None:
    normalizer = QuestionCategoryNormalizer()

    result = normalizer.normalize(value="  System    Design  ")

    assert result == "system_design"


def test_normalize_replaces_symbols_with_expected_tokens() -> None:
    normalizer = QuestionCategoryNormalizer()

    result = normalizer.normalize(value="API / Backend & Micro-Services")

    assert result == "api___backend_and_micro_services"
