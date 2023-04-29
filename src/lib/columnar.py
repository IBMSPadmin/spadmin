import io
import re
from operator import itemgetter
from . import utilities
from . import globals

from typing import (
    Union,
    Sequence,
    List,
    Any,
)
# from termcolor import colored


def grep(data):
    # print ("----------- ", data, "-------------")
    grep = globals.extras['grep'] if 'grep' in globals.extras else ''
    
    if grep != '' and grep is not None:
        
        for g in grep:
    
            grep_data = []
            
            for i, row in enumerate(data):
                found = False
                for c, cell in enumerate(row):
                    finds = re.findall(g, str(cell), re.IGNORECASE )
                    if len(finds) > 0:
                        found = True
                        for find in finds:
                            # data[i][c] = str(cell).replace(find, Fore.GREEN + find + Style.RESET_ALL)
                            data[i][c] = colorize(cell, find, 'white', ['bold'])
                if found == True:
                    grep_data.append(row)
            # ???
            data = []
            for i in grep_data:
                data.append(i)
            
    else:
        grep_data = data
        
    # cgrep test
    data = grep_data    

    grep = globals.extras['cgrep'] if 'cgrep' in globals.extras else ''
    
    if grep != '' and grep is not None:
        
        for g in grep:
    
            grep_data = []
            
            for i, row in enumerate(data):
                found = False
                for c, cell in enumerate(row):
                    finds = re.findall(g, str(cell) )
                    if len(finds) > 0:
                        found = True
                        for find in finds:
                            # data[i][c] = str(cell).replace(find, Fore.GREEN + find + Style.RESET_ALL)
                            data[i][c] = colorize(cell, find, 'white', ['bold'])
                if found == True:
                    grep_data.append(row)
            # ???
            data = []
            for i in grep_data:
                data.append(i)
            
    else:
        grep_data = data
        
    return grep_data


def invgrep(data):
    invgrep = globals.extras['invgrep'] if 'invgrep' in globals.extras else ''
    
    if invgrep != '' and invgrep is not None:
    
        for invg in invgrep:
    
            invgrep_data = []
    
            for i, row in enumerate(data):
                found = False
                for c, cell in enumerate(row):
                    founds = re.findall(invg, str(cell))
                    if len(founds) > 0:
                        found = True
                if found == False:
                    invgrep_data.append(row)
            
                # ???        
                data = []
                for i in invgrep_data:
                    data.append(i)
                    
    else:
        invgrep_data = data

    return invgrep_data

def clen(text):
    """ text length without ANSI color sequences """

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


def colorleft( text, width ):
    """ return colored line width size without escape sequences and correct the ANSI sequence at the end """
    ansiseq = False
    counter = 1
    ret     = ''
    
    text = str( text ) # 
    
    for char in text:
    
        ret += char
        
        if char == '\x1b':
            ansiseq = True
          
        if ansiseq and char == 'm':
            ansiseq = False
            continue
        
        if ansiseq:
            continue
    
        if counter == width:
            ret = ret[ :-1 ] + '>'
            ret += '\x1b[0m'
            break
    
        counter += 1
        
    return ret

def colorcutter( text, width, textfiller ):
    lastcolor      = ''
    savedlastcolor = ''
    counter        = 1
    ret            = ''
    
    text = str( text ) # 
    
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
            
        text    = str( text )                 # FIX: "TypeError: expected string or bytes-like object"
        regexp  = regexp.replace( '[', '\[' ) # FIX: regexp vs. ANSI sequence
        match   = re.search( regexp, text )
        
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
            # return text.replace(match[0], colored(match[0], color, attrs=attrs ) + found_last_color)
            return text.replace(match[0], utilities.color(match[0], color ) + found_last_color)
        else:
            return text
    

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
        if orderby != '' and orderby is not None and orderby[-1].isnumeric() and int(orderby[-1]) < len(data[0]):
            data = sorted(data, key=itemgetter(int(orderby[-1])), reverse=False)
#            headers[int(orderby)] = colored(headers[int(orderby)], "green", attrs=[ 'bold' ])

            # headers[int(orderby)] = colored(headers[int(orderby)], "green", attrs=[ 'bold' ]) + Fore.WHITE + Style.BRIGHT
            headers[ int(orderby[-1])] = colorize( headers[int(orderby[-1])], headers[int(orderby[-1])], globals.color_green, [ globals.color_attrs_bold ] )

        # Grep
        data = invgrep( grep( data ) )

        self.column_length = get_column_length(headers, data)
        header_decorator = ""
        for i, cell in enumerate(headers):
            header_decorator += self.header_decorator * self.column_length[i] + self.column_separator

        # Header 1st decorator line --------
        # out.write( colored( header_decorator[:globals.columns], globals.color_white, attrs=[ globals.color_attrs_bold ] ) + "\n")
        out.write( utilities.color( header_decorator[:globals.columns].rstrip(), globals.color_white) + "\n")

        # Header
        header_line = ''
        for i, cell in enumerate(headers):
            
            # header_line += colored( self.get_justified_cell_text( i, cell ) + self.column_separator, globals.color_white, attrs=[ globals.color_attrs_bold ] )
            header_line += utilities.color( self.get_justified_cell_text( i, cell ) + self.column_separator, globals.color_white )

        # out.write( header_line[ :globals.columns + len( header_line ) - clen( header_line ) ] + "\n")
        out.write( colorleft( header_line, globals.columns ) + "\n" )

        # Header 2nd decorator line --------
        # out.write( colored( header_decorator[:globals.columns], globals.color_white, attrs=[ globals.color_attrs_bold ] ) + "\n")
        out.write( utilities.color( header_decorator[:globals.columns].rstrip(), globals.color_white ) + "\n")

        # Rows
        for row in data:  # sorok kiíratása
            
            line = ''
                        
            for i, cell in enumerate(row):  # cellák kiíratása
                
                lenght_of_row = sum(self.column_length) + clen(self.column_length) - 1
                if (i + 1) == len(row) and globals.columns < lenght_of_row:
                    restlength = globals.columns - (sum(self.column_length[:-1]) + len(self.column_length) - 1)
                    line += colorcutter(cell, restlength, '\n' + self.column_separator * (sum(self.column_length[:-1]) + len(self.column_length) - 1) )                               
                else:
                    if (i + 1) != len(row):
                        line += self.get_justified_cell_text(i, cell) + self.column_separator
                    else:
                        line += self.get_justified_cell_text(i, cell)
                
            line = line.rstrip()
                    
            if globals.columns - (sum(self.column_length[:-1]) + len(self.column_length) - 1) < 0:
                out.write( colorleft( line, globals.columns ) + '\n' )
            else:
                out.write( line + '\n' )
            
        return out.getvalue()[ :-1 ]

    def get_justified_cell_text(self, i, cell):

        spacer = ' ' * (self.column_length[i] - clen(str(cell)))
        left, right = spacer[:len(spacer) // 2], spacer[len(spacer) // 2:]

        if self.justify[i] and self.justify[i] == 'l':
            return str(cell) + spacer
        elif self.justify[i] and self.justify[i] == 'c':
            return left + str(cell) + right
        else:
            return spacer + str(cell)
