from abc import ABC, abstractmethod
from processor.transformer.lexer import Lexer
from typing import TextIO, Iterator, List, Generic, TypeVar


ReturnType = TypeVar("ReturnType")


class TransformStrategy(ABC, Generic[ReturnType]):
    @abstractmethod
    def file_transform_lazy(self, data: TextIO) -> ReturnType:
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def data_transform_lazy(self, data: str) -> ReturnType:
        raise NotImplementedError("This method should be overridden.")


class CSVTransformedDataDTO:
    def __init__(self, headers: List[str], rows: Iterator[List[str]]):
        self.headers = headers
        self.rows = rows


class CsvTransformStrategy(TransformStrategy[CSVTransformedDataDTO]):
    def __init__(self, line_delimiter: str) -> None:
        self.line_delimiter = line_delimiter
        self.csv_lexer = Lexer(delimiter=self.line_delimiter)

    def file_transform_lazy(self, data: TextIO) -> CSVTransformedDataDTO:
        headers = self.csv_lexer.tokenize(data.readline().strip())

        def row_iterator() -> Iterator[List[str]]:
            for line in data:
                yield self.csv_lexer.tokenize(line.strip())

        return CSVTransformedDataDTO(headers, row_iterator())

    def data_transform_lazy(self, data: str) -> CSVTransformedDataDTO:
        splitted_lines = self.csv_lexer.lines_split_lazy(data)

        headers = self.csv_lexer.tokenize(next(splitted_lines))

        def row_iterator() -> Iterator[List[str]]:
            for line in splitted_lines:
                yield self.csv_lexer.tokenize(line)

        return CSVTransformedDataDTO(headers, row_iterator())
