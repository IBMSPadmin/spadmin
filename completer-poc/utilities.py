import os
import re
import sys
import globals
import readchar
import uuid
import subprocess

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

def add_remove_color(color, string):
    color_pattern = r"\x1b\[.+?m"
    color_reset = "\x1b[0m"
    ret = string
    matches = re.findall(color_pattern, string)
    ret = ret.replace(color_reset,color)
    return color + ret + color_reset


def printer(string):
    s = str(string).split("\n")
    i = 0
    grep = globals.extras['grep'] if 'grep' in globals.extras else ''

    for line in s:
        # if grep != '':
        #     if re.search(grep, line):
        #         i += 1
        #         print(line.replace(grep,'\x1b[1;37;40m'+ grep + "\x1b[0m"), sep="\n")
        # else:
        #     i += 1
        i += 1
        print(line, sep="\n")
        if 'more' in globals.extras and i > globals.rows - 3:
            print("more...   (<ENTER> to continue, 'C' to cancel)")
            key = readchar.readkey()
            if str(key).lower() == "c":
                print(*s[i + globals.rows - 2:], sep="\n")
                break
            i = 0

def check_connection(server: str, id: str, password: str) -> bool:
    if id == '' or password == '':
        print ('Userid and password won\'t be empty!')
        return False
    try:
        result = ''
        if server != '':
            result = subprocess.check_output(
                ['dsmadmc', '-se=%s' % server, '-id=%s' % id, '-pa=%s' % password, '-dataonly=yes',
                 'select SERVER_NAME from STATUS'], stderr=subprocess.STDOUT, timeout=10,
                universal_newlines=True)
        else:
            result = subprocess.check_output(
                ['dsmadmc', '-id=%s' % id, '-pa=%s' % password, '-dataonly=yes',
                 'select SERVER_NAME from STATUS'], stderr=subprocess.STDOUT, timeout=10,
                universal_newlines=True)
        print("We have successfully connected to: ", result.strip())
        return True
    except subprocess.CalledProcessError as exc:
        print(exc.output, "\nReturn code:", exc.returncode, "\n")
        return False

def getmac():
    ret = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return ret

def consoleline( char='-'):
    print(char * globals.columns)


def consolefilledline(left = '', pattern = '-', right = '', width = 120):
    patternwith = width - len(left) - len(right) - 2
    return left + ' ' + pattern * patternwith + ' ' + right


def regexpgenerator(regexp):
            
    savelastchar = ''
    if regexp[ -1 ] == '=':
        savelastchar = regexp[ -1 ]
        regexp = regexp[ : -1 ]
    # # save v2 with regexp pattern
    # match = search( '(=.*)$', regexp )
    # if match:
    #   savelastchar = match[ 1 ]
    #   regexp = regexp.replace( match[ 1 ], '' )  
    
    result = ''
    for part in regexp.split():
    
        if part[ 0 ].isupper():
    
            tmpregexp = part
            tmpstring = part
            for x in part:
                if tmpstring[ -1 ].isupper():
                    break
                tmpstring = part[ 0:len( tmpstring ) - 1 ]
                tmpregexp += '|' + tmpstring
    
            result += '(' + tmpregexp + ')'
    
        else:
            result += '(' + part + ')'
    
        result += '\s+'
    
    return result[ :-3 ] + savelastchar


def dictmerger( destination, source ):
    for key in source:
        if key not in destination:
             destination[ key ] = []
        destination[ key ].extend( source [ key ] )