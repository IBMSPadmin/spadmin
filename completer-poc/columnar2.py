import io
import os

import globals

from operator import itemgetter
from typing import (
    Union,
    Sequence,
    List,
    Any,
)
import utilities


def get_column_length(headers, data):
    column_length = []
    for cell in headers:
        column_length.append(len(cell))

    for row in data:
        for i, cell in enumerate(row):
            if column_length[i] < len(cell):
                column_length[i] = len(cell)

    row, width = os.popen('stty size', 'r').read().split()
    width = int(width)
    # truncate last column if length > terminal width
    if (sum(column_length) + len(column_length)) > width:
        column_length[-1] = column_length[-1] - (
                (sum(column_length) + len(column_length)) - width)

    return column_length


class Columnar:
    def __call__(
            self,
            data: Sequence[Sequence[Any]],
            headers: Union[None, Sequence[Any]] = None,
            justify: Union[str, List[str]] = "l",
    ) -> str:
        self.justify = justify
        self.column_separator = " "  # lenght of separator should be 1 char.
        self.header_decorator = "-"  # lenght of decorator should be 1 char.
        out = io.StringIO()

        self.column_length = get_column_length(headers, data)

        # Header 1st line --------
        for i, cell in enumerate(headers):
            out.write(self.header_decorator * self.column_length[i] + self.column_separator)
        out.write("\n")

        # Header
        for i, cell in enumerate(headers):
            out.write(self.get_justified_cell_text(i, cell) + self.column_separator)
        out.write("\n")

        # Header 2nd line --------
        for i, cell in enumerate(headers):
            out.write(self.header_decorator * self.column_length[i] + self.column_separator)
        out.write("\n")

        # Rows
        for row in data:
            for i, cell in enumerate(row):
                out.write(self.get_justified_cell_text(i, cell) + " ")
            out.write("\n")

        return out.getvalue()

    def get_justified_cell_text(self, i, cell):
        if self.justify[i] and self.justify[i] == 'l':
            return cell[0:self.column_length[i]].ljust(self.column_length[i])
        else:
            return cell[0:self.column_length[i]].rjust(self.column_length[i])
