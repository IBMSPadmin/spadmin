import re
import sys
from colorama import Fore, Back, Style

ansi_color_pattern = re.compile(r"\x1b\[.+?m")

def green(match_obj):
    for g in match_obj.groups():
        if g is not None:
            return Fore.GREEN + match_obj.group(1) + Style.RESET_ALL


def yellow(match_obj):
    for g in match_obj.groups():
        if g is not None:
            return Fore.YELLOW + match_obj.group(1) + Style.RESET_ALL


def coloring(color, line) -> str:
    for match in ansi_color_pattern.finditer(line):
        if match.group() == Style.RESET_ALL:
            line = line.replace(match.group(), Style.RESET_ALL + color)
        else:
            line = line.replace(match.group(), ''.join([Style.RESET_ALL, match.group()]))
    return "".join([color, line, Style.RESET_ALL])


for line in sys.stdin:
    line = re.sub(r"(Session)", green, line)
    line = re.sub(r"(No match found using this criteria)", green, line)
    line = re.sub(r"(Session)", green, line)
    if re.search("ANR....W", line):
        line = coloring(Fore.YELLOW, line)
    if re.search("ANR....E", line):
        line = coloring(Fore.RED, line)
    print(line, end='')
