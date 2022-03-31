import pexpect
import os
import datetime
import re
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig

from termcolor import colored

class Dsmadmc:
    "This is the DSMADMC wrapper class"
    START_DSMADMC = 'dsmadmc'  # Ezzel a paranccsal indítom a TSM klienst - csak Mac-en tesztelve!
    # TSM_PROMPT = 'Protect: USERTSM.USR>'  # ez azért fontos, mert itt áll meg a pexpect
    MORE = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    analyzer = None
    start = datetime.datetime.utcnow()
    config = None
    session = PromptSession()
    def __init__(self, configuration):
        self.config = configuration

    def sendline(self,text):
        if self.analyzer is None or not self.analyzer.isalive():
            self.startdsmadmc(self)
        columns, rows = os.get_terminal_size(0)
        self.analyzer.setwinsize(rows, columns)  ## hátha át lett méretezve az ablak
        self.analyzer.sendline(self.commandPreprocessor(text))  ## beküldjük a parancsot
        self.analyzer.expect(
            [self.config.prompt, Dsmadmc.MORE, Dsmadmc.MORE2, pexpect.EOF])  ## várjuk, hogy promptot vagy "MORE"-t kapjunk
        print(self.highlight(self.analyzer.before))  ## Highlighter-es kiíratás
        if self.analyzer.match_index == 1:
            self.commandline("more...   (<ENTER> to continue, 'C' to cancel)")
        if self.analyzer.match_index == 2:
            self.commandline("The character '#' stands for any decimal integer.")
        elif self.analyzer.match_index == 3:
            self.bye()
            quit();

    def bye(self):
        end_date = datetime.datetime.utcnow()
        print(colored('Thanks!', 'green'), colored('spadmin has run', 'white'),
              str(datetime.timedelta(seconds=abs((end_date - self.start).seconds))), colored('total', 'white'))

    def startdsmadmc(self, self1):
        STARTCOMMAND = self.START_DSMADMC + " -id=" + self.config.id + " -pa=" + self.config.password
        self.analyzer = pexpect.spawn('%s' % STARTCOMMAND, encoding='utf-8')
        self.analyzer.expect([self.config.prompt, self.MORE, self.MORE2])
        if not self.analyzer.isalive():
            print("Exception has occured, NO MORE respawn")
            print(self.highlight(self.analyzer.before))
            quit(1)

    def commandPreprocessor(self,text):
        if text == 'sh actlog':
            return 'select DATE_TIME,MESSAGE from actlog WHERE (DATE_TIME>=current_timestamp-24 hour) order by 2 '
        return text

    def highlight(self, text):
        """a kapott szöveget sorokra szedi, majd ezeket színezi a megadott reguláris kif. segítségével"""
        string = ""
        for word in text.split('\n'):
            if re.search('Off', word):
                string += (colored(word, 'red')) + "\n"
            elif re.search('(ANR\d\d\d\dE)', word):
                string += (colored(word, 'red')) + "\n"
            elif re.search('(ANR\d\d\d\dW)', word):
                string += (colored(word, 'yellow')) + "\n"
            elif re.search('([A-Za-z]{1,5}[0-9]{1,5}L[1-9])', word):  # LTO cartridges
                string += (colored(word, 'green')) + "\n"
            else:
                string += (word) + "\n"
        return string

    def commandline(self, prmpt):
        """Command line interface"""
        if not prmpt:
            text = self.session.prompt(
                self.config.prompt, completer=completer, complete_while_typing=False, cursor=CursorShape.BLINKING_BLOCK)
        else:
            text = self.session.prompt(
                prmpt, completer=completer, complete_while_typing=False,
                cursor=CursorShape.BLINKING_BLOCK)  # Prompt, history-val és completerrel.
        self.sendline(text)


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
