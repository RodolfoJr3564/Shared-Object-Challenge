from processor.transformer.transformer import Transformer
from typing import Generic, TypeVar


ReturnType = TypeVar("ReturnType")


class Ingestor(Generic[ReturnType]):
    def __init__(self, transformer: Transformer[ReturnType]) -> None:
        self.__transformer = transformer

    def transform_file_data_lazy(self, file_path: str) -> ReturnType:
        with open(file_path, "r") as file:
            return self.__transformer.file_transform_lazy(file)

    def read_data_in_memory(self, data: str) -> ReturnType:
        return self.__transformer.data_transform_lazy(data)
