from ispadmin.configuration import Configuration
from ispadmin.dsmadmc import Dsmadmc
from termcolor import colored


def welcome():
    print('Let\'s start!')
    print(colored('Welcome at', 'green'), colored('spadmin!', 'red'))


if __name__ == "__main__":
    """Main metódus"""
    welcome()

    dsm = Dsmadmc(Configuration("ispadmin.ini"))
    while True:
        dsm.commandline(None)
