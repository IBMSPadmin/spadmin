from re import search
import pexpect
import logging

class DSM2:
    STARTCOMMAND = None
    MORE1 = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    MORE3 = 'Do you wish to proceed\? \(Yes \(Y\)/No \(N\)\)'  # meg itt
    PROMPT1 = 'Protect: .*'
    PROMPT2 = 'tsm: .*'
    tsm = None

    def __init__(self, id, pa):
        self.STARTCOMMAND = 'dsmadmc' + ' -id=' + id + ' -pa=' + pa

    def get_tsm2(self):

        if self.tsm is None or not self.tsm.isalive:
            self.tsm = pexpect.spawn('%s' % self.STARTCOMMAND, encoding='utf-8', echo=False)
            self.tsm.setwinsize(65534, 120)
            self.tsm.expect(
                [self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF, pexpect.TIMEOUT])

        return self.tsm

    def send_command2(self, command):

        tsm = self.get_tsm2()

        logging.info(' DSMADMC pid2: [' + str(tsm.pid) + ']')

        try:
            tsm.sendline(command)
        except:
            print('An error occurred during a dsmadmc execution. Please try again...')
            print( tsm.before)
            quit(1)

        try:
            tsm.expect([self.PROMPT1, self.PROMPT2, self.MORE1, self.MORE2, self.MORE3, pexpect.EOF, pexpect.TIMEOUT])
        except:
            print('An error occurred during a dsmadmc execution. Please try again...')

        # Session established with server CLOUDTSM1: Linux/x86_64
        # Server Version 8, Release 1, Level 7.000
        # Server date/time: 08/20/2022 19:12:44  Last access: 08/20/2022 16:48:38

        # Let's dance
        ret = []
        for i in tsm.before.splitlines()[1:]:
            if search('^Session established with server \w+:', i):
                continue
            elif search('^\s\sServer Version \d+, Release \d+, Level \d+.\d\d\d', i):
                continue
            elif search('^\s\sServer date\/time\:', i):
                continue

            ret.append(i)

        return ret
