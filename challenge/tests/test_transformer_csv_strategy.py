import pytest
from unittest.mock import mock_open, patch, Mock

from typing import Callable, TextIO
import io
from pytest_mock import MockerFixture
from processor.transformer.transformer_strategy import (
    CSVTransformedDataDTO,
    CsvTransformStrategy,
    TransformStrategy,
)


def test_csv_transform_strategy_file_transform_lazy(
    open_file_stub: Callable[[str], None]
) -> None:
    mock_file_content = "header1,header2\n" + "data1_1,data1_2\n" + "data2_1,data2_2\n"

    mock_file = mock_open(read_data=mock_file_content)
    with patch("builtins.open", mock_file):
        with open("mock_file.csv", "r") as f:
            strategy = CsvTransformStrategy(line_delimiter=",")
            result = strategy.file_transform_lazy(f)

    assert result.headers == ["header1", "header2"]
    assert list(result.rows) == [["data1_1", "data1_2"], ["data2_1", "data2_2"]]


def test_csv_transform_strategy_data_transform_lazy() -> None:
    data = "header1,header2\ndata1_1,data1_2\ndata2_1,data2_2\n"
    strategy = CsvTransformStrategy(line_delimiter=",")
    result = strategy.data_transform_lazy(data)

    assert result.headers == ["header1", "header2"]
    assert list(result.rows) == [
        [
            "data1_1",
            "data1_2",
        ],
        ["data2_1", "data2_2"],
        [""],
    ]


class IncompleteTransformStrategy(TransformStrategy[CSVTransformedDataDTO]):
    def file_transform_lazy(self, file: TextIO) -> CSVTransformedDataDTO:
        return super().file_transform_lazy(file)  # type: ignore

    def data_transform_lazy(self, data: str) -> CSVTransformedDataDTO:
        return super().data_transform_lazy(data)  # type: ignore


def test_transform_strategy_methods_raise_not_implemented_error() -> None:
    strategy = IncompleteTransformStrategy()

    with pytest.raises(NotImplementedError):
        strategy.file_transform_lazy(Mock(spec=TextIO))

    with pytest.raises(NotImplementedError):
        strategy.data_transform_lazy("some data")


@pytest.fixture
def open_file_stub(mocker: MockerFixture) -> Callable[[str], Mock]:
    def _open_file_stub(file_content: str) -> Mock:
        mock_file = io.StringIO(file_content)
        mock_open = mocker.patch("builtins.open", return_value=mock_file)
        return mock_open

    return _open_file_stub
