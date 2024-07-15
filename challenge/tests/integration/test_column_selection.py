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
def test_selection_of_columns_based_on_string(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns: str = "name,experience"
    row_filter_definitions: str = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "name,experience" in out
    assert "Alice,5" in out
    assert "Bob,3" in out
    assert "Charlie,10" in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_empty_selection_string_selects_all_columns(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns: str = ""
    row_filter_definitions: str = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "name,age,experience" in out
    assert "Alice,30,5" in out
    assert "Bob,25,3" in out
    assert "Charlie,35,10" in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_non_existent_columns_in_selection_string(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns: str = "name,nonexistent"
    row_filter_definitions: str = ""
    with pytest.raises(SystemExit):
        process_csv_file(str(csv_file), selected_columns, row_filter_definitions)

    _, err = capfd.readouterr()

    assert "Header 'nonexistent' not found in CSV file/string" == err


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_selection_string_with_columns_in_arbitrary_order(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns: str = "experience,name"
    row_filter_definitions: str = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()

    assert "name,experience" in out
    assert "Alice,5" in out
    assert "Bob,3" in out
    assert "Charlie,10" in out


@patch("builtins.open", new_callable=mock_open, read_data=mock_csv_data)
def test_non_existent_columns_in_filters(
    _mock_file: MagicMock, capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns: str = "name"
    row_filter_definitions: str = "nonexistent=10"
    with pytest.raises(SystemExit):
        process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    _, err = capfd.readouterr()
    assert "Header 'nonexistent' not found in CSV file/string" == err
