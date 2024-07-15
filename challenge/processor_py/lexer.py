from typing import Generator, List


def tokenize(data: str, delimiter: str) -> List[str]:
    if not delimiter:
        raise ValueError("Delimiter cannot be an empty string")
    return data.split(delimiter)


def lines_split_lazy(
    full_string: str, line_delimiter: str = "\n"
) -> Generator[str, None, None]:
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
