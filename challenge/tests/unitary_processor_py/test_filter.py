from unittest.mock import patch
import pytest
from typing import Dict, List, Union
from processor_py.filter import (
    line_match,
    tokenize_filter,
    ComparisonTypeEnum,
    parse_filters,
    is_satisfied_by,
)


class TestTokenizeFilter:
    @pytest.mark.parametrize(
        "filter_string, expected",
        [
            ("age >= 30", ["age", ">=", "30"]),
            ("name = 'Alice'", ["name", "=", "Alice"]),
            ("height < 180", ["height", "<", "180"]),
            ("weight != 70", ["weight", "!=", "70"]),
        ],
    )
    def test_tokenize_filter_valid(
        self, filter_string: str, expected: List[str]
    ) -> None:
        assert tokenize_filter(filter_string) == expected

    @pytest.mark.parametrize(
        "filter_string",
        [
            ("age >= "),
            ("= 'Alice'"),
            ("height < "),
            ("weight ! 70"),
            ("invalid"),
        ],
    )
    def test_tokenize_filter_invalid(self, filter_string: str) -> None:
        with pytest.raises(ValueError, match=f"Invalid filter: '{filter_string}'"):
            tokenize_filter(filter_string)


class TestParseFilters:
    @pytest.fixture
    def valid_filter_string(self) -> str:
        return "age > 30\nname = Alice"

    @pytest.fixture
    def invalid_filter_string(self) -> str:
        return "age >> 30\nname = Alice"

    @pytest.fixture
    def empty_filter_string(self) -> str:
        return ""

    def test_parse_filters_valid(self, valid_filter_string: str) -> None:
        with patch(
            "processor_py.filter.tokenize_filter",
            side_effect=[("age", ">", "30"), ("name", "=", "Alice")],
        ):
            expected_result = {
                "age": [
                    {
                        "comparison_type": ComparisonTypeEnum.GREATER_THAN,
                        "reference_value": "30",
                    }
                ],
                "name": [
                    {
                        "comparison_type": ComparisonTypeEnum.EQUAL,
                        "reference_value": "Alice",
                    }
                ],
            }
            assert parse_filters(valid_filter_string) == expected_result

    def test_parse_filters_invalid_operator(self, invalid_filter_string: str) -> None:
        with patch(
            "processor_py.filter.tokenize_filter",
            side_effect=[("age", ">>", "30"), ("name", "=", "Alice")],
        ):
            with pytest.raises(ValueError, match="Invalid filter: 'age >> 30'"):
                parse_filters(invalid_filter_string)

    def test_parse_filters_empty_string(self, empty_filter_string: str) -> None:
        assert parse_filters(empty_filter_string) == {}

    def test_parse_filters_with_empty_lines(self) -> None:
        filter_string = "age > 30\n\nname = Alice\n"
        with patch(
            "processor_py.filter.tokenize_filter",
            side_effect=[("age", ">", "30"), ("name", "=", "Alice")],
        ):
            expected_result = {
                "age": [
                    {
                        "comparison_type": ComparisonTypeEnum.GREATER_THAN,
                        "reference_value": "30",
                    }
                ],
                "name": [
                    {
                        "comparison_type": ComparisonTypeEnum.EQUAL,
                        "reference_value": "Alice",
                    }
                ],
            }
            assert parse_filters(filter_string) == expected_result

    def test_parse_filters_duplicate_headers(self) -> None:
        filter_string = "age > 30\nage < 40"
        with patch(
            "processor_py.filter.tokenize_filter",
            side_effect=[("age", ">", "30"), ("age", "<", "40")],
        ):
            expected_result = {
                "age": [
                    {
                        "comparison_type": ComparisonTypeEnum.GREATER_THAN,
                        "reference_value": "30",
                    },
                    {
                        "comparison_type": ComparisonTypeEnum.LESS_THAN,
                        "reference_value": "40",
                    },
                ],
            }
            assert parse_filters(filter_string) == expected_result


class TestIsSatisfiedBy:

    @pytest.mark.parametrize(
        "comparison_value, reference_value, comparison_type, expected",
        [
            ("5", "5", ComparisonTypeEnum.EQUAL, True),
            ("5", "4", ComparisonTypeEnum.GREATER_THAN, True),
            ("5", "6", ComparisonTypeEnum.LESS_THAN, True),
            ("5", "5", ComparisonTypeEnum.NOT_EQUAL, False),
            ("5", "5", ComparisonTypeEnum.GREATER_OR_EQUAL, True),
            ("5", "5", ComparisonTypeEnum.LESS_OR_EQUAL, True),
            (5, 5, ComparisonTypeEnum.EQUAL, True),
            (5, 4, ComparisonTypeEnum.GREATER_THAN, True),
            (5, 6, ComparisonTypeEnum.LESS_THAN, True),
            (5, 5, ComparisonTypeEnum.NOT_EQUAL, False),
            (5, 5, ComparisonTypeEnum.GREATER_OR_EQUAL, True),
            (5, 5, ComparisonTypeEnum.LESS_OR_EQUAL, True),
            ("a", "a", ComparisonTypeEnum.EQUAL, True),
            ("a", "b", ComparisonTypeEnum.LESS_THAN, True),
            ("b", "a", ComparisonTypeEnum.GREATER_THAN, True),
            ("a", "a", ComparisonTypeEnum.NOT_EQUAL, False),
        ],
    )
    def test_is_satisfied_by(
        self,
        reference_value: Union[str, int],
        comparison_value: Union[str, int],
        comparison_type: ComparisonTypeEnum,
        expected: bool,
    ) -> None:
        assert (
            is_satisfied_by(reference_value, comparison_value, comparison_type)
            == expected
        )

    def test_is_satisfied_by_invalid_reference_value(self) -> None:
        with pytest.raises(ValueError):
            is_satisfied_by("invalid", 5, ComparisonTypeEnum.GREATER_THAN)

    def test_is_satisfied_by_invalid_comparison_value(self) -> None:
        with pytest.raises(ValueError):
            is_satisfied_by(5, "invalid", ComparisonTypeEnum.GREATER_THAN)


class TestLineMatch:

    @pytest.fixture
    def valid_headers(self) -> List[str]:
        return ["id", "name", "age"]

    @pytest.fixture
    def valid_row(self) -> List[str]:
        return ["1", "Alice", "30"]

    @pytest.fixture
    def valid_comparison_map(
        self,
    ) -> Dict[str, List[Dict[str, Union[ComparisonTypeEnum, str]]]]:
        return {
            "age": [
                {
                    "reference_value": "25",
                    "comparison_type": ComparisonTypeEnum.GREATER_THAN,
                }
            ]
        }

    def test_line_match_valid_case(
        self,
        valid_row: List[str],
        valid_headers: List[str],
        valid_comparison_map: Dict[
            str, List[Dict[str, Union[ComparisonTypeEnum, str]]]
        ],
    ) -> None:
        with patch("processor_py.filter.is_satisfied_by", return_value=True):
            assert line_match(valid_row, valid_headers, valid_comparison_map) == True

    def test_line_match_invalid_header(
        self,
        valid_row: List[str],
        valid_comparison_map: Dict[
            str, List[Dict[str, Union[ComparisonTypeEnum, str]]]
        ],
    ) -> None:
        invalid_headers = ["id", "name"]
        with pytest.raises(
            ValueError, match="Header 'age' not found in CSV file/string"
        ):
            line_match(valid_row, invalid_headers, valid_comparison_map)

    def test_line_match_invalid_reference_value(
        self, valid_row: List[str], valid_headers: List[str]
    ) -> None:
        invalid_comparison_map = {
            "age": [
                {
                    "reference_value": "invalid",
                    "comparison_type": ComparisonTypeEnum.GREATER_THAN,
                }
            ]
        }
        with patch(
            "processor_py.filter.is_satisfied_by",
            side_effect=ValueError("Invalid reference value"),
        ):
            with pytest.raises(
                ValueError, match="Invalid reference value for header 'age'"
            ):
                line_match(valid_row, valid_headers, invalid_comparison_map)

    def test_line_match_non_matching_case(
        self,
        valid_row: List[str],
        valid_headers: List[str],
        valid_comparison_map: Dict[
            str, List[Dict[str, Union[ComparisonTypeEnum, str]]]
        ],
    ) -> None:
        with patch("processor_py.filter.is_satisfied_by", return_value=False):
            assert line_match(valid_row, valid_headers, valid_comparison_map) == False

    def test_line_match_no_comparisons(
        self, valid_row: List[str], valid_headers: List[str]
    ) -> None:
        empty_comparison_map: Dict[
            str, List[Dict[str, Union[ComparisonTypeEnum, str]]]
        ] = {}
        assert line_match(valid_row, valid_headers, empty_comparison_map) == True
