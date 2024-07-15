from typing import Dict


def stringify_line(line_map: Dict[int, str]) -> str:
    column_indexes = sorted(list(line_map.keys()))
    sorted_columns = [
        line_map.get(column_index, "")
        for column_index in column_indexes
        if line_map.get(column_index)
    ]

    return ",".join(sorted_columns)
