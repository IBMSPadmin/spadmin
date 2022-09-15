import getpass
import platform
import utilities
import os.path

class Setup:
    def __init__(self):
        self.parameters = {'dsmadmc_id': "admin",
                           'dsmadmc_password': "admin",
                           'dsmadmc_path': "dsmadmc"}

        print("Welcome!")
        print("Before we start, you have to add some parameters to handle login for Spectrum Protect")
        if platform.system() == 'Darwin':
            self.parameters['dsmadmc_path'] = '/usr/local/bin/dsmadmc'
        elif platform.system() == 'Linux':
            self.parameters['dsmadmc_path'] = '/usr/bin/dsmadmc'
        else:
            print("Your \'", platform.system(), "\' platform is not supported. Sorry!")
            print("Please let us know, and we will port the application as-soon-as-possible to your platform.")
            quit(1)

        # Checking DSMADMC path
        if os.path.exists(self.parameters['dsmadmc_path']):
            print('We have found dsmadmc: ', self.parameters['dsmadmc_path'])
        else:
            found = False
            while not found:
                print(f'We did not find dsmadmc on it\'s default place. \'{self.parameters["dsmadmc_path"]}\'.')
                self.parameters['dsmadmc_path'] = input("Please type your dsmadmc path: ")
                if os.path.exists(self.parameters['dsmadmc_path']):
                    found = True

        # Checking USERID and PASSWORD
        allowed = False
        while not allowed:
            self.parameters['dsmadmc_id'] = input("Enter your Spectrum Protect userid (eg. admin): ")
            self.parameters['dsmadmc_password'] = getpass.getpass(
                "Enter your password for user \'%s\' : " % self.parameters['dsmadmc_id'])
            allowed = utilities.check_connection('', self.parameters['dsmadmc_id'], self.parameters['dsmadmc_password'])

    def get_parameters(self):
        return self.parameters
