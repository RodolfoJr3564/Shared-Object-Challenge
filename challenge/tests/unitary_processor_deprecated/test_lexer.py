from processor.transformer.lexer import Lexer, LexerInterface
import pytest

# tokenize tests


def test_tokenize() -> None:
    lexer: LexerInterface = Lexer(delimiter=",")
    data = "a,b,c"
    expected = ["a", "b", "c"]
    assert lexer.tokenize(data) == expected


def test_tokenize_with_different_delimiter() -> None:
    lexer = Lexer(delimiter="|")
    data = "a|b|c"
    expected = ["a", "b", "c"]
    assert lexer.tokenize(data) == expected


def test_tokenize_with_empty_string() -> None:
    lexer = Lexer(delimiter=",")
    data = ""
    expected = [""]
    assert lexer.tokenize(data) == expected


# lines_split_lazy tests


def test_lines_split_lazy() -> None:
    lexer = Lexer(delimiter=",")
    data = "line1\nline2\nline3"
    expected = ["line1", "line2", "line3"]
    result = list(lexer.lines_split_lazy(data, line_delimiter="\n"))
    assert result == expected


def test_lines_split_lazy_with_different_delimiter() -> None:
    lexer = Lexer(delimiter=",")
    data = "line1|line2|line3"
    expected = ["line1", "line2", "line3"]
    result = list(lexer.lines_split_lazy(data, line_delimiter="|"))
    assert result == expected


def test_lines_split_lazy_with_no_delimiter() -> None:
    lexer = Lexer(delimiter=",")
    data = "line1line2line3"
    expected = ["line1line2line3"]
    result = list(lexer.lines_split_lazy(data, line_delimiter="\n"))
    assert result == expected


def test_lines_split_lazy_with_empty_string() -> None:
    lexer = Lexer(delimiter=",")
    data = ""
    expected = [""]
    result = list(lexer.lines_split_lazy(data, line_delimiter="\n"))
    assert result == expected


def test_lines_split_lazy_with_delimiter_at_end() -> None:
    lexer = Lexer(delimiter=",")
    data = "line1\nline2\nline3\n"
    expected = ["line1", "line2", "line3", ""]
    result = list(lexer.lines_split_lazy(data, line_delimiter="\n"))
    assert result == expected


def test_lines_split_lazy_with_delimiter_at_start() -> None:
    lexer = Lexer(delimiter=",")
    data = "\nline1\nline2\nline3"
    expected = ["", "line1", "line2", "line3"]
    result = list(lexer.lines_split_lazy(data, line_delimiter="\n"))
    assert result == expected


# LexerInterface tests 100%


class TestableLexer(LexerInterface):
    def tokenize(self, data: str):  # type: ignore
        return super().tokenize(data)  # type: ignore

    def lines_split_lazy(self, full_string: str, line_delimiter: str):  # type: ignore
        return super().lines_split_lazy(full_string, line_delimiter)  # type: ignore


def test_lexer_methods_not_implemented() -> None:
    lexer = TestableLexer()
    with pytest.raises(NotImplementedError):
        lexer.tokenize("data")
    with pytest.raises(NotImplementedError):
        next(lexer.lines_split_lazy("data", "\n"))
