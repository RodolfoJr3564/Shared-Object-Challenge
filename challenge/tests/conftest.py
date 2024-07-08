from typing import Callable
from processor.transformer.transformer import Transformer
from processor.transformer.transformer_strategy import (
    CSVTransformedDataDTO,
    CsvTransformStrategy,
)
import io

import pytest
from unittest.mock import Mock
from pytest_mock import MockerFixture


@pytest.fixture
def open_file_stub(mocker: MockerFixture) -> Callable[[str], Mock]:
    def _open_file_stub(file_content: str) -> Mock:
        mock_file = io.StringIO(file_content)
        mock_open = mocker.patch("builtins.open", return_value=mock_file)
        return mock_open

    return _open_file_stub


@pytest.fixture
def csv_transformer() -> Callable[[str], Transformer[CSVTransformedDataDTO]]:
    def _csv_transformer(
        line_delimiter: str = ",",
    ) -> Transformer[CSVTransformedDataDTO]:
        csv_transform_strategy = CsvTransformStrategy(line_delimiter=line_delimiter)
        transformer: Transformer[CSVTransformedDataDTO] = Transformer(
            csv_transform_strategy
        )
        return transformer

    return _csv_transformer


@pytest.fixture
def mock_csv_transformer(
    mocker: MockerFixture,
) -> Mock:
    mock_transformer = mocker.create_autospec(Transformer)
    return mock_transformer
