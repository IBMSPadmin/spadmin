import re
import pexpect
import os
from termcolor import colored
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig

START_DSMADMC = 'dsmadmc -id=support -pa=asdpoi123'  # Ezzel indítom a TSM klienst
TSM_PROMPT = 'Protect: CLOUDTSM1'  # ez azért fontos, mert itt áll meg a pexpect
MORE = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'


def token(string):
    """A paraméterben kapott string-et szavakra szedi. a Highlight függvény használja"""
    # return string.split()
    start = 0
    i = 0
    token_list = []
    for x in range(0, len(string)):
        if " " == string[i:i + 1][0]:
            token_list.append(string[start:i + 1])
            start = i + 1
        elif "\n" == string[i:i + 1][0]:
            token_list.append(string[start:i + 1])
            start = i + 1
        i += 1
    token_list.append(string[start:i + 1])
    return token_list


def highlight(text):
    """a kapott szöveget szavakra szedi a token függvény hívásával, majd ezeket színezi a megadott reguláris kif. segítségével"""
    string = ""
    word: text
    for word in token(text):
        if re.search('Off', word):
            string += (colored(word, 'red'))
        elif re.search('(ANR\d\d\d\dE.*)', word):
            string += (colored(word, 'red'))
        elif re.search('(ANR\d\d\d\dW.*)', word):
            string += (colored(word, 'yellow'))
        elif re.search('([A-Za-z]{1,5}[0-9]{1,5}L[1-9])', word):  # LTO cartridges
            string += (colored(word, 'green'))
        else:
            string += (word)
    return string


completer = NestedCompleter.from_nested_dict({
    'show': {
        'time': None,
        'bufstats': None,
    },
    'query': {
        'node': {
            'a': None,
            'b': None,
        },
        'session': None,
        'process': None,
        'actlog': None,
    },
    'exit': None,
})


def commandline():
    """Command line interface"""

    text = session.prompt(
        TSM_PROMPT, completer=completer, complete_while_typing=False, cursor=CursorShape.BLINKING_BLOCK
    ) ## Prompt, history-val és completerrel.

    if not analyzer.isalive():
        print("Exception has occured, respawn required")
        quit(1) ## ide kellene megírni az automatikus respawn funkciót

    columns, rows = os.get_terminal_size(0)
    analyzer.setwinsize(rows, columns) ## hátha át lett méretezve az ablak
    analyzer.sendline(text) ## beküldjük a parancsot
    analyzer.expect([TSM_PROMPT, MORE]) ## várjuk, hogy promptot vagy "MORE"-t kapjunk
    print(highlight(analyzer.before)) ## Highlighter-es kiíratás
    if analyzer.match_index == 1:
        print("more...   (<ENTER> to continue, 'C' to cancel")


if __name__ == "__main__":
    """Main metódus"""
    print('Let\'s start!')
    print(colored('Hello', 'red'), colored('world!', 'green'))
    analyzer = pexpect.spawn('%s' % START_DSMADMC, encoding='utf-8')
    analyzer.expect([TSM_PROMPT, MORE])
    session = PromptSession()

    while True:
        commandline()
