import io
import re
from operator import itemgetter

from . import globals
from colorama import Fore, Back, Style
from typing import (
    Union,
    Sequence,
    List,
    Any,
)
from termcolor import colored


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


def colorize( text: str, regexp: str, color: str, attrs=[] ):
    
        text = str( text ) # FIX: "TypeError: expected string or bytes-like object"
        match = re.search( regexp, text )
        
        if match:
            before = text[0:match.start()]
            # print(repr(before))
            # last_colors = re.findall("(\x1b\[.+?m)", before)
            last_colors = re.findall( "(\x1b\[.+?m|\x1b\[1m\x1b\[.+?m)", before )
            found_last_color = ''
            if last_colors:
                if len( last_colors ) > 1  and last_colors[ -2 ] == '\x1b[1m':
                    found_last_color = last_colors[ -2 ] + last_colors[ -1 ]
                else:
                     found_last_color = last_colors[ -1 ]
            return text.replace(match[0], colored(match[0], color, attrs=attrs ) + found_last_color)
        else:
            return text
    

def grep(data):
    grep = globals.extras['grep'] if 'grep' in globals.extras else ''
    grep_data = []
    if grep != '' and grep is not None:
        for i, row in enumerate(data):
            found = False
            for c, cell in enumerate(row):
                finds = re.findall(grep, str(cell))
                if len(finds) > 0:
                    found = True
                    for find in finds:
                        # data[i][c] = str(cell).replace(find, Fore.GREEN + find + Style.RESET_ALL)
                        data[i][c] = colorize( cell, find, 'white', [ 'bold' ] )
            if found is True:
                grep_data.append(row)
    else:
        grep_data = data

    return grep_data


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

        orderby = globals.extras['orderby'] if 'orderby' in globals.extras else ''
        if orderby != '' and orderby is not None and orderby.isnumeric() and int(orderby) < len(data[0]):
            data = sorted(data, key=itemgetter(int(orderby)), reverse=False)
#            headers[int(orderby)] = colored(headers[int(orderby)], "green", attrs=[ 'bold' ])
            headers[int(orderby)] = colored(headers[int(orderby)], "green", attrs=[ 'bold' ]) + Fore.WHITE + Style.BRIGHT

        # Grep
        data = grep(data)

        self.column_length = get_column_length(headers, data)
        header_decorator = ""
        for i, cell in enumerate(headers):
            header_decorator += self.header_decorator * self.column_length[i] + self.column_separator

        # Header 1st decorator line --------
        out.write( colored( header_decorator[:globals.columns], 'white', attrs=[ 'bold' ] ) + "\n")

        # Header
        header_line = ""
        for i, cell in enumerate(headers):
            header_line += self.get_justified_cell_text( i, cell ) + self.column_separator
        out.write( header_line[:globals.columns] + "\n")

        # Header 2nd decorator line --------
        out.write( colored( header_decorator[:globals.columns], 'white', attrs=[ 'bold' ] ) + "\n")

        # Rows
        for row in data:  # sorok kiíratása
            for i, cell in enumerate(row):  # cellák kiíratása

                lenght_of_row = sum(self.column_length) + clen(self.column_length) - 1
                if (i + 1) == len(row) and globals.columns < lenght_of_row:
                    restlength = globals.columns - (sum(self.column_length[:-1]) + clen(self.column_length) - 1)
                    out.write(colorcutter(cell, restlength,
                                          '\n' + ' ' * (sum(self.column_length[:-1]) + clen(self.column_length) - 1)))
                else:
                    out.write(self.get_justified_cell_text(i, cell) + " ")
            out.write("\n")
        return out.getvalue()[:-1]

    def get_justified_cell_text(self, i, cell):

        spacer = ' ' * (self.column_length[i] - clen(str(cell)))
        left, right = spacer[:len(spacer) // 2], spacer[len(spacer) // 2:]

        if self.justify[i] and self.justify[i] == 'l':
            return str(cell) + spacer
        elif self.justify[i] and self.justify[i] == 'c':
            return left + str(cell) + right
        else:
            return spacer + str(cell)
