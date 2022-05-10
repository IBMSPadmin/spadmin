import pexpect
import os
import datetime
import re
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from ispadmin.ispcompleter import DsmadmcSelectCompleter
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig

from termcolor import colored

class Dsmadmc:
    "This is the DSMADMC wrapper class"
    START_DSMADMC = 'dsmadmc'  # Ezzel a paranccsal indítom a TSM klienst - csak Mac-en tesztelve!
    # TSM_PROMPT = 'Protect: USERTSM.USR>'  # ez azért fontos, mert itt áll meg a pexpect
    MORE = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    MORE3 = 'Do you wish to proceed\? \(Yes \(Y\)/No \(N\)\)'  # meg itt
    analyzer = None
    analyzertabdel = None
    start = datetime.datetime.utcnow()
    config = None
    session = PromptSession()
    def __init__(self, configuration):
        self.config = configuration

    def sendline(self,text):
        command = text
        if text == 'sh actlog':
           command = 'select DATE_TIME,MESSAGE from actlog WHERE (DATE_TIME>=current_timestamp-24 hour) order by 1'
        if self.analyzer is None or not self.analyzer.isalive():
            self.startdsmadmc(self)
        columns, rows = os.get_terminal_size(0)
        self.analyzer.setwinsize(rows, columns)  ## hátha át lett méretezve az ablak
        self.analyzer.sendline(command)  ## beküldjük a parancsot
        self.analyzer.expect(
            [self.config.prompt, Dsmadmc.MORE, Dsmadmc.MORE2, Dsmadmc.MORE3, pexpect.EOF])  ## várjuk, hogy promptot vagy "MORE"-t kapjunk
        print(self.highlight(self.analyzer.before))  ## Highlighter-es kiíratás
        if self.analyzer.match_index == 1:
            self.commandline("more...   (<ENTER> to continue, 'C' to cancel)")
        if self.analyzer.match_index == 2:
            self.commandline("The character '#' stands for any decimal integer.")
        if self.analyzer.match_index == 3:
            self.commandline("Do you wish to proceed? (Yes (Y)/No (N))")
        elif self.analyzer.match_index == 4:
            self.bye()
            quit();

    def bye(self):
        end_date = datetime.datetime.utcnow()
        print(colored('Thanks!', 'green'), colored('spadmin has run', 'white'),
              str(datetime.timedelta(seconds=abs((end_date - self.start).seconds))), colored('total', 'white'))

    def startdsmadmc(self, self1):
        STARTCOMMAND = self.START_DSMADMC + " -id=" + self.config.id + " -pa=" + self.config.password
        self.analyzer = pexpect.spawn('%s' % STARTCOMMAND, encoding='utf-8')
        self.analyzer.expect([self.config.prompt, self.MORE, self.MORE2, self.MORE3])
        if not self.analyzer.isalive():
            print("Exception has occured, NO MORE respawn")
            print(self.highlight(self.analyzer.before))
            quit(1)

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

    def getanalyzer(self):
        if self.analyzertabdel is None or not self.analyzertabdel.isalive():
            self.analyzertabdel = pexpect.spawn(self.START_DSMADMC + " -id=" + self.config.id + " -pa=" + self.config.password + " -dataonly=yes" + " -tabdel" + " -Itemcommit", encoding='utf-8')
            self.analyzertabdel.setwinsize(32767, 32767)
            self.analyzertabdel.expect([self.config.prompt, self.MORE, self.MORE2, self.MORE3])
        return self.analyzertabdel

    def commandline(self, prmpt):
        """Command line interface"""

        completer = NestedCompleter.from_nested_dict({
            'accept': {
                'date': None
            },
            'activate': {
                'policyset': DsmadmcSelectCompleter(self.getanalyzer(), "DOM")
            },
            'query': {
                'node':
                    DsmadmcSelectCompleter(self.getanalyzer(), "NODE"),
                'stgp': DsmadmcSelectCompleter(self.getanalyzer(), "STGP"),
            },
            'quit': None,
        })


        if not prmpt:
            text = self.session.prompt(
                self.config.prompt, completer=completer, complete_while_typing=False, cursor=CursorShape.BLINKING_BLOCK)
        else:
            text = self.session.prompt(
                prmpt, completer=completer, complete_while_typing=False,
                cursor=CursorShape.BLINKING_BLOCK)  # Prompt, history-val és completerrel.
        self.sendline(text)



