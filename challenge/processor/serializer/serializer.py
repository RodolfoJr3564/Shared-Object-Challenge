import sys
from typing import List, Set

from processor.processor.processor import ProcessedLazyDataDTO
from processor.transformer.lexer import Lexer


class Serializer:
    def __init__(self, data: ProcessedLazyDataDTO):
        self.data = data

    def __stringify(self, headers: List[str], rows: List[str]) -> str:
        headers_string = ",".join(headers) + "\n"
        rows_string = "\n".join(rows)
        return headers_string + rows_string

    def stringify(self, selected_columns_input: str) -> str:
        if not selected_columns_input:
            rows = [",".join(row) for row in self.data.rows]
            return self.__stringify(self.data.headers, rows)

        selected_columns = Lexer(delimiter=",").tokenize(selected_columns_input)

        selected_column_indexes = set()
        for column in selected_columns:
            if column not in self.data.headers:
                sys.stderr.write(f"Header '{column}' not found in CSV file/string")
                sys.exit(1)

            selected_column_indexes.add(self.data.headers.index(column))

        filtered_headers = self.filter_entries(
            selected_column_indexes, self.data.headers
        )
        filtered_rows = [
            ",".join(self.filter_entries(selected_column_indexes, row))
            for row in self.data.rows
        ]

        return self.__stringify(filtered_headers, filtered_rows)

    def filter_entries(
        self,
        selected_column_indexes: Set[int],
        entry_list: List[str],
    ) -> List[str]:
        return [
            entry
            for index, entry in enumerate(entry_list)
            if index in selected_column_indexes
        ]
