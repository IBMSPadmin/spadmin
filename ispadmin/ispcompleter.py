import re
import subprocess
import pexpect
from prompt_toolkit.completion import NestedCompleter, Completion, Completer, WordCompleter


class DsmadmcSelectCompleter(Completer):
    select = None
    MORE = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt

    def __init__(self,analyzer, select):
        if not select:
            pass
        self.select = select
        self.analyzer = analyzer

    def count_space(self, string):
        count = 0
        for i in range(0, len(string)):
            if string[i] == " ":
                count += 1
        return count

    def execute(self, sql):
        self.analyzer.sendline(sql)
        self.analyzer.expect(
            ['Protect: USERTSM.USR>', self.MORE, self.MORE2,
             pexpect.EOF])  ## várjuk, hogy promptot vagy "MORE"-t kapjunk
        list = self.analyzer.before.splitlines()
        list.pop(0) # delete "select" command
        while ("" in list): ## remove empty lines
            list.remove("")
        return list

    def get_completions(self, document, complete_event):
        if self.select == "NODE":
            if document.cursor_position == 0:  # ha most lépett be a függvénybe
                yield Completion("*", start_position=0)
                for a in self.execute('select NODE_NAME from NODES'):
                   yield Completion(a.strip(), start_position=0)
            elif self.count_space(re.sub(' +', ' ', document.text)) > 0:  # már legalább 2. alkalommal lépett be a függvénybe
                for a in ["DOmain=","Format=Standard","Format=Detailed","AUTHentication=LOcal","AUTHentication=LDap","Type=Client","Type=NAS","Type=Server","Type=Any",]:
                    yield Completion(a, start_position=0)

        elif self.select == "STGP":
            if document.cursor_position == 0:  # ha most lépett be a függvénybe
                yield Completion("*", start_position=0)
                for line in self.execute('select STGPOOL_NAME from STGPOOLS'):
                    yield Completion(line.strip(), start_position=0)
            elif self.count_space(re.sub(' +', ' ', document.text)) > 0:  # már legalább 2. alkalommal lépett be a függvénybe
                for a in ["Format=Standard","Format=Detailed","POoltype=ANY","POoltype=PRimary","POoltype=COpy","POoltype=COPYCONtainer","POoltype=ACTIVEdata","POoltype=RETention"]:
                    yield Completion(a, start_position=0)

        elif self.select == "DOM":
            if document.cursor_position == 0: # ha most lépett be a függvénybe
                for line in self.execute('select DOMAIN_NAME from DOMAINS'):
                    yield Completion(line.strip(), start_position=0)
            elif self.count_space(re.sub(' +', ' ',document.text)) == 1: # már legalább 2. alkalommal lépett be a függvénybe
                for line in self.execute('select SET_NAME from POLICYSETS where DOMAIN_NAME=\'%s\'' % document.text.strip()):
                    yield Completion(line.strip(), start_position=0)
            else:
                pass