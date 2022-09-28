import io
import os

from typing import (
    Union,
    Sequence,
    List,
    Any,
)


def clen( text ):

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

    row, width = os.popen('stty size', 'r').read().split()
    width = int(width)
    # truncate last column if length > terminal width
    if (sum(column_length) + clen(column_length)) > width:
        column_length[-1] = column_length[-1] - (
                (sum(column_length) + clen(column_length)) - width)

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
        for row in data:
            for i, cell in enumerate(row):
                out.write(self.get_justified_cell_text(i, cell) + " ")
            out.write("\n")

        return out.getvalue()

    # def get_justified_cell_text(self, i, cell):
    #     if self.justify[i] and self.justify[i] == 'l':
    #         return str(cell)[0:self.column_length[i]].ljust(self.column_length[i])
    #     else:
    #         return str(cell)[0:self.column_length[i]].rjust(self.column_length[i])
    
    def get_justified_cell_text( self, i, cell ):
        
        spacer = ' ' * ( self.column_length[ i ] - clen( str( cell ) ) )
        left, right = spacer [ :len( spacer ) // 2 ], spacer [ len( spacer ) // 2: ]
        
        if self.justify[ i ] and self.justify[ i ] == 'l':
            return str( cell ) + spacer 
        elif self.justify[ i ] and self.justify[ i ] == 'c':
            return left + str( cell ) + right
        else:
            return spacer + str( cell )
