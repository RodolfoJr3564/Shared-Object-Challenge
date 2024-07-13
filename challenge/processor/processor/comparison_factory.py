import re
from typing import List
from processor.processor.comparison import Comparison
from processor.processor.comparison_type_enum import ComparisonTypeEnum
import sys


class ComparisonError(Exception):
    pass


class HeaderNotFoundError(ComparisonError):
    pass


class InvalidFilterError(ComparisonError):
    pass


class ComparisonFactory:
    @staticmethod
    def tokenize_filter(filter_string: str, operators_sorted: List[str]) -> List[str]:
        pattern = re.compile(
            rf"(?P<header>[^\s,]+?)\s*"
            rf"(?P<operator>{'|'.join(re.escape(op) for op in operators_sorted)})"
            rf"\s*"
            rf"(?P<value>\".*?\"|'.*?'|[^\s,]+)"
        )

        match = pattern.match(filter_string)
        if not match:
            raise InvalidFilterError(f"Invalid filter: '{filter_string}'")

        header = match.group("header")
        operator = match.group("operator").strip()
        value = match.group("value").strip().strip("'\"")

        return [header, operator, value]

    @staticmethod
    def parse_filters(
        full_filter_string: str,
        valid_columns: List[str],
        valid_sorted_operators: List[str],
    ) -> List[Comparison[str]]:

        filters: List[Comparison[str]] = []
        filter_list: List[str] = full_filter_string.split("\n")

        for filter in filter_list:
            try:
                tokens = ComparisonFactory.tokenize_filter(
                    filter, valid_sorted_operators
                )

                if tokens:
                    header, operator, value = tokens

                    if header not in valid_columns:
                        raise HeaderNotFoundError(
                            f"Header '{header}' not found in CSV file/string"
                        )

                    comparison_type = ComparisonTypeEnum(operator)

                    filters.append(
                        Comparison(
                            comparison_header=header,
                            comparison_type=comparison_type,
                            reference_value=value,
                        )
                    )
            except Exception as error:
                sys.stderr.write(str(error))
                sys.exit(1)

        return filters
