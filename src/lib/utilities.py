import os
import re
import sys
from . import globals
import readchar
import uuid
import subprocess

from termcolor import colored
from typing import (
    Sequence
)

ansi_color_pattern = re.compile(r"\x1b\[.+?m")


def refreshrowscolumns():
    row, column = os.popen('stty size', 'r').read().split()
    globals.rows = int(row)
    globals.columns = int(column)


def progressbar(count, total, leadtext=''):
    barlength = globals.columns - 2 - len(leadtext)  # [...]
    filledlength = int(round((barlength) * count / float(total)))

    percent = round(100.0 * count / float(total), 1)
    barline = '=' * filledlength + colored('-', 'grey', attrs=['bold']) * (barlength - filledlength)

    sys.stdout.write(leadtext + '[%s]\r' % (barline))
    sys.stdout.write(leadtext + '[%s%s\r' % (colored(percent, 'grey', 'on_white'), colored('%', 'grey', 'on_white')))
    sys.stdout.flush()


def add_remove_color(color, string):
    color_pattern = r"\x1b\[.+?m"
    color_reset = "\x1b[0m"
    ret = string
    matches = re.findall(color_pattern, string)
    ret = ret.replace(color_reset, color)
    return color + ret + color_reset


def printer(string):
    s = str(string).split("\n")
    i = 0

    refreshrowscolumns()

    for line in s:
        i += 1
        print(line, sep="")
        if 'more' in globals.extras and i > globals.rows - 2:
            sys.stdout.write("more...   (<ENTER> to continue, 'C' to cancel)")
            sys.stdout.flush()
            key = readchar.readkey()
            if str(key).lower() == "c":
                #print(*s[i + globals.rows - 2:], sep="\n")
                print()
                break
            i = 0
            #print('\n')


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
    except subprocess.CalledProcessError as exc:
        print(exc.output, "\nReturn code:", exc.returncode, "\n")
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
    
    except subprocess.CalledProcessError as exc:
        print(exc.output, "\nAn error occured during the console mode, Return code:", exc.returncode, "\n")
        return False
        
    except KeyboardInterrupt:
        print( '\nQuit...' )
        return False
        

def colorize_line( line ):
    if re.search( '^ANR\d{4}E', line ):
        return colored( line, 'red', attrs = [ 'bold' ])
    elif re.search( '^ANR\d{4}W', line ):
        return colored( line, 'yellow', attrs = [ 'bold' ])
    elif re.search( '^ANR\d{4}D', line ):
        return colored( line, 'cyan', attrs = [ 'bold' ])
    elif re.search( '^AN\d{5}S', line ):
        return colored( line, 'red', attrs = [ 'bold' ])
    else:
        return line

def getmac():
    ret = ':'.join(re.findall('../..', '%012x' % uuid.getnode()))
    return ret


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