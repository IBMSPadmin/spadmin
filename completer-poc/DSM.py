import re
import pexpect
import logging

class DSM:
    STARTCOMMAND = None
    MORE1 = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    MORE3 = 'Do you wish to proceed\? \(Yes \(Y\)/No \(N\)\)'  # meg itt
    PROMPT1 = 'Protect: .*'
    PROMPT2 = 'tsm: .*'
    tsm = None

    def __init__(self, id, pa):
        self.STARTCOMMAND = 'dsmadmc' + ' -id=' + id + ' -pa=' + pa + ' -dataonly=yes' + ' -tabdel'

    def get_tsm(self):

        if self.tsm is None or not self.tsm.isalive:
            #debug purposes only: print ("Spawn: ", self.STARTCOMMAND)
            self.tsm = pexpect.spawn('%s' % self.STARTCOMMAND, encoding='utf-8', echo=False)
            self.tsm.setwinsize(65534, 65534)
            rc = self.tsm.expect(
                [self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF, pexpect.TIMEOUT,
                 'ANS8023E',
                 'Enter your password:', 'ANS1051I'])
            if rc == 6:
                print('Timeout occured.')
                print('Please check the connection parameters and restart spadmin')
                print(self.tsm.before)
                quit(1)
            if rc == 7:
                print('TCP/IP connection failure.')
                print('Please check the connection parameters and restart spadmin')
                print(self.tsm.before)
                quit(1)
            if rc == 8 or rc == 9:
                print('Invalid user id or password.')
                print('Please check the connection parameters and restart spadmin')
                print(self.tsm.before)
                quit(1)
        return self.tsm

    def send_command(self, command):

        tsm = self.get_tsm()

        logging.info(' DSMADMC pid: [' + str(tsm.pid) + ']')

        try:
            tsm.sendline(command)
        except:
            print('An error occurred during a dsmadmc execution:')
            print(tsm.before)
            print('Please check the connection parameters and restart spadmin')
            quit(1)

        rc = self.tsm.expect(
            [self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF, pexpect.TIMEOUT, 'ANS8023E',
             'Enter your password:', 'ANS1051I'])
        if rc == 6:
            print('Timeout occured.')
            print('Please check the connection parameters and restart spadmin')
            print(tsm.before)
            quit(1)
        if rc == 7:
            print('TCP/IP connection failure.')
            print('Please check the connection parameters and restart spadmin')
            print(tsm.before)
            quit(1)
        if rc == 8 or rc == 9:
            print('Invalid user id or password.')
            print('Please check the connection parameters and restart spadmin')
            print(tsm.before)
            quit(1)
        return tsm.before

    def send_command_array(self, command):
        """
        1. It executes a dsmadmc command
        2. splits the output line-by-line
        3. remove empty lines
        4. returns a list, where every line is an item
        """
        list = self.send_command(command).splitlines()
        if len(list) > 0:
            list.pop(0)  # delete the first line which is the command itself
        while ("" in list):  ## every output contains empty lines, we remove it
            list.remove("")
        return list

    def send_command_array_array(self, command):
        """
        1. It executes a dsmadmc command
        2. splits the output line-by-line
        3. remove empty lines
        4. returns a list of list, outter list is separated line-by-line, inner list is tab separated
        """
        list = self.send_command(command).splitlines()
        ar = []
        if len(list) > 0:
            list.pop(0)  # delete the first line which is the command itself
        while ("" in list):  ## every output contains empty lines, we remove it
            list.remove("")
        for i in list:
            ar.append(re.split(r'\t', i))
        return ar


