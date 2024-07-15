import pytest
from processor_py.lexer import tokenize, lines_split_lazy


def test_tokenize() -> None:
    assert tokenize("a,b,c", ",") == ["a", "b", "c"]
    assert tokenize("a,b,c", ";") == ["a,b,c"]
    assert tokenize("a;b;c", ";") == ["a", "b", "c"]
    assert tokenize("", ",") == [""]

    with pytest.raises(ValueError, match="Delimiter cannot be an empty string"):
        tokenize("a,b,c", "")

    with pytest.raises(AttributeError):
        tokenize(None, ",")


def test_lines_split_lazy() -> None:
    result = list(lines_split_lazy("a\nb\nc"))
    assert result == ["a", "b", "c"]

    result = list(lines_split_lazy("a\nb\nc\n"))
    assert result == ["a", "b", "c", ""]

    result = list(lines_split_lazy("a\n\nb\nc"))
    assert result == ["a", "", "b", "c"]

    result = list(lines_split_lazy("abc", ","))
    assert result == ["abc"]

    result = list(lines_split_lazy("", "\n"))
    assert result == [""]

    with pytest.raises(TypeError):
        list(lines_split_lazy(None, "\n"))
