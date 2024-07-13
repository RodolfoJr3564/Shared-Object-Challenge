import pytest
from processor.processor.filter import Filter
from typing import List, Dict


def test_single_filter_valid(
    headers: Dict[str, List[str]],
    valid_filters: Dict[str, str],
    valid_rows: Dict[str, List[str]],
) -> None:
    filter_instance = Filter(
        valid_filters["single_param_filter"], headers["single_header"]
    )
    assert filter_instance.is_satisfied_by(valid_rows["single_item_row"]) is True


def test_multiple_filters_valid(
    headers: Dict[str, List[str]],
    valid_filters: Dict[str, str],
    valid_rows: Dict[str, List[str]],
) -> None:
    filter_instance = Filter(
        valid_filters["many_filter_params"], headers["many_headers"]
    )
    assert filter_instance.is_satisfied_by(valid_rows["many_item_row"]) is True


def test_comma_in_filter_valid(
    headers: Dict[str, List[str]],
    valid_filters: Dict[str, str],
    valid_rows: Dict[str, List[str]],
) -> None:
    filter_instance = Filter(valid_filters["comma_in_filter"], headers["many_headers"])
    assert filter_instance.is_satisfied_by(valid_rows["comma_item_row"]) is True


def test_invalid_operator_filter(
    headers: Dict[str, List[str]], invalid_filters: Dict[str, str]
) -> None:
    with pytest.raises(ValueError):
        Filter(invalid_filters["invalid_operator_filter"], headers["single_header"])


def test_nonexistent_column_filter(
    headers: Dict[str, List[str]], invalid_filters: Dict[str, str]
) -> None:
    with pytest.raises(ValueError):
        Filter(invalid_filters["nonexistent_column_filter"], headers["many_headers"])


def test_invalid_column_filter(
    headers: Dict[str, List[str]], invalid_filters: Dict[str, str]
) -> None:
    with pytest.raises(ValueError):
        Filter(invalid_filters["invalid_column_filter"], headers["single_header"])


def test_single_item_invalid_row(
    headers: Dict[str, List[str]],
    valid_filters: Dict[str, str],
    invalid_rows: Dict[str, List[str]],
) -> None:
    filter_instance = Filter(
        valid_filters["single_param_filter"], headers["single_header"]
    )
    assert (
        filter_instance.is_satisfied_by(invalid_rows["single_item_invalid_row"])
        is False
    )


def test_comma_item_invalid_row(
    headers: Dict[str, List[str]],
    valid_filters: Dict[str, str],
    invalid_rows: Dict[str, List[str]],
) -> None:
    filter_instance = Filter(valid_filters["comma_in_filter"], headers["many_headers"])
    assert (
        filter_instance.is_satisfied_by(invalid_rows["comma_item_invalid_row"]) is False
    )
