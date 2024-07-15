import pytest
from pathlib import Path
from processor_py.processor import process_csv_file

from _pytest.capture import CaptureFixture


@pytest.fixture
def csv_file() -> Path:
    return (Path(__file__).parent.parent / "mocks" / "mock.csv").resolve()


def test_csv_with_256_columns(capfd: CaptureFixture[str], csv_file: Path) -> None:
    selected_columns = "col1,col256"
    row_filter_definitions = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "data" in out


def test_lexicographic_order(capfd: CaptureFixture[str], csv_file: Path) -> None:
    selected_columns = "col1,col2"
    row_filter_definitions = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    lines = out.splitlines()
    data_lines = lines[1:]
    assert data_lines == sorted(data_lines)


def test_performance_with_extra_columns(
    capfd: CaptureFixture[str], csv_file: Path
) -> None:
    selected_columns = ",".join([f"col{i}" for i in range(1, 257)])
    row_filter_definitions = ""
    process_csv_file(str(csv_file), selected_columns, row_filter_definitions)
    out, _ = capfd.readouterr()
    assert "data" in out
