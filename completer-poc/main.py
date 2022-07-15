#!/usr/bin/env python
"""
Example of using the control-space key binding for auto completion.
"""
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.shortcuts import CompleteStyle
from re import search


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
                yield Completion("backup", start_position=0)
                yield Completion("Define", start_position=0)
                yield Completion("Delete", start_position=0)
                yield Completion("Query", start_position=0)
            # Level 1
            else:
                # Ez a BACKUP parancs ága
                if search("backup|backu|back|bac|ba|b", document.text):
                    # Level 2: ha már van szóköz végén
                    if search("backup |backu |back |bac |ba ", document.text):
                        # Level 3: opciók
                        if search("ba.*db", document.text):
                            if search("ba.*db ", document.text):
                                if search("ba.*db.*t.*=", document.text):
                                    yield Completion("full", start_position=0)
                                    yield Completion("incremental", start_position=0)
                                    yield Completion("dbsnapshot", start_position=0)
                                elif search("ba.*db.*d.*=", document.text):
                                    yield Completion("AC_01", start_position=0)
                                    yield Completion("AC_02", start_position=0)
                                    yield Completion("DC_01", start_position=0)
                                    yield Completion("DC_02", start_position=0)

                                else:
                                    yield Completion("type=", start_position=0)
                                    yield Completion("devclass=", start_position=0)

                        else:
                            yield Completion("db ", start_position=0)

                    else:
                        yield Completion("backup", start_position=0 - len(document.text))





        elif self.select == "backup_db":
            if document.cursor_position == 0:  # ha most lépett be a függvénybe
                    yield Completion("DEVclass=", start_position=0)
                    yield Completion("Type=", start_position=0)
                    yield Completion("VOLumenames=", start_position=0)
            else:
                if search("DEV.*=", document.text):
                    yield Completion("DEVC_01", start_position=-1)
                    yield Completion("DEVC_02", start_position=-1)
                    yield Completion("DEVC_03", start_position=-1)
                elif search("[dD].*", document.text):
                    yield Completion("DEVclass=", start_position=0-len(document.text))
        else:
            pass


completer = NestedCompleter.from_nested_dict({
    'ACCept': {
        'Date': None
    },
    'ACTivate': {
        'POlicyset': None
    },
    'ASsign': {
        'DEFMGmtclass': None
    },
    'AUDit': {
        'LIBRary': None,
        'LICense': {'?'},
        'Volume':None
    },
    'BAckup': {
        'DB': DsmadmcSelectCompleter("backup_db")
    },
    'Query': {
        'NOde':
            None,
        'STGp': None,
        'actlog': {'?'},
        'admin': {'?'},
        'association': {'?'},
        'auditoccupancy': {'?'},
        'backupset': {'?'},
        'backupsetcontents': {'?'},
        'cloptset': {'?'},
        'collocgroup': {'?'},
        'content': {'?'},
        'copygroup': {'?'},
        'datamover': {'?'},
        'db': {'?'},
        'dbbackuptrigger': {'?'},
        'dbvolume': {'?'},
        'devclass': {'?'},
        'dirspace': {'?'},
        'domain': {'?'},
        'drive': {'?'},
        'drmedia': {'?'},
        'drmstatus': {'?'},
        'enabled': {'?'},
        'event': {'?'},
        'eventrules': {'?'},
        'eventserver': {'?'},
        'export': {'?'},
        'filespace': {'?'},
        'library': {'?'},
        'libvolume': {'?'},
        'license': {'?'},
        'log': {'?'},
        'logvolume': {'?'},
        'machine': {'?'},
        'media': {'?'},
        'mgmtclass': {'?'},
        'mount': {'?'},
        'nasbackup': {'?'},
        'nodedata': {'?'},
        'nodegroup': {'?'},
        'occupancy': {'?'},
        'option': {'?'},
        'path': {'?'},
        'policyset': {'?'},
        'process': {'?'},
        'profile': {'?'},
        'proxynode': {'?'},
        'recoverymedia': {'?'},
        'request': {'?'},
        'restore': {'?'},
        'rpfcontent': {'?'},
        'rpfile': {'?'},
        'san': {'?'},
        'schedule': {'?'},
        'script': {'?'},
        'server': {'?'},
        'servergroup': {'?'},
        'session': {'?'},
        'shredstatus': {'?'},
        'spacetrigger': {'?'},
        'sqlsession': {'?'},
        'status': {'?'},
        'subscriber': {'?'},
        'subscription': {'?'},
        'system': {'?'},
        'tapealermsg': {'?'},
        'toc': {'?'},
        'virtualfsmapping': {'?'},
        'volhistory': {'?'},
        'volume': {'?'},
    },
    'quit': None,
})


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
    main()

