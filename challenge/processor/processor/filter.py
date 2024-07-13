from typing import Dict, List

from processor.processor.comparison import Comparison
from processor.processor.comparison_factory import ComparisonFactory
from processor.processor.comparison_type_enum import ComparisonTypeEnum


class Filter:
    def __init__(self, full_filter_string: str, headers: List[str]):
        self.comparisons: Dict[str, List[Comparison[str]]] = {
            header: [] for header in headers
        }

        self.headers = headers
        if full_filter_string == "":
            return

        operators_sorted = sorted(
            [op.value for op in ComparisonTypeEnum], key=len, reverse=True
        )

        comparisons = ComparisonFactory.parse_filters(
            full_filter_string=full_filter_string,
            valid_columns=headers,
            valid_sorted_operators=operators_sorted,
        )

        for comparison in comparisons:
            if comparison.comparison_header in self.comparisons:
                comparison_header = comparison.comparison_header
                self.comparisons[comparison_header].append(comparison)

        self.headers = headers

    def is_satisfied_by(self, row: List[str]) -> bool:
        is_match = True
        for header_position, header in enumerate(self.headers):
            header_comparisons = self.comparisons.get(header)

            if header_comparisons:
                is_match = all(
                    comparison.is_satisfied_by(row[header_position])
                    for comparison in header_comparisons
                )

                if not is_match:
                    break

        return is_match
