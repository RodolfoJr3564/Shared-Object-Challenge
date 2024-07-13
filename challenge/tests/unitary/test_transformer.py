from typing import Callable, TextIO
from unittest.mock import Mock, MagicMock
import pytest
from pytest_mock import MockerFixture
from processor.transformer.transformer import Transformer, TransformerFactory
from processor.transformer.transformer_strategy import (
    CSVTransformedDataDTO,
    TransformStrategy,
)


@pytest.fixture
def csv_transformer(
    mocker: MockerFixture,
) -> Callable[[str], Transformer[CSVTransformedDataDTO]]:
    """Fixture for creating a mocked CSV Transformer instance."""

    def _csv_transformer(delimiter: str) -> Transformer[CSVTransformedDataDTO]:
        mock_transformer: MagicMock = mocker.create_autospec(Transformer, instance=True)
        mock_transformer.file_transform_lazy.return_value = CSVTransformedDataDTO(
            headers=["header1", "header2"],
            rows=iter([["data1", "data2"], ["data3", "data4"]]),
        )
        return mock_transformer

    return _csv_transformer


def test_transformer_transform_success(
    open_file_stub: Callable[[str], Mock],
    csv_transformer: Callable[[str], Transformer[CSVTransformedDataDTO]],
) -> None:
    csv_content = "header1,header2\ndata1,data2\ndata3,data4\n"
    open_file_stub(csv_content)
    transformer = csv_transformer(",")
    result = transformer.file_transform_lazy(open("data.csv", "r"))

    headers = result.headers
    rows = list(result.rows)

    assert headers == ["header1", "header2"]
    assert rows == [["data1", "data2"], ["data3", "data4"]]


def test_transformer_file_transform_lazy() -> None:
    mock_strategy = Mock(spec=TransformStrategy)
    mock_strategy.file_transform_lazy.return_value = CSVTransformedDataDTO(
        headers=["header1", "header2"],
        rows=iter([["data1", "data2"], ["data3", "data4"]]),
    )

    transformer: Transformer[CSVTransformedDataDTO] = Transformer(mock_strategy)

    mock_file = Mock(spec=TextIO)

    result = transformer.file_transform_lazy(mock_file)

    assert result.headers == ["header1", "header2"]
    assert list(result.rows) == [["data1", "data2"], ["data3", "data4"]]
    mock_strategy.file_transform_lazy.assert_called_once_with(mock_file)


def test_transformer_data_transform_lazy() -> None:
    mock_strategy = Mock(spec=TransformStrategy)
    mock_strategy.data_transform_lazy.return_value = CSVTransformedDataDTO(
        headers=["header1", "header2"],
        rows=iter([["data1", "data2"], ["data3", "data4"]]),
    )

    transformer: Transformer[CSVTransformedDataDTO] = Transformer(mock_strategy)

    data = "header1,header2\ndata1,data2\ndata3,data4\n"
    result = transformer.data_transform_lazy(data)

    assert result.headers == ["header1", "header2"]
    assert list(result.rows) == [["data1", "data2"], ["data3", "data4"]]
    mock_strategy.data_transform_lazy.assert_called_once_with(data)


def test_transformer_factory_create_csv_transformer() -> None:
    line_delimiter = ","
    transformer = TransformerFactory.create_csv_transformer(line_delimiter)

    assert isinstance(transformer, Transformer)
