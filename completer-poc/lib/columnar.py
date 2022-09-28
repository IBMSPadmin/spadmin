import io
import os
from . import globals

from typing import (
    Union,
    Sequence,
    List,
    Any,
)


def clen(text):
    length = 0
    kikapcs = False

    for char in text:

        if char == '\x1b':
            kikapcs = True
            continue

        if kikapcs and char == 'm':
            kikapcs = False
            continue

        if kikapcs:
            continue

        length += 1

    return length


def get_column_length(headers, data):
    column_length = []
    for cell in headers:
        column_length.append(clen(str(cell)))

    for row in data:
        for i, cell in enumerate(row):
            if column_length[i] < clen(str(cell)):
                column_length[i] = clen(str(cell))

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
        # Header 1st decorator line --------
        for i, cell in enumerate(headers):
            out.write(self.header_decorator * self.column_length[i] + self.column_separator)
        out.write("\n")

        # Header
        for i, cell in enumerate(headers):
            out.write(self.get_justified_cell_text(i, cell) + self.column_separator)
        out.write("\n")

        # Header 2nd decorator line --------
        for i, cell in enumerate(headers):
            out.write(self.header_decorator * self.column_length[i] + self.column_separator)
        out.write("\n")

        # Rows
        for row in data:  # sorok kiíratása
            for i, cell in enumerate(row):  # cellák kiíratása
                lenght_of_row = sum((lambda x: [len(i) for i in x])(row)) + len(self.column_length) - 1
                if (i + 1) == len(row) and globals.columns < lenght_of_row:
                    cut = lenght_of_row - globals.columns
                    out.write(self.get_justified_cell_text(i, cell)[:-cut])
                else:
                    out.write(self.get_justified_cell_text(i, cell) + " ")
            out.write("\n")
        return out.getvalue()[:-1]

    def colorcutter(text, width, textfiller):

        lastcolor = ''
        savedlastcolor = ''
        counter = 1
        ret = ''
        for char in text:

            ret += char

            # collect and save the last color sequence
            if char == '\x1b' or lastcolor != '':
                if char == 'm':
                    if lastcolor == '\x1b[0':
                        savedlastcolor = ''
                    else:
                        savedlastcolor += lastcolor + 'm'
                    lastcolor = ''
                else:
                    lastcolor += char
                continue

            # reach the width
            if counter == width:
                ret += '\x1b[0m' + textfiller
                counter = 0
                if savedlastcolor != '':
                    ret += savedlastcolor
                    counter = counter

            counter += 1

        return ret

    def get_justified_cell_text(self, i, cell):

        spacer = ' ' * (self.column_length[i] - clen(str(cell)))
        left, right = spacer[:len(spacer) // 2], spacer[len(spacer) // 2:]

        if self.justify[i] and self.justify[i] == 'l':
            return str(cell) + spacer
        elif self.justify[i] and self.justify[i] == 'c':
            return left + str(cell) + right
        else:
            return spacer + str(cell)
