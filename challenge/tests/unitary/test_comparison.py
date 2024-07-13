import pytest
from processor.processor.comparison import Comparison
from processor.processor.comparison_type_enum import ComparisonTypeEnum


def test_equal() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.EQUAL, "10")
    assert comparison.is_satisfied_by("10")
    assert not comparison.is_satisfied_by("5")


def test_greater_than() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.GREATER_THAN, "10")
    assert comparison.is_satisfied_by("15")
    assert not comparison.is_satisfied_by("10")


def test_less_than() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.LESS_THAN, "10")
    assert comparison.is_satisfied_by("5")
    assert not comparison.is_satisfied_by("10")


def test_not_equal() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.NOT_EQUAL, "10")
    assert comparison.is_satisfied_by("5")
    assert not comparison.is_satisfied_by("10")


def test_greater_or_equal() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.GREATER_OR_EQUAL, "10")
    assert comparison.is_satisfied_by("10")
    assert comparison.is_satisfied_by("15")
    assert not comparison.is_satisfied_by("5")


def test_less_or_equal() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.LESS_OR_EQUAL, "10")
    assert comparison.is_satisfied_by("10")
    assert comparison.is_satisfied_by("5")
    assert not comparison.is_satisfied_by("15")


def test_invalid_operator() -> None:
    with pytest.raises(ValueError):
        Comparison("header1", "invalid_operator", "10")  # type: ignore


def test_casting_and_data_types() -> None:
    comparison = Comparison("header1", ComparisonTypeEnum.EQUAL, "10")
    assert comparison.is_satisfied_by(10)
    assert comparison.is_satisfied_by("10")
    comparison = Comparison("header1", ComparisonTypeEnum.EQUAL, "string")
    assert comparison.is_satisfied_by("string")
    assert not comparison.is_satisfied_by("another_string")


@pytest.mark.parametrize(
    "header, comparison_type, ref_value, value, expected",
    [
        ("header1", ComparisonTypeEnum.EQUAL, "10", "10", True),
        ("header1", ComparisonTypeEnum.GREATER_THAN, "10", "15", True),
        ("header1", ComparisonTypeEnum.LESS_THAN, "10", "5", True),
        ("header1", ComparisonTypeEnum.NOT_EQUAL, "10", "5", True),
        ("header1", ComparisonTypeEnum.GREATER_OR_EQUAL, "10", "10", True),
        ("header1", ComparisonTypeEnum.LESS_OR_EQUAL, "10", "10", True),
        ("header1", ComparisonTypeEnum.LESS_OR_EQUAL, "10", "5", True),
        ("header1", ComparisonTypeEnum.EQUAL, "10", "5", False),
        ("header1", ComparisonTypeEnum.GREATER_THAN, "10", "5", False),
        ("header1", ComparisonTypeEnum.LESS_THAN, "10", "15", False),
        ("header1", ComparisonTypeEnum.NOT_EQUAL, "10", "10", False),
        ("header1", ComparisonTypeEnum.GREATER_OR_EQUAL, "10", "5", False),
        ("header1", ComparisonTypeEnum.LESS_OR_EQUAL, "10", "15", False),
    ],
)
def test_comparisons(
    header: str,
    comparison_type: ComparisonTypeEnum,
    ref_value: str,
    value: str,
    expected: bool,
) -> None:
    comparison = Comparison(header, comparison_type, ref_value)
    assert comparison.is_satisfied_by(value) == expected
