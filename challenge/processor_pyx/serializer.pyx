from typing import Dict
import cython

@cython.cfunc
def stringify_line(line_map: Dict[int, str]) -> str:
    cdef list column_indexes = sorted(list(line_map.keys()))
    cdef list sorted_columns = [
        line_map[column_index]
        for column_index in column_indexes
        if line_map.get(column_index)
    ]

    return ",".join(sorted_columns)