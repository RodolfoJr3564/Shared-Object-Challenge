from typing import List, Iterator
from abc import ABC, abstractmethod


class LexerInterface(ABC):
    @abstractmethod
    def tokenize(self, data: str) -> List[str]:
        raise NotImplementedError("This method should be overridden.")

    @abstractmethod
    def lines_split_lazy(self, full_string: str, line_delimiter: str) -> Iterator[str]:
        raise NotImplementedError("This method should be overridden.")


class Lexer(LexerInterface):
    """
    A class used to tokenize data based on a delimiter.
    """

    def __init__(self, delimiter: str) -> None:
        self.delimiter = delimiter

    def tokenize(self, data: str) -> List[str]:
        return data.split(self.delimiter)

    def lines_split_lazy(
        self, full_string: str, line_delimiter: str = "\n"
    ) -> Iterator[str]:
        has_other_lines = line_delimiter in full_string

        if not has_other_lines:
            yield full_string
            return

        sliced_string = full_string

        while has_other_lines:
            line_position = sliced_string.find(line_delimiter)
            yield sliced_string[:line_position]

            sliced_string = sliced_string[line_position + len(line_delimiter) :]
            has_other_lines = line_delimiter in sliced_string

        if sliced_string:
            yield sliced_string

        elif full_string.endswith(line_delimiter):
            yield ""
