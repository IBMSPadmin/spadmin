import configparser
import getpass
import subprocess


class Configuration:
    id = None
    password = None
    prompt = None
    configparser = None

    def __init__(self, configfile):
        if not configfile:
            configfile = 'ispadmin.ini'
        self.configparser = configparser.ConfigParser()
        self.configparser.read(configfile)
        try:
            self.id = self.configparser['DEFAULT']['id']
            self.password = self.configparser['DEFAULT']['password']
        except:
            pass
        self.checklogin()

    def checklogin(self):
        if self.id is None or not self.id:
            self.id = input("Enter your user id: ")
        if self.password is None or not self.password:
            self.password = getpass.getpass("Enter your password: ")
        try:
            result = subprocess.check_output(
                ['dsmadmc', '-id=%s' % self.id, '-pa=%s' % self.password, '-dataonly=yes',
                 'select SERVER_NAME from STATUS'], stderr=subprocess.STDOUT, timeout=10,
                universal_newlines=True)

            self.prompt = 'Protect: %s>' % result.strip()
            self.writeconfig( self.id, self.password)
        except subprocess.CalledProcessError as exc:
            print(exc.output,"\nReturn code:", exc.returncode)
            print(
                "An error occured during the authentication, please check the error message above.")
            quit(1)

    def writeconfig(self, id, password):
        self.configparser['DEFAULT']['id'] = id
        self.configparser['DEFAULT']['password'] = password

        with open('ispadmin.ini', 'w') as configfile:
            self.configparser.write(configfile)
