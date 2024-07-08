from unittest.mock import Mock, MagicMock
from typing import Callable
from processor.ingestor.ingestor import Ingestor
from processor.transformer.transformer_strategy import CSVTransformedDataDTO


def test_ingestor_transform_file_data_lazy_success(
    open_file_stub: Callable[[str], Mock],
    mock_csv_transformer: MagicMock,
) -> None:
    file_content = "header1,header2\ndata1,data2\ndata3,data4\n"
    mock_open = open_file_stub(file_content)

    expected_result = CSVTransformedDataDTO(
        ["header1", "header2"], iter([["data1", "data2"], ["data3", "data4"]])
    )

    mock_csv_transformer.file_transform_lazy.return_value = expected_result
    ingestor: Ingestor[CSVTransformedDataDTO] = Ingestor(mock_csv_transformer)

    result = ingestor.transform_file_data_lazy("data.csv")

    mock_open.assert_called_once_with("data.csv", "r")
    file_handle = mock_open.return_value
    mock_csv_transformer.file_transform_lazy.assert_called_once_with(file_handle)

    assert mock_open.call_count == 1

    assert result.headers == expected_result.headers
    assert list(result.rows) == list([["data1", "data2"], ["data3", "data4"]])


def test_ingestor_read_data_in_memory_success(
    mock_csv_transformer: MagicMock,
) -> None:
    data_content = "header1,header2\ndata1,data2\ndata3,data4\n"

    expected_result = CSVTransformedDataDTO(
        ["header1", "header2"], iter([["data1", "data2"], ["data3", "data4"]])
    )

    mock_csv_transformer.data_transform_lazy.return_value = expected_result
    ingestor: Ingestor[CSVTransformedDataDTO] = Ingestor(mock_csv_transformer)

    result = ingestor.read_data_in_memory(data_content)

    mock_csv_transformer.data_transform_lazy.assert_called_once_with(data_content)

    assert result.headers == expected_result.headers
    assert list(result.rows) == list([["data1", "data2"], ["data3", "data4"]])
