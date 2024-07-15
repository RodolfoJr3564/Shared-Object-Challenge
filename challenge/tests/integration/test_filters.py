import pytest
from pathlib import Path
from _pytest.capture import CaptureFixture
from unittest.mock import MagicMock, patch, mock_open
from processor_py.processor import process_csv_file

mock_csv_data = "name,age,experience\nAlice,30,5\nBob,25,3\nCharlie,35,10"
mock_csv_data_with_extra = (
    "name,age,experience,education\n"
    "Alice,30,5,Bachelor\n"
    "Bob,25,3,Master\n"
    "Charlie,35,10,PhD"
)
mock_csv_data_special_chars = (
    "na\"me,'a@ge',ex\"'per@i\"'ence\n" "Alice,30,5\n" "Bob,25,3\n" "Charlie,35,10"
)


@pytest.fixture
def csv_file(tmpdir: Path) -> Path:
    file_path: Path = tmpdir / "test.csv"
    return file_path


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_greater_than(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "age>29"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Charlie" in out
    assert "Bob" not in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_with_multiple_comparative_operators(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "age>=30\nexperience<=5"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Charlie" not in out
    assert "Bob" not in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data_special_chars)
def test_csv_filter_ignore_special_characters(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = 'na"me'
    row_filter_definitions = "'a@ge'>29\nex\"'per@i\"'ence<10"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Bob" not in out
    assert "Charlie" not in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_non_existent_column_error_logging(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "height>60"
    with pytest.raises(SystemExit):
        process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, err = capfd.readouterr()
    assert "Header 'height' not found in CSV file/string" in err


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_invalid_filter_error_logging(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "age#25"
    with pytest.raises(SystemExit):
        process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, err = capfd.readouterr()
    assert "Invalid filter: 'age#25'" in err


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_order_independence(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "experience>4\nage<35"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Bob" not in out
    assert "Charlie" not in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data_with_extra)
def test_csv_filter_with_multiple_filters_same_column(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "age>20\nage<35"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Bob" in out
    assert "Charlie" not in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_csv_filter_with_AND_logic(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name"
    row_filter_definitions = "age>25\nexperience>3"
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "Alice" in out
    assert "Bob" not in out
    assert "Charlie" in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_non_existent_columns_in_selection_string(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = "name,nonexistent"
    row_filter_definitions = ""
    with pytest.raises(SystemExit):
        process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    _, err = capfd.readouterr()
    assert "Header 'nonexistent' not found in CSV file/string" in err
