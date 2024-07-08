from typing import TextIO, Generic, TypeVar

from processor.transformer.transformer_strategy import (
    CsvTransformStrategy,
    CSVTransformedDataDTO,
    TransformStrategy,
)


ReturnType = TypeVar("ReturnType")


class Transformer(Generic[ReturnType]):
    """
    A class used to transform data by applying a lexer to it.
    """

    def __init__(self, transform_strategy: TransformStrategy[ReturnType]):
        self.__transform_strategy = transform_strategy

    def file_transform_lazy(self, file: TextIO) -> ReturnType:
        return self.__transform_strategy.file_transform_lazy(file)

    def data_transform_lazy(self, data: str) -> ReturnType:
        return self.__transform_strategy.data_transform_lazy(data)


class TransformerFactory:
    @staticmethod
    def create_csv_transformer(
        line_delimiter: str,
    ) -> Transformer[CSVTransformedDataDTO]:
        csv_transform_strategy = CsvTransformStrategy(line_delimiter)
        return Transformer(csv_transform_strategy)
