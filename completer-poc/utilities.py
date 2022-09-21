import os
import re
import sys
import globals
import readchar
import uuid
import subprocess
from colorama import Fore, Back, Style
from termcolor import colored
from typing import (
    Sequence,
)
ansi_color_pattern = re.compile(r"\x1b\[.+?m")


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

    for line in s:
        i += 1
      #  print(repr(line), sep="\n")
        print(line, sep="")
        if 'more' in globals.extras and i > globals.rows - 3:
            print("more...   (<ENTER> to continue, 'C' to cancel)")
            key = readchar.readkey()
            if str(key).lower() == "c":
                print(*s[i + globals.rows - 2:], sep="\n")
                break
            i = 0

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
            if re.search("ANR....W", line):
                line = coloring(Fore.YELLOW, line)
            if re.search("ANR....E", line):
                line = coloring(Fore.RED, line)
            if re.search("ANR....D", line):
                line = coloring(Fore.CYAN, line)
            if re.search("AN.....S", line):
                line = coloring(Fore.CYAN, line)
            print(line, end='')
        print("Console mode ended.")
        return True
    except subprocess.CalledProcessError as exc:
        print(exc.output, "\nAn error occured during the console mode, Return code:", exc.returncode, "\n")
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
        savelastchar = regexp[ -1 ] + '(?!.*\w+\s)'
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


def green(match_obj):
    for g in match_obj.groups():
        if g is not None:
            return Fore.GREEN + match_obj.group() + Style.RESET_ALL


def yellow(match_obj):
    for g in match_obj.groups():
        if g is not None:
            return Fore.YELLOW + match_obj.group() + Style.RESET_ALL


def coloring(color, line) -> str:
    for match in ansi_color_pattern.finditer(line):
        if match.group() == Style.RESET_ALL:
            line = line.replace(match.group(), Style.RESET_ALL + color)
        else:
            line = line.replace(match.group(), ''.join([Style.RESET_ALL, match.group()]))
    return "".join([color, line, Style.RESET_ALL])


def szinezo(text: str, regexp: str, color: Sequence[str]):
    ret = text
    for m in reversed(list(re.finditer(regexp, text))):
        last_colors = re.findall("(\x1b\[1m\x1b\[.+?m)|(\x1b\[.+?m)", text[0:m.start()])
        if last_colors:
            ret = ''.join(
                [ret[0:m.start()], ''.join(color), ret[m.start():(m.start() + len(m.group()))], last_colors[-1],
                 ret[m.start() + len(m.group()):]])
        else:
            ret = ''.join([text[0:m.start()], ''.join(color), text[m.start():(m.start() + len(m.group()))], text[
                                                                                                     m.start() + len(
                                                                                                         m.group()):]])
    return ret