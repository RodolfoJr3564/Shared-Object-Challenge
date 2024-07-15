import sys
from typing import List, Set, Dict, Union
from processor_py.serializer import stringify_line
from processor_py.lexer import tokenize, lines_split_lazy
from processor_py.filter import line_match, parse_filters


def process_csv(
    csv_data: str, selected_columns: str, row_filter_definitions: str
) -> None:
    """
    Process the CSV data by applying filters and selecting columns.

    @param csv_data The CSV data to be processed.
    @param selected_columns The columns to be selected from the CSV data.
    @param row_filter_definitions The filters to be applied to the CSV data.

    @return void
    """
    try:
        splitted_lines = lines_split_lazy(csv_data)
        headers = tokenize(next(splitted_lines), ",")

        filter_comparisons = {}
        if row_filter_definitions:
            filter_comparisons = parse_filters(row_filter_definitions)

        selected_column_indexes: set[int] = parse_columns(
            selected_columns, headers
        ).get(
            "selected_column_indexes"
        )  # type: ignore

        serialized_headers_response = stringify_line(
            {index: headers[index] for index in selected_column_indexes}
        )

        serialized_response = serialized_headers_response
        for line in splitted_lines:
            tokenized_line = tokenize(line, ",")
            if line_match(tokenized_line, headers, filter_comparisons):
                serialized_line = stringify_line(
                    {index: tokenized_line[index] for index in selected_column_indexes}
                )
                serialized_response = "\n".join([serialized_response, serialized_line])

        print(serialized_response)

    except Exception as error:
        sys.stderr.write(str(error))
        sys.exit(1)


def process_csv_file(
    csv_file_path: str, selected_columns: str, row_filter_definitions: str
) -> None:
    """
    Process the CSV file by applying filters and selecting columns.

    @param csv_file_path The path to the CSV file to be processed.
    @param selected_columns The columns to be selected from the CSV data.
    @param row_filter_definitions The filters to be applied to the CSV data.

    @return void
    """
    try:
        serialized_response = ""

        with open(csv_file_path, "r") as file:
            headers = tokenize(file.readline().strip(), ",")

            filter_comparisons = {}
            if row_filter_definitions:
                filter_comparisons = parse_filters(row_filter_definitions)

            selected_column_indexes: set[int] = parse_columns(
                selected_columns, headers
            ).get(
                "selected_column_indexes"
            )  # type: ignore

            serialized_headers_response = stringify_line(
                {index: headers[index] for index in selected_column_indexes}
            )

            serialized_response = serialized_headers_response
            for line in file:
                tokenized_line = tokenize(line.strip(), ",")
                if line_match(tokenized_line, headers, filter_comparisons):
                    serialized_line = stringify_line(
                        {
                            index: tokenized_line[index]
                            for index in selected_column_indexes
                        }
                    )
                    serialized_response = "\n".join(
                        [serialized_response, serialized_line]
                    )

        print(serialized_response)

    except Exception as error:
        sys.stderr.write(str(error))
        sys.exit(1)


def parse_columns(
    selected_columns: str, headers: List[str]
) -> dict[str, Union[List[str], Set[int]]]:
    """
    Parse the columns from the CSV data.

    @return The columns from the CSV data.
    """
    selected_column_tokens = []

    if selected_columns:
        selected_column_tokens = tokenize(selected_columns, ",")

        selected_column_indexes: Set[int] = set()
        for column in selected_column_tokens:
            if column not in headers:
                raise ValueError(f"Header '{column}' not found in CSV file/string")
            selected_column_indexes.add(headers.index(column))
    else:
        selected_column_indexes = set(range(len(headers)))

    return {
        "selected_column_indexes": selected_column_indexes,
        "selected_columns": selected_column_tokens,
    }
