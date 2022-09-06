import os
import sys
import globals

from termcolor import colored
from re import search, IGNORECASE


def refreshrowscolumns():
    row, column = os.popen( 'stty size', 'r' ).read().split()
    globals.rows    = int( row )
    globals.columns = int( column )


def progressbar( count, total, leadtext = '' ):
    barlength = globals.columns - 2 - len( leadtext )  # [...]
    filledlength = int(round((barlength) * count / float(total)))

    percent = round(100.0 * count / float(total), 1)
    barline = '=' * filledlength + colored('-', 'grey', attrs=['bold']) * (barlength - filledlength)

    sys.stdout.write( leadtext + '[%s]\r' % (barline))
    sys.stdout.write( leadtext + '[%s%s\r' % (colored(percent, 'grey', 'on_white'), colored('%', 'grey', 'on_white')))
    sys.stdout.flush()


def consoleline( char='-'):
    print(char * globals.columns)


def consolefilledline(left = '', pattern = '-', right = '', width = 120):
    patternwith = width - len(left) - len(right) - 2
    return left + ' ' + pattern * patternwith + ' ' + right


def ruler( self, parameters ):
    if parameters == None or parameters == '' or parameters == []:
        ruler100()
        ruler10()
        ruler1()
    else:    
        if search ( regexpgenerator('Help'), parameters[0], IGNORECASE ):
            print( 'SHow Ruler Help message!' )
        elif search ( regexpgenerator('INVerse'), parameters[0], IGNORECASE ):
            ruler1()    
            ruler10()
            ruler100()
            

def ruler100():
    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 100:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 100 else cc
    print()


def ruler10():
    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 10:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 10 else cc
    print()

    
def ruler1():
    for i in range( 1, globals.columns + 1, 1 ):
        c = i % 10
        if c:
            sys.stdout.write( str( c ) )
        else:
            sys.stdout.write( colored( str( c ), 'green' ) )    

def regexpgenerator(regexp):
            
    savelastchar = ''
    if regexp[-1] == '=':
        savelastchar = regexp[-1]
        regexp = regexp[: -1]
    
    result = ''
    for part in regexp.split():
    
        if part[0].isupper():
    
            tmpregexp = part
            tmpstring = part
            for x in part:
                if tmpstring[-1].isupper():
                    break
                tmpstring = part[0: len(tmpstring) - 1]
                tmpregexp += '|' + tmpstring
    
            result += '(' + tmpregexp + ')'
    
        else:
            result += '(' + part + ')'
    
        result += '\s+'
    
    return result[:-3] + savelastchar


def dictmerger( destination, source ):
    for key in source:
        if key not in destination:
             destination[ key ] = []
        destination[ key ].extend( source [ key ] )