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
        # yield Completion("?", start_position=0)
        if self.select == "new":
            # Level 0
            if document.cursor_position == 0:
                logging.info("Level 0: [" + document.text + "]")
                yield Completion("backup", start_position=0)
                yield Completion("Define", start_position=0)
                yield Completion("Delete", start_position=0)
                yield Completion("Query", start_position=0)
            # Level 1
            else:
                # Ez a BACKUP parancs ága
                if search("(backup|backu|back|bac|ba|b)", document.text):
                    logging.info("\t [" + document.text + "]")
                    # Level 2: ha már van szóköz végén
                    if search("(backup|backu|back|bac|ba)\s+", document.text):
                        logging.info("\t\t [" + document.text + "]")
                        # Level 3: opciók
                        if search("(backup|backu|back|bac|ba)\s+db", document.text):
                            logging.info("\t\t\t [" + document.text + "]")
                            if search("ba.*db ", document.text):
                                logging.info("\t\t\t\t [" + document.text + "]")
                                if search("ba.*db.*t.*=", document.text):
                                    logging.info("\t\t\t\t\t [" + document.text + "]")
                                    start_position=0
                                    if document.text[-1] == " ":
                                        start_position=-1
                                    yield Completion("full", start_position=start_position)
                                    yield Completion("incremental", start_position=start_position)
                                    yield Completion("dbsnapshot", start_position=start_position)
                                elif search("ba.*db.*d.*=", document.text):
                                    yield Completion("AC_01", start_position=0)
                                    yield Completion("AC_02", start_position=0)
                                    yield Completion("DC_01", start_position=0)
                                    yield Completion("DC_02", start_position=0)
                                else:
                                    yield Completion("type=", start_position=0)
                                    yield Completion("devclass=", start_position=0)

                        else:
                            logging.info("\t\t\t length: [" + document.text + "]: %s", len(document.text.split()[-1]))
                            if search("\s+$",document.text):
                                yield Completion("db", start_position=0)
                            else:
                                yield Completion("db", start_position=0 - len(document.text.split()[-1]))
                    else:
                        yield Completion("backup", start_position=0 - len(document.text))
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
        complete_while_typing=True,
        key_bindings=kb,

    )
    print("You said: %s" % text)


if __name__ == "__main__":
    while 1:
        main()

