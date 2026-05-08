import pytest

from src.domain.common.result import Result


def test_result_ok_returns_successful_result() -> None:
    result = Result.ok(data=123)

    assert result.success is True
    assert result.data == 123
    assert result.error is None


def test_result_fail_returns_failed_result() -> None:
    result = Result.fail("Something went wrong.")

    assert result.success is False
    assert result.data is None
    assert result.error == "Something went wrong."


def test_result_unwrap_returns_data_for_success() -> None:
    result = Result.ok("hello")

    assert result.unwrap() == "hello"


def test_result_unwrap_raises_for_failure() -> None:
    result = Result.fail("Failure.")

    with pytest.raises(ValueError, match="Failure."):
        result.unwrap()
