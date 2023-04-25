import os
import re
import sys
from . import globals
import readchar
import uuid
import subprocess
import base64

import lib.columnar as columnar

from termcolor import colored
from typing import (
    Sequence
)

ansi_color_pattern = re.compile(r"\x1b\[.+?m")

PASS = "PASS"
def encode(password):
    encoded_byte_list = [(ord(a) ^ ord(b)) for a, b in zip(password, getmac())]
    b64_encoded_string = base64.b64encode(bytes(encoded_byte_list)).decode('ascii')
    return PASS + b64_encoded_string

def decode (b64_encoded):
    if b64_encoded.startswith(PASS):
        b64_decoded = list(base64.b64decode(b64_encoded[len(PASS):]))
        decoded = [(ord(a) ^ ord(b)) for a, b in zip(''.join([chr(x) for x in b64_decoded]), getmac())]
        decoded_string = ''.join([chr(x) for x in decoded])
        return decoded_string
    else:
        return b64_encoded


def refreshrowscolumns():
    row, column = os.popen('stty size', 'r').read().split()
    globals.rows = int(row)
    globals.columns = int(column)


def progressbar(count, total, leadtext=''):
    barlength = globals.columns - 2 - len(leadtext)  # [...]
    filledlength = int(round((barlength) * count / float(total)))

    percent = round(100.0 * count / float(total), 1)
    barline = '=' * filledlength + colored('-', globals.color_grey, attrs=[globals.color_attrs_bold ]) * (barlength - filledlength)

    sys.stdout.write(leadtext + '[%s]\r' % (barline))
    sys.stdout.write(leadtext + '[%s%s\r' % (colored(percent, globals.color_grey, globals.color_on_white), colored('%', globals.color_grey, globals.color_on_white)))
    sys.stdout.flush()


def add_remove_color(color, string):
    color_pattern = r"\x1b\[.+?m"
    color_reset = "\x1b[0m"
    ret = string
    matches = re.findall(color_pattern, string)
    ret = ret.replace(color_reset, color)
    return color + ret + color_reset


def printer(string):
    if not string:
        return

    filename = globals.extras[ 'file' ] if 'file' in globals.extras else ''
    
    if filename != '':
        with open( filename, 'w' ) as f:
            f.writelines( string )
            f.writelines( '\n' )
        return

    filename = globals.extras[ 'fileappend' ] if 'fileappend' in globals.extras else ''
    
    if filename != '':
        with open( filename, 'a' ) as f:
            f.writelines( string )
            f.writelines( '\n' )
        return

    s = str(string).split("\n")
    i = 0

    refreshrowscolumns()

    for line in s:
        i += 1
        
        print( line, sep='' )

        if 'more' in globals.extras and i > globals.rows - 2:
            sys.stdout.write("more...   (<ENTER> to continue, 'C' to cancel)")
            sys.stdout.flush()
            key = readchar.readkey()
            print()
            if str(key).lower() == "c":
                #print(*s[i + globals.rows - 2:], sep="\n")
                # print()
                break
            i = 0
            #print('\n')
            
    count = globals.extras[ 'count' ] if 'count' in globals.extras else ''
    if count != '':
        print( 'Line count = ' + colored( str( len( s ) ), globals.color_white, attrs=[globals.color_attrs_bold] ) )


def check_connection(server: str, id: str, password: str) -> bool:
    if id == '' or password == '':
        print('Userid and password won\'t be empty!')
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
    except Exception as exc:
        print(exc.output, "\n")
        return False


def start_console(server: str, id: str, password: str) -> bool:
    if id == '' or password == '':
        print('Userid and password won\'t be empty!')
        return False
    try:
        if server != '':
            dsmadmc = subprocess.Popen(
                ['dsmadmc', '-se=%s' % server, '-id=%s' % id, '-pa=%s' % password, '-console'], stdout=subprocess.PIPE)
        else:
            dsmadmc = subprocess.Popen(
                ['dsmadmc', '-id=%s' % id, '-pa=%s' % password, '-console'], stdout=subprocess.PIPE)
        print("Console mode started.")
        
        while True:
            line = dsmadmc.stdout.readline().decode("utf-8")
            if not line:
                break
            line = colorize_line( line )
            print(line, end='')
            
        print("Console mode ended.")
    
        return True
    
    except Exception as exc:
        print(exc.output, "\nAn error occured during the console mode\n")
        return False
        
    except KeyboardInterrupt:
        print( '\nQuit...' )
        return False
        

def colorize_line( line ):
    if re.search( '^ANR\d{4}E', line ):
        return colored( line, globals.color_red, attrs = [ globals.color_attrs_bold ])
    elif re.search( '^ANR\d{4}W', line ):
        return colored( line, globals.color_yellow, attrs = [ globals.color_attrs_bold ])
    elif re.search( '^ANR\d{4}D', line ):
        return colored( line, globals.color_cyan, attrs = [ globals.color_attrs_bold ])
    elif re.search( '^AN\d{5}S', line ):
        return colored( line, globals.color_red, attrs = [ globals.color_attrs_bold ])
    else:
        return line

def getmac():
    #ret = ':'.join(re.findall('../..', '%012x' % uuid.getnode()))
    mac_address = uuid.getnode()
    # print(mac_address)
    ret = ':'.join(['{:02x}'.format((mac_address >> elements) & 0xff) for elements in range(0,8*6,8)][::-1])
    return ret

def validate_license():
    if getmac() and getmac() == '7e:17:4c:06:06:e7':
        print(colored( " Your license is valid for 2023.02.03.!", globals.color_green, attrs = [ globals.color_attrs_bold ]))
        globals.licensed = True
    else:
        print(colored( " Your License key has expired!", globals.color_red, attrs = [ globals.color_attrs_bold ]))
        print()
        globals.licensed = True


def consoleline(char='-'):
    print(char * globals.columns)


def consolefilledline(left='', pattern='-', right='', width=120):
    patternwith = width - len(left) - len(right) - 2
    return left + ' ' + pattern * patternwith + ' ' + right


def regexpgenerator(regexp):
    savelastchar = ''
    if regexp[-1] == '=':
        savelastchar = regexp[-1] + '(?!.*\w+\s)'
        regexp = regexp[: -1]
    # # save v2 with regexp pattern
    # match = search( '(=.*)$', regexp )
    # if match:
    #   savelastchar = match[ 1 ]
    #   regexp = regexp.replace( match[ 1 ], '' )  

    result = ''
    for part in regexp.split():

        if part[0].isupper():

            tmpregexp = part
            tmpstring = part
            for x in part:
                if tmpstring[-1].isupper():
                    break
                tmpstring = part[0:len(tmpstring) - 1]
                tmpregexp += '|' + tmpstring

            result += '(' + tmpregexp + ')'

        else:
            result += '(' + part + ')'

        result += '\s+'

    return result[:-3] + savelastchar


def dictmerger(destination, source):
    for key in source:
        if key not in destination:
            destination[key] = []
        destination[key].extend(source[key])
        
def color( text, color: "" ):
    
    htmlout = True if 'htmlout' in globals.extras else False
    
    if htmlout:

        if color == 'red':
             return '<span style="color:' + color + '">' + text + '</span>'

        elif color == 'green':
             return '<span style="color:' + color + '">' + text + '</span>'

        elif color == 'yellow':
             return '<span style="color:' + color + '">' + text + '</span>'

        elif color == 'white':
             return '<span style="color:' + color + '">' + text + '</span>'


        else:
            return text
    else:

        if color == 'red':
             return colored( text, globals.color_red,   attrs = [ globals.color_attrs_bold ] )

        elif color == 'green':
             return colored( text, globals.color_green, attrs = [ globals.color_attrs_bold ] )

        elif color == 'yellow':
             return colored( text, globals.color_yellow, attrs = [ globals.color_attrs_bold ] )

        elif color == 'white':
             return colored( text, globals.color_white, attrs = [ globals.color_attrs_bold ] )

        else:
            return text