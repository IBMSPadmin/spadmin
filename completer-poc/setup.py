import getpass
import platform
from typing import Dict, List

import utilities
import os.path


def ask_yesno(question):
    """
    Get yes / no answer from user.
    """
    yes = {'yes', 'y'}
    no = {'no', 'n'}

    done = False
    print(question)
    while not done:
        choice = input().lower()
        if choice in yes:
            return True
        elif choice in no:
            return False
        else:
            print("Please respond by yes or no.")


class Setup:
    def __call__(self) -> List:
        parameters = {'dsmadmc_id': "admin",
                      'dsmadmc_password': "admin",
                      'dsmadmc_path': "dsmadmc"}

        print("Welcome!")
        print("Before we start, you have to add some parameters to handle login for Spectrum Protect")
        if platform.system() == 'Darwin':
            parameters['dsmadmc_path'] = '/usr/local/bin/dsmadmc'
        elif platform.system() == 'Linux':
            pass
        else:
            print("Your \'", platform.system(), "\' platform is not supported. Sorry!")
            print("Please let us know, and we will port the application as-soon-as-possible to your platform.")
            quit(1)

        # Checking DSMADMC path
        if os.path.exists(parameters['dsmadmc_path']):
            print('We have found dsmadmc: ', parameters['dsmadmc_path'])
        else:
            found = False
            while not found:
                print(f'We did not find dsmadmc on it\'s default place. \'{parameters["dsmadmc_path"]}\'.')
                parameters['dsmadmc_path'] = input("Please type your dsmadmc path: ")
                if os.path.exists(parameters['dsmadmc_path']):
                    found = True

        # Checking USERID and PASSWORD
        allowed = False
        while not allowed:
            parameters['dsmadmc_id'] = input("Enter your Spectrum Protect userid (eg. admin): ")
            parameters['dsmadmc_password'] = getpass.getpass(
                "Enter your password for user \'%s\' : " % parameters['dsmadmc_id'])
            allowed = utilities.check_connection('', parameters['dsmadmc_id'], parameters['dsmadmc_password'])

        return parameters