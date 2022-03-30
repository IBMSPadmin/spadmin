import re
import pexpect
import os
import datetime
import configparser
import getpass
import subprocess
from termcolor import colored
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit import PromptSession
from prompt_toolkit.cursor_shapes import CursorShape, ModalCursorShapeConfig


class Dsmadmc:
    "This is the DSMADMC wrapper class"
    START_DSMADMC = 'dsmadmc'  # Ezzel a paranccsal indítom a TSM klienst - csak Mac-en tesztelve!
    # TSM_PROMPT = 'Protect: USERTSM.USR>'  # ez azért fontos, mert itt áll meg a pexpect
    MORE = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    analyzer = None
    start = datetime.datetime.utcnow()

    def sendline(text):
        if Dsmadmc.analyzer is None or not Dsmadmc.analyzer.isalive():
            STARTCOMMAND = Dsmadmc.START_DSMADMC + " -id=" + id + " -pa=" + pa
            Dsmadmc.analyzer = pexpect.spawn('%s' % STARTCOMMAND, encoding='utf-8')
            Dsmadmc.analyzer.expect([prompt, Dsmadmc.MORE, Dsmadmc.MORE2])
            if not Dsmadmc.analyzer.isalive():
                print("Exception has occured, NO MORE respawn")
                print(highlight(Dsmadmc.analyzer.before))
                quit(1)
        columns, rows = os.get_terminal_size(0)
        Dsmadmc.analyzer.setwinsize(rows, columns)  ## hátha át lett méretezve az ablak
        Dsmadmc.analyzer.sendline(commandPreprocessor(text))  ## beküldjük a parancsot
        Dsmadmc.analyzer.expect(
            [prompt, Dsmadmc.MORE, Dsmadmc.MORE2, pexpect.EOF])  ## várjuk, hogy promptot vagy "MORE"-t kapjunk
        print(highlight(Dsmadmc.analyzer.before))  ## Highlighter-es kiíratás
        if Dsmadmc.analyzer.match_index == 1:
            commandline("more...   (<ENTER> to continue, 'C' to cancel)")
        if Dsmadmc.analyzer.match_index == 2:
            commandline("The character '#' stands for any decimal integer.")
        elif Dsmadmc.analyzer.match_index == 3:
            Dsmadmc.bye(None)
            quit();

    def bye(self):
        end_date = datetime.datetime.utcnow()
        print(colored('Thanks!', 'green'), colored('spadmin has run', 'white'),
              str(datetime.timedelta(seconds=abs((end_date - dsm.start).seconds))), colored('total', 'white'))


def highlight(text):
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


def commandPreprocessor(text):
    if text == 'sh actlog':
        return 'select DATE_TIME,MESSAGE from actlog WHERE (DATE_TIME>=current_timestamp-24 hour) order by 2 '
    return text


def commandline(prmpt):
    """Command line interface"""
    if not prmpt:
        text = session.prompt(
            prompt, completer=completer, complete_while_typing=False, cursor=CursorShape.BLINKING_BLOCK)
    else:
        text = session.prompt(
            prmpt, completer=completer, complete_while_typing=False,
            cursor=CursorShape.BLINKING_BLOCK)  # Prompt, history-val és completerrel.
    dsm.sendline(text)


def setup():
    config = configparser.ConfigParser()
    config.read('ispadmin.ini')
    global id
    global pa
    id = config['DEFAULT']['id']
    pa = config['DEFAULT']['password']
    if id is None or not id:
        id = input("Enter your user id: ")
    if pa is None or not pa:
        pa = getpass.getpass("Enter your password: ")
    try:
        result = subprocess.check_output(
            ['dsmadmc', '-id=%s' % id, '-pa=%s' % pa, '-dataonly=yes', 'select SERVER_NAME from STATUS'])
    except:
        print (
            "An error occured during the authentication, please check the error message above.")
        quit(1)
    if result:
        print ("PROMPT: ", result.decode("utf-8").strip())
        global prompt
        prompt = 'Protect: %s>' % result.decode("utf-8").strip()
    else:
        print (
            "An error occured during the authentication, please check your ISP connection, spadmin.ini file and/or userid-password pair")
        print (result.decode("utf-8"))
        quit(1)

    config['DEFAULT']['id'] = id
    config['DEFAULT']['password'] = pa

    with open('ispadmin.ini', 'w') as configfile:
        config.write(configfile)


def welcome():
    print('Let\'s start!')
    print(colored('Welcome at', 'green'), colored('spadmin!', 'red'))
    setup()


if __name__ == "__main__":
    """Main metódus"""
    welcome()
    session = PromptSession()
    dsm = Dsmadmc
    while True:
        commandline(None)
