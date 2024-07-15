import pytest
from unittest.mock import Mock
from processor.processor.processor import Processor, ProcessedLazyDataDTO
from processor.processor.filter import Filter
from processor.transformer.transformer_strategy import CSVTransformedDataDTO


@pytest.fixture
def csv_transformed_data_DTO() -> CSVTransformedDataDTO:
    headers = ["header1", "header2"]
    rows = iter([["data1", "data2"], ["data3", "data4"], ["data5", "data6"]])
    return CSVTransformedDataDTO(headers=headers, rows=rows)


@pytest.fixture
def mock_filter() -> Filter:
    filter_instance = Mock(spec=Filter)
    filter_instance.is_satisfied_by.side_effect = lambda row: row == [
        "data3",
        "data4",
    ]
    return filter_instance


def test_processed_lazy_data_DTO_initialization() -> None:
    headers = ["header1", "header2"]
    rows = iter([["data1", "data2"], ["data3", "data4"]])
    processed_data = ProcessedLazyDataDTO(headers, rows)

    assert processed_data.headers == headers
    assert list(processed_data.rows) == [["data1", "data2"], ["data3", "data4"]]


def test_processor_build_lazy(
    csv_transformed_data_DTO: CSVTransformedDataDTO, mock_filter: Filter
) -> None:
    processor = Processor(
        transformed_lazy_data_DTO=csv_transformed_data_DTO,
        entryComparisonMatcher=mock_filter,
    )
    processed_data = processor.build_lazy()

    assert processed_data.headers == csv_transformed_data_DTO.headers
    assert list(processed_data.rows) == [["data3", "data4"]]


def test_processor_no_rows_satisfied(
    csv_transformed_data_DTO: CSVTransformedDataDTO,
) -> None:
    mock_filter = Mock(spec=Filter)
    mock_filter.is_satisfied_by.return_value = False

    processor = Processor(
        transformed_lazy_data_DTO=csv_transformed_data_DTO,
        entryComparisonMatcher=mock_filter,
    )
    processed_data = processor.build_lazy()

    assert processed_data.headers == csv_transformed_data_DTO.headers
    assert list(processed_data.rows) == []


def test_processor_all_rows_satisfied(
    csv_transformed_data_DTO: CSVTransformedDataDTO,
) -> None:
    mock_filter = Mock(spec=Filter)
    mock_filter.is_satisfied_by.return_value = True

    processor = Processor(
        transformed_lazy_data_DTO=csv_transformed_data_DTO,
        entryComparisonMatcher=mock_filter,
    )
    processed_data = processor.build_lazy()

    assert processed_data.headers == csv_transformed_data_DTO.headers
    assert list(processed_data.rows) == [
        ["data1", "data2"],
        ["data3", "data4"],
        ["data5", "data6"],
    ]
