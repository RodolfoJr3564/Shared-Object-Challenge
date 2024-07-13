from typing import List, Generic, TypeVar, Union
from processor.processor.comparison_type_enum import ComparisonTypeEnum

ComparisonType = TypeVar("ComparisonType", int, str)


class Comparison(Generic[ComparisonType]):
    def __init__(
        self,
        comparison_header: str,
        comparison_type: ComparisonTypeEnum,
        reference_value: Union[str, int],
    ):
        if not isinstance(comparison_type, ComparisonTypeEnum):
            raise ValueError(f"Invalid comparison type: {comparison_type}")
        self.comparison_header = comparison_header
        self.reference_value: Union[str, int] = reference_value
        self.comparison_type: ComparisonTypeEnum = comparison_type

    def is_satisfied_by(self, comparison_value: Union[str, int]) -> bool:
        return self.__is_satisfied_by(
            *self.cast_many([comparison_value, self.reference_value])
        )

    def cast_many(self, values: List[Union[str, int]]) -> List[Union[str, int]]:
        try:
            return [int(value) for value in values]
        except ValueError:
            return [str(value) for value in values]

    def __is_satisfied_by(
        self, comparison: Union[str, int], reference: Union[str, int]
    ) -> bool:
        function_map = {
            ComparisonTypeEnum.EQUAL: self._equal,
            ComparisonTypeEnum.GREATER_THAN: self._greater_than,
            ComparisonTypeEnum.LESS_THAN: self._less_than,
            ComparisonTypeEnum.NOT_EQUAL: self._not_equal,
            ComparisonTypeEnum.GREATER_OR_EQUAL: self._greater_or_equal,
            ComparisonTypeEnum.LESS_OR_EQUAL: self._less_or_equal,
        }
        return function_map[self.comparison_type](comparison, reference)  # type: ignore

    def _equal(self, comparison: ComparisonType, reference: ComparisonType) -> bool:
        return comparison == reference

    def _greater_than(
        self,
        comparison: ComparisonType,
        reference: ComparisonType,
    ) -> bool:
        return comparison > reference

    def _less_than(self, comparison: ComparisonType, reference: ComparisonType) -> bool:
        return comparison < reference

    def _not_equal(self, comparison: ComparisonType, reference: ComparisonType) -> bool:
        return comparison != reference

    def _greater_or_equal(
        self,
        comparison: ComparisonType,
        reference: ComparisonType,
    ) -> bool:
        return comparison >= reference

    def _less_or_equal(
        self, comparison: ComparisonType, reference: ComparisonType
    ) -> bool:
        return comparison <= reference
