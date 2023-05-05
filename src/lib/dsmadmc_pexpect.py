from re import search, MULTILINE, split
import pexpect
#import lib.utilities as utilities
from termcolor import colored
import sys
import readchar
from . import utilities
from . import globals


class dsmadmc_pexpect:
    STARTCOMMAND_TABDEL = None
    STARTCOMMAND = None
    MORE1 = 'more...   \(\<ENTER\> to continue, \'C\' to cancel\)'  # meg itt
    MORE2 = 'The character \'#\' stands for any decimal integer.'  # meg itt
    MORE3 = 'Do you wish to proceed\? \(Yes \(Y\)/No \(N\)\)'  # meg itt
    CONT = 'cont>'
    PROMPT1 = 'Protect: .*'
    PROMPT2 = 'tsm: .*'
    EXPECTATIONS = [PROMPT1, PROMPT2, MORE1, MORE2, MORE3, pexpect.EOF, pexpect.TIMEOUT,
                 'ANS8023E',
                 'Enter your password:', 'ANS1051I', CONT]
    tsm_tabdel = None
    tsm_normal = None
    nrOfRetry = 3

    def __init__(self, server, id, pa):
        globals.logger.debug('starting dsmadmc: [' + server + ' ' +id + ' ' + pa + ']')
        if not server:
            self.STARTCOMMAND_TABDEL = globals.config.getconfiguration()['SPADMIN']['dsmadmc_path'] + ' -NOConfirm' + ' -id=' + id + ' -pa=' + pa + ' -dataonly=yes' + ' -tabdel'
            self.STARTCOMMAND = globals.config.getconfiguration()['SPADMIN']['dsmadmc_path'] + ' -NOConfirm' + ' -id=' + id + ' -pa=' + pa
        else:
            self.STARTCOMMAND_TABDEL = globals.config.getconfiguration()['SPADMIN']['dsmadmc_path'] + ' -NOConfirm' + ' -se=' + server + ' -id=' + id + ' -pa=' + pa + ' -dataonly=yes' + ' -tabdel'
            self.STARTCOMMAND = globals.config.getconfiguration()['SPADMIN']['dsmadmc_path'] + ' -NOConfirm' + ' -se=' + server + ' -id=' + id + ' -pa=' + pa

    def get_tsm_tabdel(self):
        if self.tsm_tabdel is None or not self.tsm_tabdel.isalive:
            # debug purposes only:
            # print ("Spawn: ", self.STARTCOMMAND)
            self.tsm_tabdel = pexpect.spawn( '%s' % self.STARTCOMMAND_TABDEL, encoding='utf-8', echo=False, codec_errors='ignore', timeout=99999999)
            self.tsm_tabdel.setwinsize(65534, 65534)
            rc = self.tsm_tabdel.expect(self.EXPECTATIONS)
            self.check_rc(self.tsm_tabdel, rc)
        return self.tsm_tabdel

    def get_tsm_normal(self):
        if self.tsm_normal is None or not self.tsm_normal.isalive:
            self.tsm_normal = pexpect.spawn('%s' % self.STARTCOMMAND, encoding='utf-8', echo=False, codec_errors='ignore', timeout=99999999)
            self.tsm_normal.setwinsize(65534, globals.columns)
            rc = self.tsm_normal.expect(self.EXPECTATIONS)
            self.check_rc(self.tsm_normal, rc)
        return self.tsm_normal

    def send_command_tabdel(self, command):
        """
        Returns with a string
        """

        try:
            tsm = self.get_tsm_tabdel()
            # globals.logger.debug( 'DSMADMC tabdel pid: [' + str( tsm.pid ) + ']' )
            globals.logger.info("Command will be sent to dsmadmc: " + command)
            tsm.sendline(command)
            rc = self.tsm_tabdel.expect(self.EXPECTATIONS)
            self.check_rc(tsm, rc)
        except KeyboardInterrupt as e:
            sys.stdout.write("CTRL+C pressed  (Press any key to reset SP connection, or press 'C' to continue)")
            sys.stdout.flush()
            key = readchar.readkey()
            print()
            if str(key).lower() != "c":
                self.quit()
                self.tsm_tabdel = None
                self.tsm_normal = None
        except Exception as e:
            print('An error occurred during a dsmadmc execution:')
            print(tsm.before)
            print(str(e))
            print('Please check the connection parameters and restart spadmin')
            quit(1)

        return tsm.before

    def send_command_array_tabdel(self, command):
        """
        1. It executes a dsmadmc command
        2. splits the output line-by-line
        3. remove empty lines
        4. returns a list, where every line is an item
        """
        list = self.send_command_tabdel(command).splitlines()
        if globals.last_error['rc'] == "11":
            return []
        if len(list) > 0:
            list.pop(0)  # delete the first line which is the command itself
        while ("" in list):  ## every output contains empty lines, we remove it
            list.remove("")
        return list

    def send_command_array_array_tabdel(self, command):
        """
        1. It executes a dsmadmc command
        2. splits the output line-by-line
        3. remove empty lines
        4. returns a list of list, outter list is separated line-by-line, inner list is tab separated
        """
        
        onserver = '(' + globals.extras[ 'onserver' ][-1] + ') ' if 'onserver' in globals.extras else ''
        
        list = self.send_command_tabdel( onserver + command ).splitlines()
        ar = []
        if globals.last_error['rc'] != "0":
            print( utilities.color( globals.last_error['message'], "red") )
            # print("ANS8001I Return code: ", globals.last_error['rc'])
            return ar
        if len(list) > 0:
            list.pop(0)  # delete the first line which is the command itself
        while ("" in list):  ## every output contains empty lines, we remove it
            list.remove("")
        for i in list:
            if i.startswith('ANR1699I') or i.startswith('ANR1687I') or i.startswith('ANR1688I') or i.startswith('ANR1694I') or i.startswith('ANR1697I'):
                continue
            ar.append(split(r'\t', i))
        return ar

    def send_command_normal(self, command):

        try:
            tsm2 = self.get_tsm_normal()

            # globals.logger.debug('DSMADMC normal pid: [' + str(tsm2.pid) + ']')

            tsm2.sendline(command)
            rc = self.tsm_normal.expect(self.EXPECTATIONS)
            self.check_rc(tsm2, rc)
        except KeyboardInterrupt as e:
            sys.stdout.write("CTRL+C pressed  (Press any key to reset SP connection, or press 'C' to continue)")
            sys.stdout.flush()
            key = readchar.readkey()
            print()
            if str(key).lower() != "c":
                self.quit()
                self.tsm_tabdel = None
                self.tsm_normal = None

        except Exception as e:
            print('An error occurred during a dsmadmc execution:')
            print(tsm2.before)
            print(str(e))
            print('Please check the connection parameters and restart spadmin')
            quit(1)

        return tsm2.before

    def check_rc(self, tsm, rc):
        if rc == 6: # Timeout
            print('Timeout occured.')
            print('Please check the connection parameters and restart spadmin')
            print( tsm.before[ :50 ] )
            quit(1)
        elif rc == 7: #  ANS8023E Unable to establish session with server.
            print('TCP/IP connection failure.')
            print('Please check the connection parameters and restart spadmin')
            print(tsm.before)
            quit(1)
        elif rc == 8 or rc == 9: # ANS1051I Invalid user id or password
            print('Invalid user id or password.')
            print('Please check the connection parameters and restart spadmin')
            print(tsm.before)
            quit(1)
        elif rc == 10: # Cont>
            print("Continue the command in the next line, please: ")

        groups = search("ANS8001I Return code (\d+).", tsm.before, MULTILINE )
        if groups:
            globals.last_error = {'rc': groups[1], 'message': tsm.before.splitlines()[2]}
        else:
            globals.last_error = {'rc': "0", 'message': ''}


    def quit(self):
        globals.logger.debug('DSMADMC normal quit.')
        self.send_command_normal('quit')
        globals.logger.debug('DSMADMC tabdel quit.')
        self.send_command_tabdel('quit')