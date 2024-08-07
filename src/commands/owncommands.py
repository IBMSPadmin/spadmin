import re
import sys

sys.path.append("..")
import logging
import os
import sys
from pprint import pprint
from re import search, sub, IGNORECASE
from termcolor import colored
import lib.globals as globals
import lib.utilities as utilities
import lib.humanbytes as humanbytes
import lib.columnar as columnar
from operator import itemgetter
from lib.IBMSPrlCompleter import IBMSPrlCompleter

import datetime
import glob
import json
import readchar

from time import time

columnar = columnar.Columnar()  # columnar: table creator/formatter utility
spadmin_commands = {}  # dictionary for the spadmin commands
disabled_words = ['DEFAULT', 'ALIAS', 'SPADMIN', 'BACK']  # disabled words: used in the configuration .ini file
globals.lastdsmcommandtype = '?'  # last command type: used by "kill", "on", "off", etc. commands
globals.lastdsmcommandresults = ['']  # last command result: used by "kill", "on", "off", etc. commands
command_type_and_index = {}
command_free_and_index = {}
command_help = {}

class SpadminCommand:
    """
    This is the interface class for every Spadmin Command
    """

    def __init__(self):
        self.command_string = ""
        self.command_type = ""
        self.command_index = 0
        self.command = "FREE" # Can be "FREE", "INTERNAL" or "PAY"

    def get_command_string(self):
        return self.command_string

    def get_command_type(self):
        return self.command_type

    def get_command_index(self):
        return self.get_command_index

    def short_help(self) -> str:
        return ''

    def help(self) -> str:
        return ""

    def _execute(self, parameters: str) -> str:
        return "not defined: " + parameters

    def execute(self, dummy, parameters):
        globals.logger.debug(
            "Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            utilities.printer(self._execute(parameters))
        globals.lastdsmcommandtype = self.get_command_type()
        globals.logger.debug(
            "Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")


def dynruleinjector( command ):  # it works only for commands which longer than 2 words!! on 1 word command needs to be added to the rules file.
    commandpartcollected = ''
    for commandpart in command.split()[:-1]:
        commandpartcollected += commandpart
        if commandpartcollected not in globals.myIBMSPrlCompleter.dynrules:
            globals.myIBMSPrlCompleter.dynrules[commandpartcollected] = []
        commandpartcollected += ' '

    commandpartcollected = command.split()
    for commandpart in command.split()[:-1]:
        rightpart = commandpartcollected.pop(-1)
        leftpart = ' '.join(commandpartcollected)
        if rightpart not in globals.myIBMSPrlCompleter.dynrules[leftpart]:
            globals.myIBMSPrlCompleter.dynrules[leftpart].append(rightpart)

    if len(command.split()) == 1 and command not in IBMSPrlCompleter.start:
        IBMSPrlCompleter.start.append(command)


# INIT -------------------------------------------------------------------
# Fill up with the servernames
for section in globals.config.getconfiguration().sections():
    if section not in disabled_words:
        dynruleinjector( 'SPadmin DELete SErver ' + section )
        dynruleinjector( 'SPadmin SWitch SErver ' + section )
        
# # load aliases
if globals.config.getconfiguration().has_section( 'ALIAS' ):
    for key in globals.config.getconfiguration()[ 'ALIAS' ].keys():
        dynruleinjector( 'SPadmin DELete ALIas ' + key.replace( ' ', '_' ) )
# ------------------------------------------------------------------------


def help(command_name):
    print(command_help[command_name])


def define_own_command(command_string, function_address, command_type, index, short_help, help, command_free):
    spadmin_commands[command_string]       = function_address
    dynruleinjector(command_string)
    command_type_and_index[command_string] = [command_type, index]
    command_help[command_string]           = [short_help, help]
    command_free_and_index[command_string] = [command_free, index]

def define_command(clazz: SpadminCommand):
    if clazz.command == "PAY" and globals.licensed == False:
        return
    define_own_command(clazz.get_command_string(), clazz.execute, clazz.get_command_type(), clazz.get_command_index(),
                       clazz.short_help(), clazz.help(), clazz.command)

def timemachine_query( command_type, query ):
        
    tm = globals.extras[ 'timemachine' ] if 'timemachine' in globals.extras else ''
    
    if tm == '':
    
        data = globals.tsm.send_command_array_array_tabdel( query )
    
        if globals.last_error[ 'rc' ] != '0':
            #print(utilities.color(globals.last_error["message"], 'red'))
            return
    
        with open( os.path.join( globals.spadmin_tmpath, datetime.datetime.now().strftime( globals.spservername + '_' + command_type + '_%Y%m%d_%H%M%S.json' ) ), 'w' ) as fp:
            json.dump( data, fp )  # save into JSON file
    
        return data
    
    else:
        
        print( 'Built-in Time Machine feature was invoked...' )
        
        files = glob.glob( globals.spadmin_tmpath + '/' + globals.spservername + '_' +  command_type + '*.json' )
        files.sort( reverse=True )
        
        if len( files ) == 0:
            print( utilities.color( 'No Time Machine data exists for: ' + command_type + ' queries!', 'red' ) )
            return []
            
            # 27, 91, 65 66 68< 67>
            # esc 27
            # 106j 74J
            # 107k 75K
            # 111o 
            
        # browser 
        index     = 0
        lastindex = len( files ) - 1
        pathlen   = len( globals.spadmin_tmpath + '/' + globals.spservername + '_' + command_type ) + 1
        
        while True:
            sys.stdout.write( '<jJ o Kk> [' + files[index][ pathlen:-5 ] + ']\r' )
            sys.stdout.flush()
            key = readchar.readkey() 
            if len( key ) == 3:
                if ord( key[0] ) == 27 and ( ord( key[1] ) == 91 or ord( key[1] ) == 79 ) and ord( key[2] ) == 68:
                    if index > 0:
                        index -= 1
                elif ord( key[0] ) == 27 and ( ord( key[1] ) == 91 or ord( key[1] ) == 79 ) and ord( key[2] ) == 67:
                    if index < lastindex:
                        index += 1
            if len ( key ) == 2:
                if ord( key[0] ) == 27 and ord( key[0] ) == 27:
                    break
            if len ( key ) == 1:
                if ord( key[0] ) == 106 or ord( key[0] ) == 74:
                    if index > 0:
                        index -= 1
                elif ord( key[0] ) == 107 or ord( key[0] ) == 75:
                    if index < lastindex:
                        index += 1
                elif ord( key[0] ) == 111 or ord( key[0] ) == 10:
                    break
        
        print( 'Selected date: [' + utilities.color( files[index][ pathlen:-5 ], "white" ) + '].' )
        
        with open( files[index], 'r' ) as fp:
             # Load the dictionary from the file
             data = json.load( fp )
        
        globals.last_error[ 'rc' ] = '0'
        
        return data
        
        # https://pynative.com/python-save-dictionary-to-file/


class SPadminAddALIas(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin Add ALIas"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Creates an alias'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if len(str(parameters).split(':')) < 2:
            print('Please use the following command format: \'SPadmin Add ALIas cmd:command\'')
            return
        else:
            key, value = str(parameters).split(':', 1)
            key = key.strip()
            value = value.strip()
            globals.aliases[key] = value
            globals.config.getconfiguration()['ALIAS'][key] = value
            globals.config.writeconfig()
            dynruleinjector( key )
            dynruleinjector( 'SPadmin DELete ALIas ' + key )
            #globals.myIBMSPrlCompleter.dynrules['SPadmin Add ALIas'].append(key)
        return ""


define_command(SPadminAddALIas())


class SPadminAddSErver(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin Add SErver"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Add new Spectrum Protect server connection'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if len(str(parameters).split(' ')) != 3:
            print('Please use the following command format: \'SPadmin Add SErver server_name user_id password\'')
            return
        else:
            server, userid, password = str(parameters).split(' ')
            server = str(server).upper()
            if globals.config.getconfiguration().has_section(server) or server in disabled_words:
                print(f'The given server name \'{server}\' already exists or not allowed')  #
            else:
                if utilities.check_connection(server, userid, password):
                    globals.config.getconfiguration().add_section(server)
                    globals.config.getconfiguration()[server]['dsmadmc_id'] = userid
                    globals.config.getconfiguration()[server]['dsmadmc_password'] = utilities.encode(password)
                    globals.config.writeconfig()
                    dynruleinjector('SPadmin SWitch SErver ' + server)
                    dynruleinjector('SPadmin DELete SErver ' + server)
                else:
                    print('Server parameters not saved!')

        return ""


define_command(SPadminAddSErver())


class SPadminDELeteSErver(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin DELete SErver"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Removes Spectrum Protect connection'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if not parameters:
            print('Please use the following command format: \'SPadmin DELete SErver servername\'')
            return
        else:
            server = str(parameters).upper()
            if globals.config.getconfiguration().has_section(server) and parameters not in disabled_words:
                globals.config.getconfiguration().pop(server)
                globals.config.writeconfig()
                globals.myIBMSPrlCompleter.rules['SPadmin DELete SErver'].remove(server)

            else:
                print(f'The given server \'{server}\' not found')
        ###EZ MIÉRT VAN?????:
        for section in globals.config.getconfiguration().sections():
            if section not in disabled_words:
                dynruleinjector('SPadmin DELete SErver ' + section)
        return ""


define_command(SPadminDELeteSErver())


class SPadminSWitchSErver(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SWitch SErver"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Switches between Spectrum Protect servers'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if not parameters or str(parameters).upper() == 'BACK':
            print('Switch back to the default server...')
            globals.server = ''
            globals.tsm.closeconnections()
            from lib.dsmadmc_pexpect import dsmadmc_pexpect
            globals.userid = globals.config.getconfiguration()['SPADMIN']['dsmadmc_id']
            globals.password = utilities.decode(globals.config.getconfiguration()['SPADMIN']['dsmadmc_password'])
            globals.tsm = dsmadmc_pexpect('', globals.userid, globals.password)
            globals.spversion, globals.sprelease, globals.splevel, globals.spsublevel = \
                globals.tsm.send_command_array_array_tabdel('select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS')[0]
            globals.spservername = globals.tsm.send_command_array_tabdel('select SERVER_NAME from STATUS')[0]
            return ""
        else:
            print("Switching Server...")
            server = str(parameters).upper()
            if globals.config.getconfiguration().has_section(server) and str(parameters).upper() not in disabled_words:
                globals.tsm.closeconnections()
                from lib.dsmadmc_pexpect import dsmadmc_pexpect
                globals.server = server
                globals.userid = globals.config.getconfiguration()[server]['dsmadmc_id']
                globals.password = utilities.decode(globals.config.getconfiguration()[server]['dsmadmc_password'])
                globals.tsm = dsmadmc_pexpect(server, globals.userid, globals.password)
                globals.spversion, globals.sprelease, globals.splevel, globals.spsublevel = \
                globals.tsm.send_command_array_array_tabdel('select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS')[0]
                globals.spservername = globals.tsm.send_command_array_tabdel('select SERVER_NAME from STATUS')[0]

            else:
                print(f'The given server \'{server}\' not found')
        return ""

define_command(SPadminSWitchSErver())


class SPadminSHowCONFig(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow CONFig"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin settings'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []

        for configclass in globals.config.getconfiguration():
            for variable in globals.config.getconfiguration()[configclass]:
                data.append([configclass, variable, '=', globals.config.getconfiguration()[configclass][variable]])
        return columnar(data, headers=[utilities.color('Class', "white"),
                                                  utilities.color('Variable', "white"),
                                                  utilities.color('=', "white"),
                                                  utilities.color('Value', "white")],
                                   justify=['l', 'l', 'l', 'l'])


define_command(SPadminSHowCONFig())

class SPadminSHowALIases(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow ALIases"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin aliases'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        for key in globals.aliases:
            data.append([key, globals.aliases[key]])
        return columnar(data, headers=[utilities.color('Alias', "white"),
                                                  utilities.color('Command', "white")], justify=['l', 'l'])

define_command(SPadminSHowALIases())


class SPadminSHowVERsion(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow VERsion"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin version'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        data.append( [ globals.version ] )
        
        return columnar( data, 
                         headers=[ utilities.color( 'spadmin.py version', "white" ) ],
                         justify=[ 'r' ] )

define_command(SPadminSHowVERsion())


class SPadminSETDEBUG(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SET DEBUG"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Turn DEBUG level logging on'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        print('Debug is set to ON. The pervious debug level was: [' + logging.getLevelName(
            globals.logger.getEffectiveLevel()) + '].')
        globals.logger.setLevel(logging.DEBUG)

        return ""

define_command(SPadminSETDEBUG())


class SPadminUNSETDEBUG(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin UNSET DEBUG"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Turn DEBUG level logging off'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        print('Debug is set to OFF. The pervious debug level was: [' + logging.getLevelName(
            globals.logger.getEffectiveLevel()) + '].')
        globals.logger.setLevel(logging.INFO)
        return ""

define_command(SPadminUNSETDEBUG())


class SPadminSHowRULes(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow RULes"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin rules'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:

        min = 0
        max = 99

        match = search(r'(\d+)\s+(\d+)', parameters)
        if match:
            min = int(match[1])
            max = int(match[2])
        else:
            match = search(r'(\d+)', parameters)
            if match:
                min = int(match[1])

        # swap variables
        if min > max:
            min, max = max, min

        data = []
        for key in globals.myIBMSPrlCompleter.rules:
            if globals.myIBMSPrlCompleter.rules[key]:
                rulelength = len(key.split())
                if rulelength >= min and rulelength <= max:
                    data.append([key, rulelength, globals.myIBMSPrlCompleter.rules[key]])

        return columnar(sorted(data, key=lambda x: x[1]),
                                   headers=['Regexp', 'LVL', 'Value'],
                                   justify=['l', 'c', 'l'])

define_command(SPadminSHowRULes())


class SPadminSHowLOG(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow LOG"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin logfile'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system( '/mnt/c/Windows/notepad.exe ' + globals.logfilename )
        elif sys.platform == "darwin":
            os.system( 'open ' + globals.logfilename )

        return ""

define_command(SPadminSHowLOG())


class SPadminSHowPRocessinfo(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow PRocessinfo"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin\'s dsmadmc processes'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = [["Normal", globals.tsm.get_tsm_normal().pid], ["Tabdelimited", globals.tsm.get_tsm_tabdel().pid]]
        table = columnar(data,
                         headers=['dsmadmc', 'PID'], justify=['l', 'cl'])
        return table

define_command(SPadminSHowPRocessinfo())


class SPadminDELeteALIas(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin DELete ALIas"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Semoves spadmin alias'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if not parameters:
            print('Please use the following command format: \'SPadmin DELete ALIas cmd\'')
            return
        else:
            parameters = parameters.strip()
            if parameters in globals.config.getconfiguration()['ALIAS']:
                globals.aliases.pop(parameters)
                globals.config.getconfiguration()['ALIAS'].pop(parameters)
                globals.config.writeconfig()
                globals.myIBMSPrlCompleter.rules['SPadmin DELete ALIas'].remove(parameters)
            else:
                print(f'The given alias \'{parameters}\' not found')
        return ""

define_command(SPadminDELeteALIas())


class SPadminSHowSErver(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow SErvers"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows Spectrum Protect connections'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        
        for section in globals.config.getconfiguration().sections():
            if section not in disabled_words:
                data.append( [ section ] )

        return columnar( data, 
                         headers=[ utilities.color( 'Server(s)', "white") ],
                         justify=[ 'r' ] )

define_command(SPadminSHowSErver())


class SPadminSHowCOMmands(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow COMmands"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "FREE"

    def short_help(self) -> str:
        return 'Shows spadmin commands'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        for key in spadmin_commands:
            desc = ""
            type = ""
            if key in command_help:
                desc = command_help[key][0]
                type = command_type_and_index[key][0]
                free = command_free_and_index[key][0]
            data.append([key, type, desc, free])

        return columnar(sorted(data, key=itemgetter(0)), headers=[
            utilities.color('Command name', "white"), 'Type', utilities.color('Short Description', "white"), 'Free'],
                        justify=['l', 'c', 'l', 'c'])

define_command(SPadminSHowCOMmands())


class SHowACTlog(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "ACTlog"
        self.command_type = "ACTLOG"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows the activity log'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = None
        if parameters is None or parameters == '' or parameters == []:
            data = globals.tsm.send_command_array_array_tabdel("q actlog")
        else:
            data = globals.tsm.send_command_array_array_tabdel(str(''.join(["q actlog ", " ".join([parameters])])))

        if globals.last_error[ 'rc' ] != '0':
            return

        data2 = []
        for index, row in enumerate(data):

            if search(r'^AN[ER]\d{4}E', row[1]):
                message = utilities.color(row[1], 'red')
            elif search(r'^ANR\d{4}W', row[1]):
                message = utilities.color(row[1], 'yellow')
            else:
                message = row[1]

            data2.append([row[0], message])

        return columnar(data2,
                        headers=['Date/Time', 'Message'],
                        justify=['l', 'l'])

define_command(SHowACTlog())




# Temporary test 
# SHow ACTlog           -> "process:
# SHow ACTlog "process: -> select process_num from processes
dynruleinjector( 'SHow ACTlog ' + '"search=process:' )
globals.myIBMSPrlCompleter.dynrules['SHow ACTlog "search=process:'] = []
globals.myIBMSPrlCompleter.dynrules['SHow ACTlog "search=process:'].append('select process_num from processes')


class SHowTEST(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "TEST"
        self.command_type = "ACTLOG"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows the activity log'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = globals.tsm.send_command_array_array_tabdel("select * from backups")

        if globals.last_error[ 'rc' ] != '0':
            return

        return data

define_command(SHowTEST())


class REload(SpadminCommand):

    def __init__(self):
        self.command_string = "REload"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Reload spadmin rule file'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        globals.myIBMSPrlCompleter.loadrules()
        return ""

define_command(REload())


class HISTory(SpadminCommand):

    def __init__(self):
        self.command_string = "HISTory"
        self.command_type = "HISTORY"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows command line history'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        rlhistfile = os.path.join( globals.spadmin_path, globals.config.getconfiguration()['SPADMIN']['historyfile'])
        globals.logger.debug('history file open: [' + rlhistfile + ']')
        if os.path.exists(rlhistfile):
            globals.logger.debug('history file open: [' + rlhistfile + ']')
            f = open(rlhistfile, "r")
            count = 0
            for line in f.readlines():
                count += 1
                data.append([count, line.strip()])
        return columnar(data,
                        headers=[utilities.color('#', "white"), utilities.color('Command', "white")],
                        justify=['r', 'l'])

define_command(HISTory())


class SpadminShowCache(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow CAche"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows spadmin SQL cache'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        for key in globals.myIBMSPrlCompleter.cache_hitratio:
            data.append([key, globals.myIBMSPrlCompleter.cache_hitratio[key]])
        utilities.printer(columnar( data, 
                                    headers=[ utilities.color( 'Name', "white" ), utilities.color( 'Value', "white" ) ], 
                                    justify=[ 'l', 'c' ] ) )

        data.clear()
        for key in globals.myIBMSPrlCompleter.cache:

            timediff = int(globals.config.getconfiguration()['SPADMIN']['cache_age']) - int(
                time() - globals.myIBMSPrlCompleter.cache_timestamp[key])
            if timediff > 0:
                timediff = utilities.color(humanbytes.HumanBytes.format(int(timediff), unit="TIME_LABELS", precision=0), 'green' )
            else:
                timediff = utilities.color(humanbytes.HumanBytes.format(int(timediff), unit="TIME_LABELS", precision=0), 'red' )

            data.append( [ key.strip(), timediff, globals.myIBMSPrlCompleter.cache[key] ] )
        
        return columnar( data, 
                         headers=[ utilities.color( 'Query', "white" ), utilities.color( 'Time',  "white" ), utilities.color( 'Result', "white" ) ], 
                         justify=[ 'l', 'c', 'l' ] )

define_command(SpadminShowCache())


class SHowLASTerror(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow LASTerror"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows the last error message and error code by dsmadmc'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        print("Last error message: ", globals.last_error["message"])
        print("Last return code: ", globals.last_error["rc"])
        return ""

define_command(SHowLASTerror())


class SPadminSHowEXtras(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow EXtras"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Print given line'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        print('CLI extra pipe parameter tester')
        pprint(globals.extras)
        return ""

define_command(SPadminSHowEXtras())


class PRint(SpadminCommand):

    def __init__(self):
        self.command_string = "PRint"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Print given line'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        
        data = []
        data.append( [ parameters ] )
        
        return columnar( data, 
                         headers = [ 'Text' ],
                         justify = [ 'l' ] )

define_command(PRint())


class SHowSESsions(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "SESsions"
        self.command_type  = "SESSIONS"
        self.command_index = 0
        self.command       = "FREE"

    def short_help(self) -> str:
        return 'Shows session informations like Query SEssions'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        
        data = timemachine_query( self.command_type, 'select SESSION_ID, STATE, WAIT_SECONDS, BYTES_SENT, BYTES_RECEIVED, SESSION_TYPE, CLIENT_PLATFORM, CLIENT_NAME,MOUNT_POINT_WAIT, INPUT_MOUNT_WAIT, INPUT_VOL_WAIT, INPUT_VOL_ACCESS, OUTPUT_MOUNT_WAIT, OUTPUT_VOL_WAIT, OUTPUT_VOL_ACCESS, LAST_VERB, VERB_STATE from sessions order by 1')
        
        if globals.last_error[ 'rc' ] != '0':
            return
        
        data2 = []
        for index, row in enumerate(data):

            if row[1] == 'Run':
                #state = utilities.color(row[1], 'green', attrs=[globals.color_attrs_bold])
                state = utilities.color(row[1], 'green')
            else:
                state = row[1]

            if int(row[2]) > 60:
                # wait = utilities.color(humanbytes.HumanBytes.format(int(row[2]), unit="TIME_LABELS", precision=0), globals.color_red,
                #               attrs=[globals.color_attrs_bold])
                wait = utilities.color(humanbytes.HumanBytes.format(int(row[2]), unit="TIME_LABELS", precision=0), globals.color_red)
            else:
                wait = humanbytes.HumanBytes.format(int(row[2]), unit="TIME_LABELS", precision=0)

            bytes_sent = humanbytes.HumanBytes.format(int(row[3]), unit="BINARY_LABELS", precision=0)
            bytes_received = humanbytes.HumanBytes.format(int(row[4]), unit="BINARY_LABELS", precision=0)

            # mediaaccess = ''.join( row[ 8:14 ] )
            match = search(r'(\w+),(.+),(\d+)', row[11])
            if match:
                # row[11] = 'Read: ' + utilities.color(match[2], 'green', attrs=[globals.color_attrs_bold]) + ', ' + match[
                #    1] + ', ' + humanbytes.HumanBytes.format(int(match[3]), unit="TIME_LABELS", precision=0)
                row[11] = 'Read: ' + utilities.color(match[2], 'green') + ', ' + match[
                    1] + ', ' + humanbytes.HumanBytes.format(int(match[3]), unit="TIME_LABELS", precision=0)

            match = search(r'(\w+),(.+),(\d+)', row[14])
            if match:
                # row[14] = 'Write: ' + utilities.color(match[2], 'green', attrs=[globals.color_attrs_bold]) + ', ' + match[
                #    1] + ', ' + humanbytes.HumanBytes.format(int(match[3]), unit="TIME_LABELS", precision=0)
                row[14] = 'Write: ' + utilities.color(match[2], 'green') + ', ' + match[
                    1] + ', ' + humanbytes.HumanBytes.format(int(match[3]), unit="TIME_LABELS", precision=0)

            mediaaccess = row[8] + row[9] + row[10] + row[11] + row[12] + row[13] + row[14]
            mediaaccess = mediaaccess.lstrip( ',' )
            # mediaaccess = sub( '(\w+)\,(\d+)', lambda m: utilities.color(m.group(1), 'green', attrs=[globals.color_attrs_bold]) + ' (' + humanbytes.HumanBytes.format( int( m.group(2) ), unit="TIME_LABELS", precision=0 ) + ')', mediaaccess)
            mediaaccess = sub( r'(\w+)\,(\d+)', lambda m: utilities.color(m.group(1), 'green') + ' (' + humanbytes.HumanBytes.format( int( m.group(2) ), unit="TIME_LABELS", precision=0 ) + ')', mediaaccess)

            data2.append(
                [index + 1, row[0], state, wait, bytes_sent, bytes_received, row[5], row[6], row[7], mediaaccess,
                 row[16] + row[15]])

        globals.lastdsmcommandresults = data2
        return columnar(data2, headers=[
            '#', 'Id', 'State', 'Wait', 'Sent', 'Received', 'Type', 'Platform', 'Name', 'MediaAcc', 'Verb'],
                        justify=['r', 'c', 'c', 'r', 'r', 'r', 'r', 'c', 'l', 'l', 'l'])


define_command(SHowSESsions())


class SHowPRocesses(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "PRocesses"
        self.command_type = "PROCESSES"
        self.command_index = 0
        self.command = "FREE"

    def short_help(self) -> str:
        return 'Show process informations, like Query PRocess'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = timemachine_query( self.command_type,
            'select PROCESS_NUM, PROCESS, FILES_PROCESSED, BYTES_PROCESSED, STATUS from processes order by 1')

        if globals.last_error['rc'] != '0':
            globals.lastdsmcommandtype = 'PROCESSES'
            globals.lastdsmcommandresults = []
            return

        data2 = []
        for index, row in enumerate(data):
            bytes_prcessed = humanbytes.HumanBytes.format(int(row[3]), unit="BINARY_LABELS", precision=0)

            # Current input volume: MKP056M8. Current output volume(s): MKP074M8.
            status = row[4]
            status = sub(r'(Current input volume: )([\w\/\.]+)(\.)',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Current input volumes: )([\w\/,\.]+)(\()',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Current input volumes: )([\w\/,\.]+)(\([\w ]+\))([\w\/,\.]+)(\()',
                         # Current input volumes: MKP002M8,(33772 Seconds)MKP049M8,(15618 Seconds)
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3) + utilities.color(
                             m.group(4), 'green') + m.group(5), status)
            status = sub(r'(Current output volume\(' + r's\): )([\w\/\.]+)(\.)',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Current output volumes: )([\w\/,\.]+)(\()',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Waiting for mount of input volume )([\w\/]+)( \()',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Waiting for mount of output volume )([\w\/,]+)( \()',
                         # Waiting for mount of input volume 000006L4 (3 seconds)
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Volume )([\w\/]+)( \()',
                         lambda m: m.group(1) + utilities.color(m.group(2), 'green') + m.group(3), status)
            status = sub(r'(Waiting for mount point in device class [\w\/,]+)( \()',
                        # Waiting for mount point in device class DC_TS3200_LTO4_05 (596 seconds).
                        lambda m: utilities.color(m.group(1), 'yellow') + m.group(2), status)
                        
            data2.append([index + 1, row[0], row[1], row[2], bytes_prcessed, status])

        globals.lastdsmcommandresults = data2
        return columnar(data2,
                        headers=['#', 'Proc#', 'Process', 'Files', 'Bytes', 'Status'],
                        justify=['r', 'l', 'l', 'r', 'r', 'l'])

define_command(SHowPRocesses())


class SPadminSHowLOCALLOG(SpadminCommand):

    def __init__(self):
        self.command_string = "SPadmin SHow LOCALLOG"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'shows local logfile'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []

        logfile = open(globals.logfilename, 'r')
        lines = logfile.readlines()
        logfile.close()

        min = -30
        match = search(r'(\d+)', parameters)
        if match:
            min = int(match[1]) * -1

        for line in lines[min:]:

            match = search(r'^(\d{8})\s(\d{6})\s(\w+)\s(.*)$', line.rstrip())
            if match:
                data.append([match[1], match[2], match[3], match[4]])
            else:
                data.append(['', '', '', line])

        return columnar(data,
                                   headers=['Date', 'Time', 'Level', 'Text'],
                                   justify=['l', 'l', 'l', 'l'])

define_command(SPadminSHowLOCALLOG())


class kill(SpadminCommand):

    def __init__(self):
        self.command_string = "Kill"
        self.command_type = "KILL"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Cancels sessions or processes'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        if globals.lastdsmcommandtype == "PROCESSES" or globals.lastdsmcommandtype == "SESSIONS":
            if parameters.strip().isnumeric():
                if len(globals.lastdsmcommandresults) >= int(parameters) > 0:
                    if globals.lastdsmcommandtype == "SESSIONS":
                        for line in (globals.tsm.send_command_array_tabdel(
                                "CANCEL SESSION " + globals.lastdsmcommandresults[ int(parameters) - 1 ][1])):
                            print(line)
                    else:
                        for line in (globals.tsm.send_command_array_tabdel(
                                "CANCEL PROCESS " + globals.lastdsmcommandresults[ int(parameters) - 1 ][1])):
                            print(line)
                else:
                    print(utilities.color("The given number is not found!", 'red'))
            else:
                print(utilities.color("The given parameter should be a number!", 'red'))
        else:
            print(utilities.color("Last command should be SHow SESSions or SHow PRocesses!", 'red'))
            globals.logger.debug("Last command type: " + globals.lastdsmcommandtype)
        return ""

define_command(kill())


class ShowEvents(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "EVents"
        self.command_type = "EVENT"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow EVents: display information about Events'

    def help(self) -> dict:
        return """Display the following information about events in the following order and format:
    ------------------- ------------------- ------------------- ------ ------------ ------------------- --------- --
            StartTime >     ActualStart     < Completed         Domain ScheduleName NodeName            Result    RC
    ------------------- ------------------- ------------------- ------ ------------ ------------------- --------- --
    09/27/2022 13:00:00                                14:00:00 FILES  INC_1300     SERVER_A            Missed
    09/27/2022 13:00:00            13:05:35            13:13:54 FILES  INC_1300     SERVER_B            Completed 0
    09/27/2022 13:00:00            13:02:46            13:09:20 FILES  INC_1300     SERVER_C            Completed 8
    09/27/2022 13:00:00                                14:00:00 FILES  INC_1300     SERVER_D            Missed"""

    def _execute(self, parameters: str) -> str:       
        data = timemachine_query( self.command_type, 'q event * * endd=today endt=now+1 f=d' + ' ' + parameters)
        
        if globals.last_error['rc'] != '0':
            return

        data2 = []
        for index, row in enumerate(data):

            if row[4][0:10] == row[3][0:10]:
                row[4] = '          ' + row[4][10:]
            if row[5][0:10] == row[3][0:10]:
                row[5] = '          ' + row[5][10:]

            if row[6] == 'Missed':
                row[6] = utilities.color(row[6], 'yellow' )
            elif row[6] == 'Failed' or row[6] == 'Failed - no restart':
                row[6] = utilities.color(row[6], 'red')
            elif row[6] == 'Pending':
                row[6] = utilities.color(row[6], 'yellow' )
            elif row[6] == 'Started':
                row[6] = utilities.color(row[6], 'yellow' )
            elif row[6] == 'Completed':
                row[6] = utilities.color(row[6], 'green' )

            if row[7] == '0':
                row[7] = utilities.color(row[7], 'green' )
            elif row[7] == '4' or row[7] == '8':
                row[7] = utilities.color(row[7], 'yellow')
            else:
                row[7] = utilities.color(row[7], 'red')

            data2.append([row[3], row[4], row[5], row[0], row[1], row[2], row[6], row[7]])

        table = (columnar(data2,
                          headers=['StartTime >', 'ActualStart', '< Completed', 'Domain', 'ScheduleName', 'NodeName',
                                   'Result', 'RC'],
                          justify=['r', 'c', 'l', 'c', 'l', 'l', 'l', 'r']))

        return table

define_command(ShowEvents())


class ShowADMINEVents( SpadminCommand ):
    def __init__(self):
        self.command_string = globals.basecommandname + "ADMINEVents"
        self.command_type = "EVENT"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow ADMINEVents: display information about Events'

    def help(self) -> dict:
        return """Display the following information about admin events in the following order and format:
    """

    def _execute(self, parameters: str) -> str:       
        data = timemachine_query( self.command_type, 'q event * endd=today endt=now+8 t=a f=d' + ' ' + parameters)
        
        if globals.last_error['rc'] != '0':
            return

        data2 = []
        for index, row in enumerate(data):

            if row[2][0:10] == row[1][0:10]:
                row[2] = '          ' + row[2][10:]
            if row[3][0:10] == row[1][0:10]:
                row[3] = '          ' + row[3][10:]

            if row[4] == 'Missed':
                row[4] = utilities.color(row[4], 'yellow' )
            elif row[4] == 'Failed' or row[4] == 'Failed - no restart':
                row[4] = utilities.color(row[4], 'red')
            elif row[4] == 'Pending':
                row[4] = utilities.color(row[4], 'yellow' )
            elif row[4] == 'Started':
                row[4] = utilities.color(row[4], 'yellow' )
            elif row[4] == 'Completed':
                row[4] = utilities.color(row[4], 'green' )

            if row[5] == '0':
                row[5] = utilities.color(row[5], 'green' )
            elif row[5] == '4' or row[5] == '8':
                row[5] = utilities.color(row[5], 'yellow')
            else:
                row[5] = utilities.color(row[5], 'red')

            data2.append( [ row[1], row[2], row[3], row[0], row[4], row[5] ] )

        table = ( columnar( data2,
                          headers=[ 'StartTime >', 'ActualStart', '< Completed', 'ScheduleName', 'Result', 'RC' ],
                          justify=[ 'r', 'c', 'l', 'l', 'l', 'r' ] ) )

        return table

define_command(ShowADMINEVents())


class ShowStgp(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "STGpools"
        self.command_type = "STGP"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow STGpools: display information about storage pools'

    def help(self) -> dict:
        return """Display the following information about storage pools in the following order and format:
 - Storage Pool name               
 - Device Class name              
 - Collocation   
 - Estimated Capacity 
 - Percent Utilized 
 - Percent Migrate 
 - High Migration threshold 
 - Low Migration threshold 
 - Reclamation
 - Next Storage Pool name"""

    def _execute(self, parameters: str) -> str:
        data = []
        data = timemachine_query( self.command_type, 
            "select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,CACHE,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS")
        
        for index, row in enumerate(data):
            (a, b, c, d, e, f, g, h, i, j, k) = row
            
            if d == '':
                data[index][3] = 0
            else:
                # data[index][3] = round((float(d)/1024),1)
                data[index][3] = humanbytes.HumanBytes.format(float( d ) * 1024 * 1024, unit="BINARY_LABELS", precision=0)

            row[6] = row[6][0:1]

            if row[1] == 'DISK':
                if float(row[5]) > 85:
                    row[5] = utilities.color( row[5], 'red' )
                elif float(row[5]) > 70:
                    row[5] = utilities.color( row[5], 'yellow' )

            if row[6] == 'Y':
                row[6] = utilities.color( row[6], 'green' )
                    
        return columnar( data,
                         headers=['PoolName', 'DeviceClass', 'Coll', 'EstCap', 'PctUtil', 'PctMigr', 'C', 'High', 'LowM', 'Recl', 'Next'],
                         justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'c', 'c', 'c', 'l'])
        
define_command(ShowStgp())


class ShowMount(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "MOUnt"
        self.command_type = "MOUNT"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow MOUnt: display volume mount'

    def help(self) -> dict:
        return """SHow MOUnt: display volume mount in the following format and order:
- ----------- ------ ----- ------------------------------ ------------------
# Volume Name Access Drive Path                           Status
- ----------- ------ ----- ------------------------------ ------------------
1 SBO566L6    R/W    DRV1  /dev/lin_tape/by-id/1068005803 DISMOUNTING
2 SBO376L6    R/W    DRV2  /dev/lin_tape/by-id/1068006258 IN USE
3 SBO566L6    R/W    DRV1  /dev/lin_tape/by-id/1068005803 IN USE
4 SBO376L6    R/W    DRV2  /dev/lin_tape/by-id/1068006258 IN USE
5 N/A         N/A    N/A   Device Class: DCLTO_02         WAITING FOR VOLUME
6 SBO376L6    R/W    DRV2  /dev/lin_tape/by-id/1068006258 IDLE"""

    def _execute(self, parameters: str) -> str:
        data = timemachine_query( self.command_type, "Query MOunt" )
        
        if len( data ) == 0:
            return
        
        """data = [[
                    "ANR8331I LTO volume SBO566L6 is mounted R/W in drive DRV1 (/dev/lin_tape/by-id/1068005803), status: DISMOUNTING."],
                [
                    "ANR8330I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IN USE."],
                [
                    "ANR8330I LTO volume SBO566L6 is mounted R/W in drive DRV1 (/dev/lin_tape/by-id/1068005803), status: IN USE."],
                [
                    "ANR8330I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IN USE."],
                [
                    "ANR8379I Mount point in device class DCLTO_02 is waiting for the volume mount to complete, status: WAITING FOR VOLUME."],
                [
                    "ANR8329I LTO volume SBO376L6 is mounted R/W in drive DRV2 (/dev/lin_tape/by-id/1068006258), status: IDLE."]
                ]"""

        data2 = []
        index = 1
        for l in data:
            if search("ANR83(29|30|31|32|33)I.*", l[0]):
                for vol, rw_ro, drive, path, status in re.findall(
                        re.compile(r'.* volume (.*) is mounted (.*) in drive (.*) \((.*)\), status: (.*)..*'), l[0]):
                    # vol = utilities.color( vol, 'green', attrs=[ globals.color_attrs_bold ] )
                    data2.append([index, vol, rw_ro, drive, path, status])
                    index += 1
            elif search("ANR8379I", l[0]):
                for devc, status in re.findall(re.compile(".* device class (.*) is waiting .*, status: (.*)..*"), l[0]):
                    data2.append([index, "N/A", "N/A", "N/A", "Device Class: " + devc, status])
                    index += 1

        globals.lastdsmcommandresults = data2
        index = 1

        ## for coloring purposes. (dismount)
        data3 = []
        for index, vol, rw_ro, drive, path, status in data2:
            vol = utilities.color(vol, 'green')
            data3.append([index, vol, rw_ro, drive, path, status])
            index += 1

        table = columnar(data3,
                         headers=['#', 'Volume', 'Access', 'Drive', 'Path', 'Status'],
                         justify=['r', 'l', 'c', 'l', 'l', 'l', ])

        return table

define_command(ShowMount())


class DISMount(SpadminCommand):
    def __init__(self):
        self.command_string = "UMount"
        self.command_type = globals.lastdsmcommandtype
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'DISMount: Dismount volume from drives (last command should be `SHow MOUnt` or `show DRive`)'

    def help(self) -> dict:
        return """Dismount volume from drives (last command should be`SHow MOUnt` or `SHow DRive`)"""

    def _execute(self, parameters: str) -> str:
        if globals.lastdsmcommandtype == "DRIVE" or globals.lastdsmcommandtype == "MOUNT":
            if parameters.strip().isnumeric():
                if len(globals.lastdsmcommandresults) >= int(parameters) > 0:
                    if globals.lastdsmcommandtype == "DRIVE":
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd = "DISMount Volume" + " " + line[7]
                    else:  # Mount
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd = "DISMount Volume" + " " + line[1]
                    for l in globals.tsm.send_command_array_tabdel(cmd):
                        print(l)
                else:
                    print(utilities.color("The given number is not found!", 'red'))
            else:
                print(utilities.color("The given parameter should be a number!", 'red'))
        else:
            print(utilities.color("Last command should be `SHow MOUnt` or `show DRive`!", 'red'))
            globals.logger.debug("Last command type: " + globals.lastdsmcommandtype)
        return ""

    def execute(self, dummy, parameters):
        globals.logger.debug(
            "Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            self._execute(parameters)
        globals.logger.debug(
            "Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")


define_command(DISMount())


class Ruler(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "RULer"
        self.command_type = "SPADMIN"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow RULer: This command will print a simple text ruler.'

    def help(self) -> dict:
        return """This command will print a simple text ruler.
    SHow RULer Help!    - print this help message
    SHow RULer          - print simple ruler
    SHow RULer INVerse  - print simple inverse ruler"""

    def _execute(self, parameters: str) -> str:
        if len(parameters) > 0:
            if search(utilities.regexpgenerator('INVerse'), parameters, IGNORECASE):
                self.ruler1()
                self.ruler10()
                self.ruler100()
            else:
                print(utilities.color('Wrong parameter(s)!', 'red'))
        else:
            self.ruler100()
            self.ruler10()
            self.ruler1()
        return ''

    def ruler100(self):
        cc = 1
        for i in range(1, globals.columns + 1, 1):
            if i % 100:
                sys.stdout.write(' ')
            else:
                sys.stdout.write(utilities.color(str(cc), 'green'))
                cc += 1
                cc = 0 if cc == 100 else cc
        print()

    def ruler10(self):
        cc = 1
        for i in range(1, globals.columns + 1, 1):
            if i % 10:
                sys.stdout.write(' ')
            else:
                sys.stdout.write(utilities.color(str(cc), 'green'))
                cc += 1
                cc = 0 if cc == 10 else cc
        print()

    def ruler1(self):
        for i in range(1, globals.columns + 1, 1):
            c = i % 10
            if c:
                sys.stdout.write(str(c))
            else:
                sys.stdout.write(utilities.color(str(c), 'green'))

    def execute(self, dummy, parameters):
        globals.logger.debug(
            "Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            self._execute(parameters)
        globals.lastdsmcommandtype = self.get_command_type()
        globals.logger.debug(
            "Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")

define_command(Ruler())


class Online(SpadminCommand):
    def __init__(self):
        self.command_string = "ONline"
        self.command_type = globals.lastdsmcommandtype
        self.command_index = 0
        self.command = "PAY"
        self.online = "ONLINE=YES"

    def short_help(self) -> str:
        return 'ONline or OFFline: switch drives/pathes into on-line/off-line state'

    def help(self) -> dict:
        return """ONline or Offline: switch drives/pathes into on-line/off-line state"""

    def _execute(self, parameters: str) -> str:
        if globals.lastdsmcommandtype == "DRIVE" or globals.lastdsmcommandtype == "PATH":
            if parameters.strip().isnumeric():
                if len(globals.lastdsmcommandresults) >= int(parameters) > 0:
                    if globals.lastdsmcommandtype == "DRIVE":
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd = "UPDATE DRIVE" + " " + line[1] + " " + line[2] + " " + self.online
                    else:
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd = "UPDATE PATH" + " " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " " + \
                              line[5] + " " + self.online
                    for l in globals.tsm.send_command_array_tabdel(cmd):
                        print(l)
                else:
                    print(utilities.color("The given number is not found!", 'red'))
            else:
                print(utilities.color("The given parameter should be a number!", 'red'))
        else:
            print(utilities.color("Last command should be SHow DRives or SHow PAth!", 'red'))
            globals.logger.debug("Last command type: " + globals.lastdsmcommandtype)
        return ""

    def execute(self, dummy, parameters):
        globals.logger.debug(
            "Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            self._execute(parameters)
        globals.logger.debug(
            "Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")

define_command(Online())


class Offline(Online):
    def __init__(self):
        self.command_string = "OFFline"
        self.command_type = globals.lastdsmcommandtype
        self.command_index = 0
        self.command = "PAY"
        self.online = "ONLINE=NO"

define_command(Offline())


class ShowDrives(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "DRives"
        self.command_type = "DRIVE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow DRives: display information about drives'

    def help(self) -> dict:
        return """"""

    def _execute(self, parameters: str) -> str:
        drives = timemachine_query( self.command_type,
            "select LIBRARY_NAME,DRIVE_NAME,'ONL='||ONLINE,ELEMENT,DRIVE_STATE,DRIVE_SERIAL,VOLUME_NAME,ALLOCATED_TO from drives order by 1,2")
            
        if globals.last_error[ 'rc' ] != '0':
            return

        data = []
        for i, row in enumerate(drives):
            # row[ 6 ] = utilities.color( row[ 6 ], 'green', attrs=[ globals.color_attrs_bold ] )
            data.append([i + 1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

        globals.lastdsmcommandresults = data

        ## for coloring purposes. (dismount)
        data2 = []
        for i, row in enumerate(drives):
            row[6] = utilities.color(row[6], 'green')
            data2.append([i + 1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

        table = columnar(data2,
                         headers=['#', 'Library', 'Drive', 'Online', 'Ele', 'State', 'Serial', 'Volume',
                                  'Allocated'],
                         justify=['r', 'l', 'l', 'l', 'c', 'l', 'l', 'l', 'l'])
        return table

define_command(ShowDrives())


class ShowPath(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "PAth"
        self.command_type = "PATH"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow PAth: display information about library and drive pathes'

    def help(self) -> dict:
        return """Display the following information about pathes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        library = globals.tsm.send_command_array_array_tabdel(
            "select SOURCE_NAME,DESTINATION_NAME,'SRCT='||SOURCE_TYPE,'DESTT='||DESTINATION_TYPE,LIBRARY_NAME,'DEVI='||DEVICE,'ONL='||ONLINE from paths where LIBRARY_NAME is null")
 
        if globals.last_error[ 'rc' ] != '0':
            return
            
        drive = globals.tsm.send_command_array_array_tabdel(
            "select SOURCE_NAME,DESTINATION_NAME,'SRCT='||SOURCE_TYPE,'DESTT='||DESTINATION_TYPE,'LIBR='||LIBRARY_NAME,'DEVI='||DEVICE,'ONL='||ONLINE from paths where LIBRARY_NAME is not null")

        if globals.last_error[ 'rc' ] != '0':
            return

        for i, row in enumerate(drive):
            library.append(row)
        data = []

        for i, row in enumerate(library):
            data.append([i + 1, row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

        table = columnar(data,
                         headers=['#', 'SourceName', 'DestiName', 'SourceType', 'DestinationType', 'LibraryName',
                                  'Device', 'Online'],
                         justify=['r', 'l', 'l', 'l', 'l', 'l', 'l', 'l'])
        globals.lastdsmcommandresults = data
        return table

define_command(ShowPath())


class ShowColumns(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "COLumns"
        self.command_type = "COLUMNS"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'SHow COLumns: display Spectrum Protect database columns'

    def help(self) -> dict:
        return """Display the Spectrum Protect internal DB2-SQL database columns by tables  
This information can be useful, when you are trying to deep dive into ISP internal world.
This table can be very long, so it recommended to use `|grep ` or `|more` or both. 
"""

    def _execute(self, parameters: str) -> str:
        data = globals.tsm.send_command_array_array_tabdel(
            "select tabname, colname from columns")

        table = columnar(data,
                         headers=['Table name', 'Column Name'],
                         justify=['l', 'l'])
        return table

define_command(ShowColumns())


class ShowLIBVolumes(SpadminCommand):
    def __init__(self):
        self.command_string = globals.basecommandname + "MIssinglibvolumes"
        self.command_type = "LIBVOLUMES"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Display information about library volumes'

    def help(self) -> dict:
        return """Display the following information about library volumes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        library = globals.tsm.send_command_array_array_tabdel(
            "select vol.volume_name, vol.stgpool_name, libv.library_name from volumes as vol left join libvolumes as libv on vol.volume_name=libv.volume_name where vol.devclass_name != 'DISK' AND vol.devclass_name not in (select devclass_name from devclasses where DEVTYPE = 'FILE' ) order by 1")
        
        if globals.last_error[ 'rc' ] != '0':
            return
    
        data = []
        data2 = []

        for i, row in enumerate(library):
            data.append([i + 1, row[0], row[1], row[2]])
            if not row[2]:
                row[2] = utilities.color("MISSING", 'yellow')
            data2.append([i + 1, utilities.color(row[0], 'green'), row[1], row[2]])
        globals.lastdsmcommandresults = data

        table = columnar(data2,
                         headers=['#', 'VolName', 'PoolName', 'LibName'],
                         justify=['r', 'l', 'l', 'l'])

        return table

define_command(ShowLIBVolumes())


class ShowFilling( SpadminCommand ):
    def __init__(self):
        self.command_string = globals.basecommandname + "FILLings"
        self.command_type   = "VOLUMES"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'SHow Filling: display information about fillings volumes'

    def help(self) -> dict:
        return """Display the following information about library volumes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        stgpools = globals.tsm.send_command_array_array_tabdel( "select stgpool_name, count(*) from volumes where stgpool_name like upper('%" + parameters + "%') and status='FILLING' and ACCESS='READWRITE' and devclass_name in (select devclass_name from devclasses where WORM='NO' and DEVCLASS_NAME !='DISK') group by STGPOOL_NAME having count(*)>1 order by 2 desc" )
        
        # select VOLUME_NAME, PCT_UTILIZED from volumes where STGPOOL_NAME='$line[0]' and STATUS='FILLING' and ACCESS='READWRITE' order by PCT_UTILIZED
        
        if globals.last_error[ 'rc' ] != '0':
            return
        
        data  = []
        data2 = []

        c = 1
        for i, row in enumerate( stgpools ):
            
            data.append( [ '', row[0] + ' [' + row[1] + ']'  ] )

            for i, vol in enumerate( globals.tsm.send_command_array_array_tabdel( "select VOLUME_NAME, PCT_UTILIZED from volumes where STGPOOL_NAME='" + row[0] + "' and STATUS='FILLING' and ACCESS='READWRITE' order by PCT_UTILIZED" ) ):
            
                data.append([ c, ' ' + vol[0] + ' [' + vol[1] + '%]' ] )
                data2.append( [ vol[0] ] )
                c += 1
            
        globals.lastdsmcommandresults = data2

        table = columnar( data,
                          headers=[ '#', 'FillingVolume' ],
                          justify=[ 'r', 'l' ] )

        return table

define_command(ShowFilling())


class Move(SpadminCommand):
    def __init__(self):
        self.command_string = "MOve"
        self.command_type = "MOVE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Move data '

    def help(self) -> dict:
        return """Move data """

    def _execute(self, parameters: str) -> str:
        if parameters.strip().isnumeric():
            if globals.lastdsmcommandtype == "VOLUMES":
            
                if len(globals.lastdsmcommandresults) >= int(parameters):
                    line = globals.lastdsmcommandresults[ int(parameters) - 1 ]
                    cmd = "MOVE DATA" + " " + line[0]
                    
                    for l in globals.tsm.send_command_normal(cmd).splitlines()[1:]:
                        print(l)
                        
                else:
                    print(utilities.color("The given number is not found!", 'red'))
            else:
                print(utilities.color("Last command should be SHow Filling!", 'red'))
                globals.logger.debug("Last command type: " + globals.lastdsmcommandtype)
        else:
            # print(utilities.color("The given parameter should be a number!", 'red'))
            #
            for l in globals.tsm.send_command_normal('MOve ' + parameters).splitlines()[1:]:
                print(l)
        return ""

    def execute(self, dummy, parameters):
        globals.logger.debug(
            "Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            self._execute(parameters)
        globals.logger.debug(
            "Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")

define_command(Move())

class Console(SpadminCommand):
    def __init__(self):
        self.command_string = "CONSole"
        self.command_type = "CONSOLE"
        self.command_index = 0
        self.command = "FREE"

    def short_help(self) -> str:
        return 'Opens a new Terminal window and starts spadmin in console mode'

    def help(self) -> dict:
        return """Open an spadmin console view like the dsmadmc -cons command does.  """

    def _execute(self, parameters: str) -> str:
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system( '/mnt/c/Windows/notepad.exe ' + globals.logfilename )
        elif sys.platform == "darwin":
           os.system('open -a Terminal ./spadmin.py --args --consoleonly')
        return ""


define_command(Console())

class SHowSCRatches(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "SCRatches"
        self.command_type = "SCRATCHES"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show Scratch volumes'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = timemachine_query( self.command_type, "select LIBRARY_NAME, MEDIATYPE, count(*) from libvolumes where upper(status)='SCRATCH' group by LIBRARY_NAME,MEDIATYPE" )
            
        if globals.last_error[ 'rc' ] != '0':
            return
      
        globals.lastdsmcommandresults = []            
        
        data2 = []
        for index, row in enumerate(data):

            if int(row[2]) < 5:
                scratches = utilities.color(row[2], 'yellow')
            elif int(row[2]) < 3:
                scratches = utilities.color(row[2], 'red')
            else:
                scratches = row[2]

            data2.append([row[0], row[1], scratches])
        globals.lastdsmcommandresults = data2
        return columnar(data2,
                        headers=['LibraryName', 'Type', '#Scratch'],
                        justify=['l', 'l', 'r'])

define_command(SHowSCRatches())


class SHowCOPYGroups(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "COPYGroups"
        self.command_type = "COPYGROUP"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows copygroup information in one table'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = globals.tsm.send_command_array_array_tabdel(
            "select bu.DOMAIN_NAME, bu.SET_NAME, bu.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where bu.DOMAIN_NAME = DOMAIN_NAME and bu.SET_NAME = SET_NAME and bu.CLASS_NAME = CLASS_NAME ), bu.VEREXISTS, bu.VERDELETED, bu.RETEXTRA, bu.RETONLY, bu.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where bu.DESTINATION = stgp.STGPOOL_NAME) from BU_COPYGROUPS bu")

        # data = globals.tsm.send_command_array_array_tabdel( "select bu.DOMAIN_NAME, bu.SET_NAME, bu.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where bu.DOMAIN_NAME = DOMAIN_NAME and bu.SET_NAME = SET_NAME and bu.CLASS_NAME = CLASS_NAME ), bu.VEREXISTS, bu.VERDELETED, bu.RETEXTRA, bu.RETONLY, bu.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where bu.DESTINATION = stgp.STGPOOL_NAME), ar.RETVER, ar.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where ar.DESTINATION = stgp.STGPOOL_NAME) from BU_COPYGROUPS bu, AR_COPYGROUPS ar" )

        if globals.last_error[ 'rc' ] != '0':
            return

        globals.lastdsmcommandresults = []
        
        unique = {}
        bu     = {}

        for index, row in enumerate(data):

            if row[3] == 'Yes':
                default = utilities.color('y', 'green')
            else:
                default = ''

            bunextdest = ''
            if row[9] != '':
                bunextdest += '-> ' + row[9]

            bu[row[0] + row[1] + row[2] + default] = [
                row[4].rstrip() + ', ' + row[5].rstrip() + ', ' + row[6].rstrip() + ', ' + row[7].rstrip(), row[8],
                bunextdest]

            unique[row[0] + row[1] + row[2] + default] = [row[0], row[1], row[2], default]

        data = globals.tsm.send_command_array_array_tabdel(
            "select ar.DOMAIN_NAME, ar.SET_NAME, ar.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where ar.DOMAIN_NAME = DOMAIN_NAME and ar.SET_NAME = SET_NAME and ar.CLASS_NAME = CLASS_NAME ), ar.RETVER, ar.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where ar.DESTINATION = stgp.STGPOOL_NAME) from AR_COPYGROUPS ar")

        if globals.last_error[ 'rc' ] != '0':
            return

        ar = {}

        for index, row in enumerate(data):

            if row[3] == 'Yes':
                default = utilities.color('y', 'green')
            else:
                default = ''

            arnextdest = ''
            if row[6] != '':
                arnextdest += '-> ' + row[6]

            ar[row[0] + row[1] + row[2] + default] = [row[4].rstrip(), row[5], arnextdest]

            unique[row[0] + row[1] + row[2] + default] = [row[0], row[1], row[2], default]

        data2 = []
        for key in unique:

            if key in bu and key in ar:
                data2.append(unique[key] + bu[key] + ar[key])
            elif key in bu:
                data2.append(unique[key] + bu[key] + ['', '', ''])
            elif key in ar:
                data2.append(unique[key] + ['', '', ''] + ar[key])

        return columnar(data2,
                        headers=['Domain', 'PolicySet', 'MgmtClass', 'd', 'BACopy(ve,vd,re,ro)', 'BADest',
                                 'Next', 'ARCopy(d)', 'ARDest', 'Next'],
                        justify=['l', 'l', 'l', 'l', 'c', 'l', 'l', 'c', 'l', 'l'])

        # utilities.printer( columnar( data2,
        #     headers = [ 'Domain', 'PolicySet', 'MgmtClass', 'd', 'ARCopy (d)', 'ARDest', 'Next' ],
        #     justify = [ 'l', 'l', 'l', 'l', 'l', 'l', 'l' ] ) )

define_command(SHowCOPYGroups())


class ShowCLIENTBACKUPPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "CLIENTBACKUPPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show client backup performanc data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:

        return basicPerformanceFromSummary( self, "BACKUP", parameters )
        
define_command(ShowCLIENTBACKUPPERFormance())


class ShowCLIENTRESTOREPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "CLIENTRESTOREPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show client restore performance data'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "RESTORE", parameters )

define_command(ShowCLIENTRESTOREPERFormance())


class ShowCLIENTARCHIVEPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "CLIENTARCHIVEPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show client archive performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "ARCHIVE", parameters )

define_command(ShowCLIENTARCHIVEPERFormance())


class ShowCLIENTRETRIEVEPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "CLIENTRETRIEVEPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show client retrieve performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "RETRIEVE", parameters )

define_command(ShowCLIENTRETRIEVEPERFormance())


class ShowDBBACKUPPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "DBBACKUPPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows db backup performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "FULL_DBBACKUP", parameters )

define_command(ShowDBBACKUPPERFormance())


class ShowMIGRATIONPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "MIGRATIONPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Shows migrations performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "MIGRATION", parameters )

define_command(ShowMIGRATIONPERFormance())


class ShowMOVEDATAPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "MOVEDATAPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show move data performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "MOVE DATA", parameters )

define_command(ShowMOVEDATAPERFormance())


class ShowRECLAMATIONPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "RECLAMATIONPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show reclamation performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "RECLAMATION", parameters )

define_command(ShowRECLAMATIONPERFormance())


class ShowSTGPOOLBACKUPPERFormance(SpadminCommand):

    def __init__(self):
        self.command_string = globals.basecommandname + "STGPOOLBACKUPPERFormance"
        self.command_type = "PERFROMANCE"
        self.command_index = 0
        self.command = "PAY"

    def short_help(self) -> str:
        return 'Show storage poll backup performance data'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        return basicPerformanceFromSummary( self, "STGPOOL BACKUP", parameters )

define_command(ShowSTGPOOLBACKUPPERFormance())


def basicPerformanceFromSummary( self, activity, parameters ):
    # ARCHIVE           Ok
    # BACKUP            Ok
    # EXPIRATION
    # FULL_DBBACKUP     Ok
    # INCR_DBBACKUP
    # MIGRATION         Ok
    # MOVE DATA         Ok
    # RECLAMATION       Ok
    # RESTORE           Ok
    # RETRIEVE          OK
    # STGPOOL BACKUP    Ok
    # TAPE MOUNT

    fromdate = 0
    todate   = 1


    match = search(r'(\d+)\s+(\d+)', parameters)
    if match:
        fromdate = int(match[1])
        todate = int(match[2])
    else:
        match = search(r'(\d+)', parameters)
        if match:
            todate = int(match[1])

    # swap variables
    if fromdate > todate:
        fromdate, todate = todate, fromdate

    data = globals.tsm.send_command_array_array_tabdel(
        "select date(START_TIME),time(START_TIME),date(END_TIME),time(END_TIME),NUMBER,ENTITY,SCHEDULE_NAME,EXAMINED,AFFECTED,FAILED,BYTES,IDLE,MEDIAW,PROCESSES,SUCCESSFUL,timestampdiff(2,char((END_TIME-START_TIME))) from summary where ACTIVITY='" + activity + "' and (start_time >= current_timestamp - " + str( todate ) + " day) and (end_time <= current_timestamp - " + str( fromdate ) + " day) order by 1")

    if globals.last_error['rc'] != '0':
        return

    data2 = []
    for index, row in enumerate(data):

        if int(row[15]) > 0:
            speed = str(int(int(row[10]) / 1024 / 1024 / int(row[15])))
        else:
            speed = "n/a";

        if int(row[9]) > 0:
            failed = utilities.color(row[9], 'red')
        else:
            failed = row[9]

        if int(row[11]) > 10*60:
            row[11] = utilities.color( humanbytes.HumanBytes.format( int( row[11] ), unit="TIME_LABELS", precision=0 ), 'red')
        elif int(row[11]) > 2*60:
            row[11] = utilities.color( humanbytes.HumanBytes.format( int( row[11] ), unit="TIME_LABELS", precision=0), 'yellow' )
        else:
            row[11] = humanbytes.HumanBytes.format( int( row[11] ), unit="TIME_LABELS", precision=0 )

        if int(row[12]) > 10*60:
            row[12] = utilities.color( humanbytes.HumanBytes.format( int( row[12] ), unit="TIME_LABELS", precision=0 ), 'red' )
        elif int(row[12]) > 2*60:
            row[12] = utilities.color( humanbytes.HumanBytes.format( int( row[12] ), unit="TIME_LABELS", precision=0 ), 'yellow' )
        else:
            row[12] = humanbytes.HumanBytes.format( int( row[12] ), unit="TIME_LABELS", precision=0)

        if row[14] == 'NO':
            success = utilities.color( row[14], 'red' )
        else:
            success = utilities.color( row[14], 'green' )

        columntmp = 'Pool'
        if activity == "BACKUP" or activity == "RESTORE" or activity == "ARCHIVE" or activity == "RETRIEVE":
            columntmp = "Node"

        data2.append(
            [row[0] + ' ' + row[1], row[2] + ' ' + row[3], row[4], row[5], row[6], row[7] + '/' + row[8] + '/' + failed,
             humanbytes.HumanBytes.format( int( row[10] ), unit="BINARY_LABELS", precision=0 ),
             humanbytes.HumanBytes.format( int( row[15] ), unit="TIME_LABELS", precision=0 ), speed + ' MB/s', row[11], row[12], row[13], success])

    return columnar(data2,
                    headers=['StartTime >', '< EndTime', '#Proc', columntmp, 'SchedName', '#E/A/F', '#Bytes', 'Time', 'Speed', 'Idle', 'MedW', 'P', 'Suc'],
                    justify=['r', 'l', 'c', 'c', 'l', 'c', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])


class ShowSTatus( SpadminCommand ):
                    
    def __init__(self):
        self.command_string = globals.basecommandname + "STatus"
        self.command_type   = "STATUS"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show general SP status'

    def help(self) -> dict:
        return """ 
        """
    def _execute(self, parameters: str) -> str:
        
        # From: https://github.com/FleXoft/tsmadm.pl/blob/master/tsmadm.pl/plugins/v2_plugin.pl
        
        if int( globals.spversion ) <= 5:
            print( 'This command not supported on SP version less than v6!' )
            return
        
        data = []
        
        # DB part
        data.append( [ 'DB' ] )
        DBerrorcollector = 0
        
        dbFreeSpace, dbCacheHitPct, dbPkgHitPct, dbLastReorgHour, dbLastBackupHour = globals.tsm.send_command_array_array_tabdel( "select FREE_SPACE_MB, BUFF_HIT_RATIO, PKG_HIT_RATIO, TIMESTAMPDIFF( 8, char(timestamp( current_timestamp ) - TIMESTAMP( LAST_REORG ) ) ), TIMESTAMPDIFF( 8, char(timestamp( current_timestamp ) - TIMESTAMP( LAST_BACKUP_DATE ) ) ) from db" )[0]          
        
        status = '  Ok.'
        if float( dbFreeSpace ) < 10000:
            status = utilities.color( '  Failed!', 'red' )
            DBerrorcollector =+ 1
        data.append( [ ' FreeSpace', humanbytes.HumanBytes.format( float( dbFreeSpace ) * 1024 * 1024, unit="BINARY_LABELS", precision=0), status ] )
        
        status = '  Ok.'
        if float( dbCacheHitPct ) < 90:
            status = utilities.color( '  Failed!', 'red' )
            DBerrorcollector =+ 1
        data.append( [ ' Cache Hit', dbCacheHitPct + ' %', status ] )    

        status = '  Ok.'
        if float( dbPkgHitPct ) < 90:
            status = utilities.color( '  Failed!', 'red' )
            DBerrorcollector =+ 1
        data.append( [ ' Pkg Hit', dbPkgHitPct + ' %', status ] )    

        status = '  Ok.'
        if dbLastBackupHour == '':
            dbLastBackupHour = 0
        if int( dbLastBackupHour ) > 19:
            status = utilities.color( '  Failed!', 'red' )
            DBerrorcollector =+ 1
        data.append( [ ' Last DBBackup', humanbytes.HumanBytes.format( int( dbLastBackupHour ) * 3600, unit="TIME_LABELS", precision=0 ), status ] )    
        
        status = '  Ok.'
        if float( dbLastReorgHour ) > 24:
            status = utilities.color( '  Failed!', 'red' )
            DBerrorcollector =+ 1
        data.append( [ ' Last DB reorganization', humanbytes.HumanBytes.format( float( dbLastReorgHour ) * 3600, unit="TIME_LABELS", precision=0 ), status ] )
        
        tmpdata = globals.tsm.send_command_array_array_tabdel( "select VOLUME_NAME, BACKUP_SERIES, DATE_TIME from volhistory where type='BACKUPFULL' order by BACKUP_SERIES desc" )
        
        if globals.last_error[ 'rc' ] != '0':
            DBLastFull, dbLastSeq, dbLastFullBackupHour = '', '', '0'
        else:
            DBLastFull, dbLastSeq, dbLastFullBackupHour = tmpdata[0]
        
        data.append( [ ' Last Full Volume', '[' + utilities.color( DBLastFull, 'green' ) + ']' ] )
        data.append( [ ' Last Full', dbLastFullBackupHour[:19] ] )
        
        status = '  Ok.'
        if int( DBerrorcollector ) > 0:
            status = utilities.color( '  Failed!', 'red' )                        
        data.append( [ 'DB overall STATUS', '->', status ] )
                        
        data.append( [] )
        
        # LOG part
        data.append( [ 'LOG' ] )
        LOGerrorcollector = 0
        
        logFreeSpace, logArchFreeSpace, logActLogDir, logArchLogDir, logMirrorDir, logArchFailLog = globals.tsm.send_command_array_array_tabdel( "select FREE_SPACE_MB, ARCHLOG_FREE_FS_MB, ACTIVE_LOG_DIR, ARCH_LOG_DIR, MIRROR_LOG_DIR, AFAILOVER_LOG_DIR from log" )[0]
        
        status = '  Ok.'
        if float( logFreeSpace ) < 10000:
            status = utilities.color( '  Failed!', 'red' )
            LOGerrorcollector =+ 1
        data.append( [ ' Active log FreeSpace', humanbytes.HumanBytes.format( float( logFreeSpace ) * 1024 * 1024,      unit="BINARY_LABELS", precision=0), status ] )
        
        status = '  Ok.'
        if float( logArchFreeSpace ) < 10000:
            status = utilities.color( '  Failed!', 'red' )
            LOGerrorcollector =+ 1
        data.append( [ ' Archive log FreeSpace', humanbytes.HumanBytes.format( float( logArchFreeSpace ) * 1024 * 1024, unit="BINARY_LABELS", precision=0), status ] )
        
        data.append( [ ' Active log dir', logActLogDir ] )    
        data.append( [ ' Archive log dir', logArchLogDir ] )
        data.append( [ ' Active failover log dir', logArchFailLog ] )    
        data.append( [ ' Active mirror log dir', logMirrorDir ] )    
        
        status = '  Ok.'
        if int( LOGerrorcollector ) > 0:
            status = utilities.color( '  Failed!', 'red' )                        
        data.append( [ 'LOG overall STATUS', '->', status ] )
        
        data.append( [] )
        
        # VOL part
        data.append( [ 'VOLs' ] )
        VOLerrorcollector = 0

        sumVols   = globals.tsm.send_command_array_array_tabdel( "select count(*) from volumes" )[0][0]
        roVols    = globals.tsm.send_command_array_array_tabdel( "select count(*) from volumes where access like '%READO%'" )[0][0]
        unavaVols = globals.tsm.send_command_array_array_tabdel( "select count(*) from volumes where access like '%UNAVA%'" )[0][0]
        rweVols   = globals.tsm.send_command_array_array_tabdel( "select count(*) from volumes where WRITE_ERRORS>0 or READ_ERRORS>0" )[0][0]

        data.append( [ ' ReadOnly Vol(s)',    sumVols + ' / ' + roVols ] )
        data.append( [ ' Unavailable Vol(s)', sumVols + ' / ' + unavaVols ] ) 
        data.append( [ ' Suspicious Vol(s)',  sumVols + ' / ' + rweVols ] )

        status = '  Ok.'
        if int( roVols ) + int( unavaVols ) + int( rweVols ) > 0:
            status = utilities.color( '  Failed!', 'red' )
            VOLerrorcollector += 1                        
        data.append( [ 'VOLs overall STATUS', '->', status ] )

        data.append( [] )
        
        # HW part
        data.append( [ 'HW' ] )
        HWerrorcollector = 0

        sumDrives = globals.tsm.send_command_array_array_tabdel( "select count(*) from drives" )[0][0]
        offDrives = globals.tsm.send_command_array_array_tabdel( "select count(*) from drives where online='NO'" )[0][0]
        sumPaths  = globals.tsm.send_command_array_array_tabdel( "select count(*) from paths" )[0][0]
        offPaths  = globals.tsm.send_command_array_array_tabdel( "select count(*) from paths where online='NO'" )[0][0]

        data.append( [ ' Offline drive(s)', sumDrives + ' / ' + offDrives ] )
        data.append( [ ' Offline path(s)',  sumPaths  + ' / ' + offPaths ] )

        status = '  Ok.'
        if int( offDrives ) + int( offPaths ) > 0:
            status = utilities.color( '  Failed!', 'red' )
            HWerrorcollector += 1                        
        data.append( [ 'HW overall STATUS', '->', status ] )

        data.append( [] )
       
        # Client events part
        data.append( [ '<24H client events summary' ] )
        EVENTerrorcollector = 0

        for completed in globals.tsm.send_command_array_array_tabdel( "select result, count(1) from events where status='Completed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is not null and NODE_NAME is not null group by result" ):
            data.append( [ ' Completed (' + completed[0] + ')', completed[1] ] )
            if completed[0] != '0':
                EVENTerrorcollector =+ 1
                
        missed = globals.tsm.send_command_array_array_tabdel( "select count(1) from events where status='Missed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is not null and NODE_NAME is not null" )[0][0]
        data.append( [ ' Missed', missed ] )
        
        failed = globals.tsm.send_command_array_array_tabdel( "select count(1) from events where status='Failed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is not null and NODE_NAME is not null" )[0][0]
        data.append( [ ' Failed', failed ] )

        status = '  Ok.'
        if int( EVENTerrorcollector ) + int( missed ) + int( failed ) > 0 :
            status = utilities.color( '  Failed!', 'red' )
            EVENTerrorcollector += 1                        
        data.append( [ 'EVENTs overall STATUS', '->', status ] )

        data.append( [] )
        
        # VM part
        data.append( [ '<24H VM backups summary' ] )
        VMerrorcollector = 0
        
        failed = globals.tsm.send_command_array_array_tabdel( "select count(1) from SUMMARY_EXTENDED where ACTIVITY_DETAILS='VMware' and SUB_ENTITY != 'Aggregate' and (start_time >= current_timestamp - 1 day) and SUCCESSFUL != 'YES' order by 1" )[0][0]
        data.append( [ ' Failed', failed ] )
        
        status = '  Ok.'
        if int( VMerrorcollector ) + int( failed ) > 0 :
            status = utilities.color( '  Failed!', 'red' )
            VMerrorcollector += 1                        
        data.append( [ 'VM overall STATUS', '->', status ] )

        data.append( [] )
        
        # REPL part
        data.append( [ '<24H replication summary' ] )
        LOGerrorcollector = 0
                
        data.append( [] )
        
        # ADMIN part
        data.append( [ '<24H admin events summary' ] )
        ADMINerrorcollector = 0

        for completed in globals.tsm.send_command_array_array_tabdel( "select result, count(1) from events where status='Completed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is null and NODE_NAME is null group by result" ):
            data.append( [ ' Completed (' + completed[0] + ')', completed[1] ] )
            if completed[0] != '0':
                EVENTerrorcollector =+ 1
                
        missed = globals.tsm.send_command_array_array_tabdel( "select count(1) from events where status='Missed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is null and NODE_NAME is null" )[0][0]
        data.append( [ ' Missed', missed ] )
        
        failed = globals.tsm.send_command_array_array_tabdel( "select count(1) from events where status='Failed' and SCHEDULED_START>'2012-01-01 00:00:00' and (SCHEDULED_START>=current_timestamp-24 hour) and DOMAIN_NAME is null and NODE_NAME is null" )[0][0]
        data.append( [ ' Failed', failed ] )
        
        status = '  Ok.'
        if int( ADMINerrorcollector ) + int( missed ) + int( failed ) > 0 :
            status = utilities.color( '  Failed!', 'red' )
            EVENTerrorcollector += 1                        
        data.append( [ 'ADMIN EVENTs overall STATUS', '->', status ] )
    
        data.append( [] )
        
        # ACTLOG part
        data.append( [ '<24H activity log summary' ] )
        ACTLOGerrorcollector = 0
        
        for severity in globals.tsm.send_command_array_array_tabdel( "select severity, count(1) from actlog where (DATE_TIME>=current_timestamp-24 hour) and severity in ('E','W') and MSGNO not in (2000, 2034, 0944) group by severity" ):
            data.append( [ ' Completed (' + severity[0] + ')', severity[1] ] )
            ACTLOGerrorcollector =+ 1

        status = '  Ok.'
        if int( ACTLOGerrorcollector ) + int( failed ) > 0 :
            status = utilities.color( '  Failed!', 'red' )                        
        data.append( [ 'ACTLOG overall STATUS', '->', status ] )
                
        data.append( [] )
        
        # GLOBAL SUM part
        data.append( [ 'Global SP status summary' ] )
        
        status = '  Ok.'
        if int( DBerrorcollector ) + int( LOGerrorcollector ) + + int( VOLerrorcollector ) + + int( HWerrorcollector ) + int( EVENTerrorcollector ) + int( VMerrorcollector ) + int( ACTLOGerrorcollector )  > 0 :
            status = utilities.color( '  Failed!', 'red' )                        
        data.append( [ 'Global SP STATUS', '->', status ] )

        return columnar( data,
                         headers = [ 'Item', 'Value', 'Result' ],
                         justify = [ 'l', 'r', 'c' ] )

define_command( ShowSTatus() )


class SHowDBBackups( SpadminCommand ):

    def __init__(self):
        self.command_string = globals.basecommandname + "DBBackups"
        self.command_type   = "DBBACKUP"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show SP DB full backups'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        
        data = timemachine_query( self.command_type, "select date(DATE_TIME),time(DATE_TIME),TYPE,BACKUP_SERIES,BACKUP_OPERATION,VOLUME_SEQ,DEVCLASS,VOLUME_NAME from volhistory where type='BACKUPFULL' or type='BACKUPINCR' order by date_time desc, BACKUP_SERIES" )
            
        if globals.last_error[ 'rc' ] != '0':
            return
        
        data2 = []      
        for row in data:
            row[7] = utilities.color( row[7], 'green' )
            data2.append(row)
        
        return columnar( data2,
                         headers = [ 'Date', 'Time', 'Type', 'Serie', '#', 'Seq', 'DeviceClass', 'Volume' ],
                         justify = [ 'l', 'l', 'l', 'c', 'l', 'l', 'c', 'l' ])

define_command( SHowDBBackups() )


class SHowDBSBackups( SpadminCommand ):

    def __init__(self):
        self.command_string = globals.basecommandname + "DBSBackups"
        self.command_type   = "DBSBACKUP"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show SP DB full snapshot backups'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        
        data = timemachine_query( self.command_type, "select date(DATE_TIME),time(DATE_TIME),TYPE,BACKUP_SERIES,BACKUP_OPERATION,VOLUME_SEQ,DEVCLASS,VOLUME_NAME from volhistory where type='DBSNAPSHOT' order by date_time desc, BACKUP_SERIES" )
            
        if globals.last_error[ 'rc' ] != '0':
            return
        
        data2 = []      
        for row in data:
            row[7] = utilities.color( row[7], 'green' )
            data2.append(row)
        
        return columnar( data2,
                         headers = [ 'Date', 'Time', 'Type', 'Serie', '#', 'Seq', 'DeviceClass', 'Volume' ],
                         justify = [ 'l', 'l', 'l', 'c', 'l', 'l', 'c', 'l' ] )

define_command( SHowDBSBackups() )


class SHowINActives( SpadminCommand ):

    def __init__(self):
        self.command_string = globals.basecommandname + "INActives"
        self.command_type   = "INACTIVE"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show inactive nodes'

    def help(self) -> dict:
        return """ 
        """

    def _execute(self, parameters: str) -> str:
        data = []
        
        data = timemachine_query( self.command_type, "select n.domain_name,n.node_name,locked,date(n.lastacc_time),TIMESTAMPDIFF(16,CHAR(current_timestamp-n.lastacc_time)),o.type,sum(logical_mb),sum(o.num_files) from nodes as n, occupancy as o where n.node_name=o.node_name and TIMESTAMPDIFF(16,CHAR(current_timestamp-n.lastacc_time))>=15 group by n.domain_name,n.node_name,n.locked,n.lastacc_time,o.type order by 7 desc" )
            
        if globals.last_error[ 'rc' ] != '0':
            return
               
        return columnar( data,
                         headers = [ 'DomainName', 'NodeName', 'Locked?', 'LastAccessTime', 'Days', 'Type', '#Data', 'Files' ],
                         justify = [ 'l', 'l', 'c', 'c', 'r', 'l', 'r', 'r' ] )

define_command( SHowINActives() )


class SHowREPLICATIONDifferences( SpadminCommand ):

    def __init__(self):
        self.command_string = globals.basecommandname + "REPLICATIONDifferences"
        self.command_type   = "REPLDIFF"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show replication differences nodes'

    def help(self) -> dict:
        return """SHow REPLICATIONDifferences command will show the replication differences in the following format:
        
---

* It expects one single parameter, which is a node name. 

* If nothing is specified, it will show the replication differences of all SP nodes."""

    def _execute(self, parameters: str) -> str:
        
        if not parameters:
            parameters = '*'
            
        data = []
        
        data = timemachine_query( self.command_type, "q replnode " + parameters )
            
        if globals.last_error[ 'rc' ] != '0' or data[0] == ['ANR2726E QUERY REPLNODE: None of the specified nodes are configured for replication or they are part of an active replication process.']:
            print( 'No data!' )
            return
               
        data2 = []
        for row in data:
            
            # > 8.1.13 
            if int( globals.spversion ) > 8 or ( int( globals.spversion ) == 8 and int( globals.sprelease ) >= 1 and int( globals.splevel ) >= 13 ) :
                if row[6] == '':
                    continue
                if row[4] == '':
                    row[4] = '0'              
                if row[5] == '':
                    row[5] = '0'
                delta =  int( row[5].replace( ',', '' ) ) - int( row[4].replace( ',', '' ) )
                hh = [ 'NodeName', 'Type', 'FilespaceName', 'FSID', 'FilesonS', 'FilesonR', 'ReplServer', 'delta' ]
                if row[6] == '0':
                    continue
            else:
                if row[5] == '':
                    continue
                if row[4] == '':
                    row[4] = '0'
                if row[6] == '':
                    row[6] = '0'
                delta =  int( row[6].replace( ',', '' ) ) - int( row[4].replace( ',', '' ) )
                hh = [ 'NodeName', 'Type', 'FilespaceName', 'FSID', 'FilesonS', 'ReplServer', 'FilesonR', 'delta' ]
            
            if delta > 0:
                delta = utilities.color( str ( delta ), 'yellow' )
            elif delta == 0:
                delta = utilities.color( str ( delta ), 'green' )
            else:
                delta = utilities.color( str ( delta ), 'red' )
                  
            data2.append( row + [ delta ] )  
               
        return columnar( data2,
                         headers = hh,
                         justify = [ 'l', 'l', 'l', 'r', 'c', 'c', 'c', 'c' ] )

define_command( SHowREPLICATIONDifferences() )


class SHowNODEOccuopancy( SpadminCommand ):

    def __init__(self):
        self.command_string = globals.basecommandname + "NODEOccuopancy"
        self.command_type   = "NODEOCCU"
        self.command_index  = 0
        self.command        = "PAY"

    def short_help(self) -> str:
        return 'Show node occuopancy'

    def help(self) -> dict:
        return """ 
        Please, be aware to run audit license before show nodeoccupancy
        https://www.ibm.com/docs/en/storage-protect/8.1.20?topic=commands-query-auditoccupancy-query-client-node-storage-utilization
        """

    def _execute(self, parameters: str) -> str:
        data = []
        
        data = timemachine_query( self.command_type, "select a.NODE_NAME, n.domain_name, BACKUP_MB, ARCHIVE_MB, SPACEMG_MB, TOTAL_MB from auditocc a, nodes n where n.node_name = a.node_name order by 6" )
            
        if globals.last_error[ 'rc' ] != '0':
            return
        
        data2 = []
        for row in data:

            row[2] = humanbytes.HumanBytes.format( float( row[2] ) * 1024 * 1024, unit="BINARY_LABELS", precision=0 )
            row[3] = humanbytes.HumanBytes.format( float( row[3] ) * 1024 * 1024, unit="BINARY_LABELS", precision=0 )
            row[4] = humanbytes.HumanBytes.format( float( row[4] ) * 1024 * 1024, unit="BINARY_LABELS", precision=0 )
            row[5] = humanbytes.HumanBytes.format( float( row[5] ) * 1024 * 1024, unit="BINARY_LABELS", precision=0 )
          
            data2.append( row )
                              
        return columnar( data2,
                         headers = [ 'NodeName', 'DoaminName', 'BData', 'AData', 'SPData', 'SumData' ],
                         justify = [ 'l', 'c', 'r', 'r', 'r', 'r' ] )

define_command( SHowNODEOccuopancy() )


# merge these commands to the global rules
utilities.dictmerger( globals.myIBMSPrlCompleter.rules, globals.myIBMSPrlCompleter.dynrules )