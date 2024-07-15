from typing import Callable, List, Dict, Union
from enum import Enum
import re


class ComparisonTypeEnum(Enum):
    EQUAL = "="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    NOT_EQUAL = "!="
    GREATER_OR_EQUAL = ">="
    LESS_OR_EQUAL = "<="


comparison_priority_operators = ["<=", ">=", "!=", "=", ">", "<"]


def tokenize_filter(filter_string: str) -> List[str]:
    operator_pattern = re.compile(
        r"|".join(map(re.escape, comparison_priority_operators))
    )
    match = operator_pattern.search(filter_string)

    if match:
        operator = match.group()
        header = filter_string[: match.start()].strip()
        value = filter_string[match.end() :].strip().strip("'\"")

        if header and value:
            return [header, operator, value]

    raise ValueError(f"Invalid filter: '{filter_string}'")


def parse_filters(
    row_filter_definitions: str,
) -> Dict[str, List[Dict[str, Union[ComparisonTypeEnum, str]]]]:
    filters: Dict[str, List[Dict[str, Union[ComparisonTypeEnum, str]]]] = {}
    filter_list = row_filter_definitions.split("\n")
    print(row_filter_definitions)
    for filter in filter_list:
        if not filter.strip():
            continue

        header, operator, value = tokenize_filter(filter)

        if operator not in comparison_priority_operators:
            raise ValueError(f"Invalid filter: '{filter}'")

        comparison_type = ComparisonTypeEnum(operator)

        comparison_entry = {
            "comparison_type": comparison_type,
            "reference_value": value,
        }

        if header in filters:
            filters[header].append(comparison_entry)  # type: ignore
        else:
            filters[header] = [comparison_entry]  # type: ignore

    return filters


compare: Dict[
    ComparisonTypeEnum, Callable[[Union[int, str], Union[int, str]], bool]
] = {
    ComparisonTypeEnum.EQUAL: lambda comparison_value, reference_value: (
        comparison_value == reference_value
    ),
    ComparisonTypeEnum.GREATER_THAN: lambda comparison_value, reference_value: (
        comparison_value > reference_value
    ),  # type: ignore
    ComparisonTypeEnum.LESS_THAN: lambda comparison_value, reference_value: (
        comparison_value < reference_value
    ),  # type: ignore
    ComparisonTypeEnum.NOT_EQUAL: lambda comparison_value, reference_value: (
        comparison_value != reference_value
    ),  # type: ignore
    ComparisonTypeEnum.GREATER_OR_EQUAL: lambda comparison_value, reference_value: (
        comparison_value >= reference_value
    ),  # type: ignore
    ComparisonTypeEnum.LESS_OR_EQUAL: lambda comparison_value, reference_value: (
        comparison_value <= reference_value
    ),  # type: ignore
}


def is_satisfied_by(
    reference_value: Union[str, int],
    comparison_value: Union[str, int],
    comparison_type: ComparisonTypeEnum,
) -> bool:
    try:
        ref_value = int(reference_value)
        comp_value = int(comparison_value)
    except ValueError:
        if isinstance(reference_value, str) and isinstance(comparison_value, str):
            ref_value = reference_value  # type: ignore
            comp_value = comparison_value  # type: ignore
        else:
            raise ValueError(
                "Both reference_value and comparison_value must be either int or str"
            )

    if comparison_type not in compare:
        raise ValueError(f"Invalid comparison type: '{comparison_type}'")

    return compare[comparison_type](comp_value, ref_value)


def line_match(
    row: List[str],
    headers: List[str],
    comparison_map: Dict[str, List[Dict[str, Union[ComparisonTypeEnum, str]]]],
) -> bool:
    for comparison_header in comparison_map:
        if comparison_header not in headers:
            raise ValueError(
                f"Header '{comparison_header}' not found in CSV file/string"
            )

        header_comparisons = comparison_map[comparison_header]
        comparison_value = row[headers.index(comparison_header)]
        try:
            comparison_header_matches = [
                is_satisfied_by(
                    reference_value=header_comparison.get("reference_value"),  # type: ignore
                    comparison_type=header_comparison.get("comparison_type"),  # type: ignore
                    comparison_value=comparison_value,
                )
                for header_comparison in header_comparisons
            ]

            is_match = all(comparison_header_matches)
        except Exception:
            raise ValueError(
                f"Invalid reference value for header '{comparison_header}'"
            )

        if not is_match:
            return False

    return True
