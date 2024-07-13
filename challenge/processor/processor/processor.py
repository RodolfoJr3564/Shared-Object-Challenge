from typing import Iterator, List

from processor.processor.filter import Filter
from processor.transformer.transformer_strategy import CSVTransformedDataDTO


class ProcessedLazyDataDTO:
    def __init__(self, headers: List[str], rows: Iterator[List[str]]):
        self.headers = headers
        self.rows = rows


class Processor:
    def __init__(
        self,
        transformed_lazy_data_DTO: CSVTransformedDataDTO,
        entryComparisonMatcher: Filter,
    ):
        self.transformed_lazy_data_DTO = transformed_lazy_data_DTO
        self.entryComparisonMatcher = entryComparisonMatcher

    def build_lazy(self) -> ProcessedLazyDataDTO:
        headers = self.transformed_lazy_data_DTO.headers

        def row_iterator() -> Iterator[List[str]]:
            for line in self.transformed_lazy_data_DTO.rows:
                if self.entryComparisonMatcher.is_satisfied_by(line):
                    yield line

        return ProcessedLazyDataDTO(headers, row_iterator())
