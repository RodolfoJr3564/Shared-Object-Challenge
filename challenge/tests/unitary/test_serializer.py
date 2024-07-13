import pytest
from processor.serializer.serializer import Serializer
from processor.processor.processor import ProcessedLazyDataDTO
from unittest.mock import MagicMock


@pytest.fixture
def processed_lazy_data_dto() -> ProcessedLazyDataDTO:
    return ProcessedLazyDataDTO(
        headers=["header1", "header2"], rows=iter([["10", "20"], ["30", "40"]])
    )


def test_serializer_initialization(
    processed_lazy_data_dto: ProcessedLazyDataDTO,
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    assert serializer.data == processed_lazy_data_dto


def test_serializer_stringify_all_columns(
    processed_lazy_data_dto: ProcessedLazyDataDTO,
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    result = serializer.stringify("")
    expected = "header1,header2\n10,20\n30,40\n"
    assert result == expected


def test_serializer_stringify_single_column(
    processed_lazy_data_dto: ProcessedLazyDataDTO, mock_lexer: MagicMock
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    mock_lexer.tokenize.return_value = ["header1"]
    result = serializer.stringify("header1")
    expected = "header1\n10\n30\n"
    assert result == expected


def test_serializer_stringify_multiple_columns(
    processed_lazy_data_dto: ProcessedLazyDataDTO, mock_lexer: MagicMock
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    mock_lexer.tokenize.return_value = ["header1", "header2"]
    result = serializer.stringify("header1,header2")
    expected = "header1,header2\n10,20\n30,40\n"
    assert result == expected


def test_serializer_stringify_invalid_column(
    processed_lazy_data_dto: ProcessedLazyDataDTO, mock_lexer: MagicMock
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    mock_lexer.tokenize.return_value = ["header3"]
    with pytest.raises(
        ValueError, match="Invalid column specified: 'header3' is not in list"
    ):
        serializer.stringify("header3")


def test_serializer_stringify_empty_column(
    processed_lazy_data_dto: ProcessedLazyDataDTO, mock_lexer: MagicMock
) -> None:
    serializer = Serializer(data=processed_lazy_data_dto)
    mock_lexer.tokenize.return_value = [""]
    result = serializer.stringify("")
    expected = "header1,header2\n10,20\n30,40\n"
    assert result == expected
