import pytest
from unittest.mock import MagicMock
from pytest_mock import MockerFixture
from processor.processor.filter import Filter
from processor.processor.processor import Processor
from processor.serializer.serializer import Serializer
from processor.transformer.transformer import Transformer
from typing import Callable, List, Dict


@pytest.fixture
def mock_transformer(mocker: MockerFixture) -> MagicMock:
    return mocker.create_autospec(Transformer, instance=True)


@pytest.fixture
def mock_processor(mocker: MockerFixture) -> MagicMock:
    processor = mocker.create_autospec(Processor, instance=True)
    processor.build_lazy.return_value = processor
    return processor


@pytest.fixture
def mock_serializer(mocker: MockerFixture) -> MagicMock:
    serializer = mocker.create_autospec(Serializer, instance=True)
    serializer.stringify.return_value = "header1\n3\n"
    return serializer


@pytest.fixture
def mock_filter(mocker: MockerFixture) -> MagicMock:
    return mocker.create_autospec(Filter, instance=True)


@pytest.fixture
def transformer_factory(
    mocker: MockerFixture, mock_transformer: MagicMock
) -> MagicMock:
    return mocker.patch(
        "processor.transformer.transformer.TransformerFactory.create_csv_transformer",
        return_value=mock_transformer,
    )


@pytest.fixture
def open_file_stub(mocker: MockerFixture) -> Callable[[str], MagicMock]:
    def _open_file_stub(file_content: str) -> MagicMock:
        mock_open: MagicMock = mocker.mock_open(read_data=file_content)
        mocker.patch("builtins.open", mock_open)
        return mock_open

    return _open_file_stub


@pytest.fixture
def mock_lexer(mocker: MockerFixture) -> MagicMock:
    mock_lexer = mocker.patch("processor.serializer.serializer.Lexer")
    instance: MagicMock = mock_lexer.return_value
    instance.tokenize.side_effect = lambda x: x.split(",")
    return instance


@pytest.fixture
def headers() -> Dict[str, List[str]]:
    return {
        "single_header": ["header1"],
        "many_headers": ["header1", "header2", "header3", "header4"],
    }


@pytest.fixture
def valid_filters() -> Dict[str, str]:
    return {
        "single_param_filter": "header1=10",
        "many_filter_params": "header1=10\nheader2>20\nheader3<=30\nheader4!=40",
        "comma_in_filter": 'header1="val,ue"\nheader2>20',
    }


@pytest.fixture
def invalid_filters() -> Dict[str, str]:
    return {
        "invalid_operator_filter": "header1#2",
        "nonexistent_column_filter": "header6=10",
    }


@pytest.fixture
def valid_rows() -> Dict[str, List[str]]:
    return {
        "single_item_row": ["10"],
        "many_item_row": ["10", "20", "30", "40"],
        "comma_item_row": ['"val,ue"', "21", "30"],
    }


@pytest.fixture
def invalid_rows() -> Dict[str, List[str]]:
    return {
        "single_item_invalid_row": ["5"],
        "many_item_invalid_row": ["5", "15", "25", "35"],
        "comma_item_invalid_row": ['"val,ue"', "19", "30"],
    }
