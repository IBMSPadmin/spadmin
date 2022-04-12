import re
import subprocess

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter, Completion, Completer, WordCompleter


class DsmadmcSelectCompleter(Completer):
    select = None

    def __init__(self, select):
        if not select:
            pass
        self.select = select

    def count_space(self, string):
        count = 0
        for i in range(0, len(string)):
            if string[i] == " ":
                count += 1
        return count

    def execute(self, sql):
        result = subprocess.check_output(
            ['dsmadmc', '-id=%s' % 'support', '-pa=%s' % 'userkft1q2', '-dataonly=yes',
             sql], stderr=subprocess.STDOUT, timeout=10,
            universal_newlines=True)
        return result

    def get_completions(self, document, complete_event):
        nodes = None
        if self.select == "NODE":
            if document.cursor_position == 0:  # ha most lépett be a függvénybe
                nodes = self.execute('select DOMAIN_NAME from DOMAINS').splitlines()
                for a in nodes:
                    yield Completion(a.strip(), start_position=0)
            elif self.count_space(re.sub(' +', ' ', document.text)) == 0:
                for a in nodes:
                    if a.startswith(document.text):
                        yield Completion(a.strip, start_position=0)

            elif self.count_space(re.sub(' +', ' ', document.text)) == 1:  # már legalább 2. alkalommal lépett be a függvénybe
                yield Completion("DOmain=", start_position=0)
                yield Completion("Format=", start_position=0)
                yield Completion("AUTHentication=LOcal", start_position=0)
                yield Completion("AUTHentication=LDap", start_position=0)
                yield Completion("Type=Client", start_position=0)
                yield Completion("Type=NAS", start_position=0)
                yield Completion("Type=Server", start_position=0)
                yield Completion("Type=Any", start_position=0)

        elif self.select == "STGP":
            yield Completion("STGP1", start_position=0)
            yield Completion("STGP2", start_position=0)
            yield Completion("STGP3", start_position=0)
            yield Completion("STGP4", start_position=0)
        elif self.select == "DOM":
            if document.cursor_position == 0: # ha most lépett be a függvénybe
                for line in self.execute('select DOMAIN_NAME from DOMAINS').splitlines():
                    yield Completion(line.strip(), start_position=0)
            elif self.count_space(re.sub(' +', ' ',document.text)) == 1: # már legalább 2. alkalommal lépett be a függvénybe
                for line in self.execute('select SET_NAME from POLICYSETS where DOMAIN_NAME=\'%s\'' % document.text.strip()).splitlines():
                    yield Completion(line.strip(), start_position=0)
            else:
                pass


completer = NestedCompleter.from_nested_dict({
    'accept': {
        'date': None
    },
    'activate':{
        'policyset': DsmadmcSelectCompleter("DOM")
    },
    'query': {
        'node':
            DsmadmcSelectCompleter("NODE"),
        'stgp': DsmadmcSelectCompleter("STGP"),
        'ip': {
            'interface': WordCompleter(["alligator", "ant"]),
        },
    },
    'quit': None,
})

text = prompt('# ', completer=completer, complete_while_typing=True)

print('You said: %s' % text)

d = [["Mark", 12, 95],
     ["Jay", 11, 88],
     ["Jack", 14, 90]]

print ("{:<8} {:<15} {:<10}".format('Name', 'Age', 'Percent'))

for v in d:
    name, age, perc = v
    print ("{:<8} {:<15} {:<10}".format(name, age, perc))
