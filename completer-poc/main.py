#!/usr/bin/env python
"""
Example of using the control-space key binding for auto completion.
"""
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle
from re import search
import logging

logging.basicConfig(filename="logfile.txt",
                    filemode='a',
                    format='%(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

class DsmadmcSelectCompleter(NestedCompleter):
    select = None

    def __init__(self, select):
        if not select:
            pass
        self.select = select

    def get_completions(self, document, complete_event):
        tokens = document.text.split(" ")
        if self.select == "new":
            # Level 0
            if document.cursor_position == 0:
                logging.info("Level 0: [" + document.text + "]")
                yield Completion("backup ", start_position=0)
                yield Completion("define ", start_position=0)
                yield Completion("delete ", start_position=0)
                yield Completion("query ", start_position=0)
                yield Completion("quit ", start_position=0)
            logging.info("Level 1: Nr. of tokens: %s Length of prompt: %s, Token: [%s]", len(tokens), len(document.text), document.text )
            # Level 3
            if len(tokens) >= 3:
                ############ Backup DB
                ###################
                if search("b.*", tokens[0]) and search("db.*", tokens[1]):
                    if not tokens[len(tokens)-1]:  # Backup, és db a második szó
                        yield Completion("type", start_position=0)
                        yield Completion("devclass", start_position=0)
                    elif search('t.*=f.*', tokens[len(tokens) - 1]):  # Backup, DB
                        yield Completion("full ", start_position=0 - len(tokens[len(tokens)-2]+1))
                    elif search('t.*=d.*', tokens[len(tokens) - 1]):  # Backup, DB
                        yield Completion("dbs ", start_position=0 - len(tokens[len(tokens)-2]+1))
                    elif search('t.*=i.*', tokens[len(tokens) - 1]):  # Backup, DB
                        yield Completion("incr ", start_position=0 - len(tokens[len(tokens)-2]+1))
                    elif search('t.*=', tokens[len(tokens)-1]):  # Backup, DB
                        yield Completion("full", start_position=0 )
                        yield Completion("dbs", start_position=0)
                        yield Completion("incr", start_position=0)
                    elif search('d.*=', tokens[len(tokens)-1]):  # Backup, DEVC
                        yield Completion("AC_01 ", start_position=0)
                        yield Completion("BC_01 ", start_position=0)
                        yield Completion("CC_01 ", start_position=0)
                        yield Completion("DC_01 ", start_position=0)
                    elif search('t.*', tokens[len(tokens)-1]):  # Backup, DB
                        yield Completion("type=", start_position=0 - len(tokens[len(tokens)-1]))
                    elif search('d.*', tokens[len(tokens)-1]):  # Backup, DEVC
                        yield Completion("devclass= ", start_position=0 - len(tokens[len(tokens)-1]))

            # Level 2
            if len(tokens) == 2:
                ############ Backup
                ###################
                if search("b.*", tokens[0]):
                    if not tokens[1]: # Backup, és üres a második szó, tehát csak egy szóközt ütöttek
                        yield Completion("db ", start_position=0 )
                        yield Completion("devc ", start_position=0)
                        yield Completion("volhistory ", start_position=0)
                    elif search('db', tokens[1]): # Backup, DB
                        yield Completion("db ", start_position=0 - len(tokens[1]))
                    elif search('de.*', tokens[1]): # Backup, DEVC
                        yield Completion("devc ", start_position=0 - len(tokens[1]))
                    elif search('d.*',tokens[1]): # Backup, D*
                        yield Completion("db", start_position=0 - len(tokens[1]))
                        yield Completion("devc", start_position=0 - len(tokens[1]))
                    elif search('v.*', tokens[1]):  # Backup, VOLHISTORY
                        yield Completion("volhistory ", start_position=0 - len(tokens[1]))
                ############ Query
                ###################
                if search("que.*", tokens[0]):
                    if not tokens[1]:  # Query, és üres a második szó, tehát csak egy szóközt ütöttek
                        yield Completion("node ", start_position=0)
                        yield Completion("stgpool ", start_position=0)
                    elif search('n.*', tokens[1]):
                        yield Completion("node ", start_position=0 - len(tokens[1]))
                    elif search('s.*', tokens[1]):
                        yield Completion("stgpool ", start_position=0 - len(tokens[1]))
                # Level 1
            elif len(tokens) == 1:
                if search("(backup|backu|back|bac|ba|b)", tokens[0]):
                    yield Completion("backup ", start_position=0 - len(document.text))
                elif search("(query|quer|que)", tokens[0]):
                    yield Completion("query ", start_position=0 - len(document.text))
                elif search("(quit|qui)", tokens[0]):
                    yield Completion("quit ", start_position=0 - len(document.text))
                elif search("(qu|q)", tokens[0]):
                    yield Completion("query ", start_position=0 - len(document.text))
                    yield Completion("quit ", start_position=0 - len(document.text))


            pass




kb = KeyBindings()


@kb.add("c-space")
def _(event):
    """
    Start auto completion. If the menu is showing already, select the next
    completion.
    """
    b = event.app.current_buffer
    if b.complete_state:
        b.complete_next()
    else:
        b.start_completion(select_first=False)


def main():
    text = prompt(
        "Spectrum> ",
        completer=DsmadmcSelectCompleter("new"),
        complete_style=CompleteStyle.MULTI_COLUMN,
        complete_while_typing=False,
        key_bindings=kb,

    )
    print("You said: %s" % text)


if __name__ == "__main__":
    while 1:
        main()

