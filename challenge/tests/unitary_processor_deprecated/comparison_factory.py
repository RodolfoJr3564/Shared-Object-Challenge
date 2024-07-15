import pytest
from typing import List, Dict
from processor.processor.comparison_factory import ComparisonFactory
from processor.processor.comparison_type_enum import ComparisonTypeEnum


def test_tokens_matcher_valid() -> None:
    filter_entry = "header1 >= 10"
    match = ComparisonFactory.tokens_matcher(filter_entry)
    assert match is not None
    assert match.group(1) == "header1"
    assert match.group(2) == ">="
    assert match.group(3) == "10"


def test_tokens_matcher_invalid() -> None:
    filter_entry = "header1 # 10"
    match = ComparisonFactory.tokens_matcher(filter_entry)
    assert match is None


def test_parse_filters_single(
    valid_filters: Dict[str, str], headers: Dict[str, List[str]]
) -> None:
    filter_string = valid_filters["single_param_filter"]
    comparisons = ComparisonFactory.parse_filters(
        filter_string, headers["many_headers"]
    )
    assert len(comparisons) == 1
    assert comparisons[0].comparison_header == "header1"
    assert comparisons[0].comparison_type == ComparisonTypeEnum("=")
    assert comparisons[0].reference_value == "10"


def test_parse_filters_multiple(
    valid_filters: Dict[str, str], headers: Dict[str, List[str]]
) -> None:
    filter_string = valid_filters["many_filter_params"]
    comparisons = ComparisonFactory.parse_filters(
        filter_string, headers["many_headers"]
    )
    assert len(comparisons) == 4
    assert comparisons[0].comparison_header == "header1"
    assert comparisons[0].comparison_type == ComparisonTypeEnum("=")
    assert comparisons[0].reference_value == "10"
    assert comparisons[1].comparison_header == "header2"
    assert comparisons[1].comparison_type == ComparisonTypeEnum(">")
    assert comparisons[1].reference_value == "20"
    assert comparisons[2].comparison_header == "header3"
    assert comparisons[2].comparison_type == ComparisonTypeEnum("<=")
    assert comparisons[2].reference_value == "30"
    assert comparisons[3].comparison_header == "header4"
    assert comparisons[3].comparison_type == ComparisonTypeEnum("!=")
    assert comparisons[3].reference_value == "40"


def test_parse_filters_invalid(
    invalid_filters: Dict[str, str], headers: Dict[str, List[str]]
) -> None:
    filter_string = invalid_filters["invalid_operator_filter"]
    with pytest.raises(ValueError, match=r"Invalid filter expression"):
        ComparisonFactory.parse_filters(filter_string, headers["many_headers"])


def test_parse_filters_nonexistent_column(
    invalid_filters: Dict[str, str], headers: Dict[str, List[str]]
) -> None:
    filter_string = invalid_filters["nonexistent_column_filter"]
    with pytest.raises(ValueError, match=r"Invalid column: header6"):
        ComparisonFactory.parse_filters(filter_string, headers["many_headers"])


def test_parse_filters_invalid_column(
    invalid_filters: Dict[str, str], headers: Dict[str, List[str]]
) -> None:
    filter_string = invalid_filters["invalid_column_filter"]
    with pytest.raises(ValueError, match=r"Invalid filter expression"):
        ComparisonFactory.parse_filters(filter_string, headers["many_headers"])
