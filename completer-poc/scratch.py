import queue
import re
import sys
from typing import Sequence
from typing.re import Match

from colorama import Fore, Back, Style
from termcolor import colored
import humanbytes

def yellow(match_obj):
    for g in match_obj.groups():
        if g is not None:
            return Fore.YELLOW + match_obj.group() + Style.RESET_ALL


text = "ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria."
# print (text)

text = text.replace("No match found using this criteria",
                    ''.join([Fore.BLUE, "No match found using this criteria", Style.RESET_ALL]))
# print (text)

text = Fore.RED + text + Style.RESET_ALL

# print (repr(text))
# print (text)
grep = "u"

# RED
#                                     Kek
#    ANR2034E QUERY STGPOOLDIRECTORY: No match found using this criteria RESET  . RESET

text = re.sub(r"(" + grep + ")", yellow, str(text))
# print (repr(text))
# print (text)

ansi_color_pattern = re.compile(r"\x1b\[.+?m")

print("")
print("")
print("")


def szinezo_jo(text: str, regexp: str, color: str):
    match = re.search(regexp, text)
    print(match)
    if match:
        before = text[0:match.start()]
        # print(repr(before))
        last_colors = re.findall("(\x1b\[.+?m)", before)
        found_last_color = ''
        if last_colors:
            found_last_color = last_colors[-1]
        return text.replace(match[0], colored(match[0], color) + found_last_color)
    else:
        return text


# re.compile(r"(" + match.group() + ")").finditer(text):

def szinezo(text: str, regexp: str, color: str):
    ret = text
    for m in reversed(list(re.finditer(regexp, text))):
        last_colors = re.findall("(\x1b\[1m\x1b\[.+?m)", text[0:m.start()])
        if last_colors:
            ret = ''.join(
                [ret[0:m.start()], colored(ret[m.start():(m.start() + len(m.group()))], color, attrs=['bold']), last_colors[-1],
                 ret[m.start() + len(m.group()):]])
        else:
            ret = text[0:m.start()] + colored(text[m.start():(m.start() + len(m.group()))], color, attrs=['bold']) + text[
                                                                                                     m.start() + len(
                                                                                                         m.group()):]
    return ret


text = "ANR2034E QUERY STGPOuOuLDuuuIRECTORY: No match found using this criteria."
text = szinezo(text, "ANR....E.*$", "red")
print(repr(text))
text = szinezo(text, "TGPOuOuLDuuuIRECTORY", "blue")
print(repr(text))
text = szinezo(text, "u", "yellow")
print(repr(text))
text = szinezo(text, "O", "green")
print(repr(text))
text = szinezo(text, "i", "cyan")
print(repr(text))
print(text)



def strip_color(cell_text):
    matches = [match for match in ansi_color_pattern.finditer(cell_text)]
    clean_text = cell_text
    if matches:
        clean_text = ansi_color_pattern.sub("", cell_text)
    return clean_text, matches


def colorize(text, code: Sequence[Match]):
    ret = text
    code_list = list(code)
    marker = -1
    for i, m in enumerate(code_list):
        print("M: ", m, i)
        if m.group() == Style.RESET_ALL:
            marker -= 1
            print("MarkerR: ", repr(code_list[marker].group()))
            ret = "".join([ret[:m.start()+1], code_list[marker].group(), ret[m.start()+1:]])
        else:
            marker += 1
            print("MarkerC: ", repr(code_list[marker].group()))
            ret = "".join([ret[:m.start()], m.group(), ret[m.start():]])
    return ret + Style.RESET_ALL


# clean = "ANR2034E QUERY REPLICATION: No match found using this criteria."
# text = "ANR2034E QUERY REPLICATION: No match found using this criteria."
#
# text = colored(text, "red")
# value, code = strip_color(text)
# print(colorize(value, code))
#
# text = text.replace("No match found using this c",
#                     ''.join([Fore.BLUE, "No match found using this c", Style.RESET_ALL]))
# value, code = strip_color(text)
# print(colorize(value, code))
#
# text = text.replace("found",
#                     ''.join([Fore.YELLOW, "found", Style.RESET_ALL]))
# value, code = strip_color(text)
# print(colorize(value, code))
#
# text = text.replace("i",
#                     ''.join([Fore.CYAN, "i", Style.RESET_ALL]))
# value, code = strip_color(text)
# print(colorize(value, code))


from wcwidth import wcwidth, wcswidth



def get_visible_lenght(code, text):
    s = ''
    i = 0
    while repr(s) != repr(text):
        s = re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code[0:i]))
        i += 1
        print(repr(s))
    return i-1

def get_visible_lenght_vege(code, text):
    s = ''
    i = len(code)
    while repr(s) != repr(text):
        s = re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code[i:]))
        i -= 1
        print(repr(s))
    return i+1


def szinezd_ki(code, text):
    if re.sub("(\x1b\[1m\x1b\[.+?m)",'',re.sub("(\x1b\[.+?m)",'',code)).startswith(str(text)):
        return code[:get_visible_lenght(code, str(text))]
    else:
        return code[get_visible_lenght_vege(code, str(text)):]

code = '\x1b[1m\x1b[31mANR2034E QUERY S\x1b[1m\x1b[34mTGP\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34mLD\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34m\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[34mIRECT\x1b[1m\x1b[32mO\x1b[0m\x1b[1m\x1b[34mRY\x1b[0m\x1b[1m\x1b[31m: No match fo\x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[31mnd \x1b[1m\x1b[33mu\x1b[0m\x1b[1m\x1b[31ms\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31mng th\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31ms cr\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31mter\x1b[1m\x1b[36mi\x1b[0m\x1b[1m\x1b[31ma.\x1b[0m'
text = 'ANR2034E QUERY STGPOuOuLDuuuIRECTORY: No match found u'

print(text)
print(code)
# print("1", szinezd_ki(code,text))

# text = 'sing this criteria.'
# print("2", szinezd_ki(code,text))
#
# code = '\x1b[1m\x1b[31m 677 \x1b[0m'
# text = 677
#
# print("3", szinezd_ki(code,str(text)))

print (humanbytes.HumanBytes.format(float(128)*1024*1024, unit="BINARY_LABELS", precision=0))
print (humanbytes.HumanBytes.format(float(128)*1024*1024, unit="METRIC_LABELS",precision=0))
print (humanbytes.HumanBytes.format(int(31), unit="TIME_LABELS",precision=0))
print (humanbytes.HumanBytes.format(int(65), unit="TIME_LABELS",precision=0))
print (humanbytes.HumanBytes.format(int(128), unit="TIME_LABELS",precision=0))
print (humanbytes.HumanBytes.format(int(3600*23), unit="TIME_LABELS",precision=0))