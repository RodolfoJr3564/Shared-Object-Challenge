from typing import Generator, List
import cython

@cython.cfunc
def tokenize(data: str, delimiter: str):
    if not delimiter:
        raise ValueError("Delimiter cannot be an empty string")
    return data.split(delimiter)

@cython.locals(line_delimiter=str, full_string=str, line_position=int, sliced_string=str, has_other_lines=cython.bint)
def lines_split_lazy(full_string: str, line_delimiter: str = "\n"):
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