import sys
import globals

from termcolor import colored


def progressbar(count, total):
    barlength = globals.columns - 2  # [...]
    filledlength = int(round((barlength) * count / float(total)))

    percent = round(100.0 * count / float(total), 1)
    barline = '=' * filledlength + colored('-', 'grey', attrs=['bold']) * (barlength - filledlength)

    sys.stdout.write('[%s]\r' % (barline))
    sys.stdout.write('[%s%s\r' % (colored(percent, 'grey', 'on_white'), colored('%', 'grey', 'on_white')))
    sys.stdout.flush()


def consoleline( char='-'):
    print(char * globals.columns)


def consolefilledline(left='', pattern='-', right='', width=80):
    patternwith = width - len(left) - len(right) - 2
    return left + ' ' + pattern * patternwith + ' ' + right




def ruler():
    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 100:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 100 else cc
    print()

    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 10:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 10 else cc
    print()

    for i in range( 1, globals.columns + 1, 1 ):
        c = i % 10
        if c:
            sys.stdout.write( str( c ) )
        else:
            sys.stdout.write( colored( str( c ), 'green' ) )
