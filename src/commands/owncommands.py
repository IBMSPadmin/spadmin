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

from time import time

columnar = columnar.Columnar() # columnar: table creator/formatter utility
spadmin_commands      = {}  # dictionary for the spadmin commands
disabled_words        = ['DEFAULT', 'ALIAS', 'SPADMIN']  # disabled words: used in the configuration .ini file
globals.lastdsmcommandtype    = '?'  # last command type: used by "kill", "on", "off", etc. commands
globals.lastdsmcommandresults = ['']  # last command result: used by "kill", "on", "off", etc. commands


class SpadminCommand:
    """
    This is the interface class for every Spadmin Command
    """
    def __init__(self):
        self.command_string = ""
        self.command_type = ""
        self.command_index = 0

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
        globals.logger.debug("Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            utilities.printer(self._execute(parameters))
        globals.lastdsmcommandtype = self.get_command_type()
        globals.logger.debug("Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")


def dynruleinjector( command ): # it works only for commands which longer than 2 words!! on 1 word command needs to be added to the rules file.
            commandpartcollected = ''
            for commandpart in command.split()[ :-1 ]:
                commandpartcollected += commandpart
                if commandpartcollected not in globals.myIBMSPrlCompleter.dynrules:
                    globals.myIBMSPrlCompleter.dynrules[ commandpartcollected ] = []
                commandpartcollected += ' '
            
            commandpartcollected = command.split()        
            for commandpart in command.split()[ :-1 ]:                      
                    rightpart = commandpartcollected.pop( -1 )
                    leftpart  = ' '.join( commandpartcollected )
                    if rightpart not in globals.myIBMSPrlCompleter.dynrules[ leftpart ]:
                        globals.myIBMSPrlCompleter.dynrules[ leftpart ].append( rightpart )


def spadmin_show_cache( self, parameters ):
    data  = []
    for key in globals.myIBMSPrlCompleter.cache_hitratio:
        data.append( [ key, globals.myIBMSPrlCompleter.cache_hitratio[ key ] ] )
    utilities.printer( columnar( data, headers=[ colored( 'Name', 'white', attrs=[ 'bold' ] ), colored( 'Value', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'c' ] ) )

    data.clear()
    for key in globals.myIBMSPrlCompleter.cache:
        
        timediff = int( globals.config.getconfiguration()['SPADMIN']['cache_age'] ) - int( time() - globals.myIBMSPrlCompleter.cache_timestamp[ key ] )
        if timediff > 0:
           timediff = colored( humanbytes.HumanBytes.format( int( timediff ), unit="TIME_LABELS", precision = 0 ), 'green', attrs=[ 'bold' ] )  
        else:
            timediff = colored( humanbytes.HumanBytes.format( int( timediff ), unit="TIME_LABELS", precision = 0 ), 'red', attrs=[ 'bold' ] )
        
        data.append( [ key.strip(), timediff, globals.myIBMSPrlCompleter.cache[ key ] ] )
    utilities.printer( columnar( data, headers=[ colored( 'Query', 'white', attrs=[ 'bold' ] ), colored( 'Time', 'white', attrs=[ 'bold' ] ), colored( 'Result', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'c', 'l' ] ) )

#
spadmin_commands[ 'SPadmin SHow CAche' ] = spadmin_show_cache
dynruleinjector(  'SPadmin SHow CAche' )


def history(self, parameters):
    data = []
    rlhistfile = os.path.join("./", globals.config.getconfiguration()['SPADMIN']['historyfile'])
    globals.logger.debug('history file open: [' + rlhistfile + ']')
    if os.path.exists(rlhistfile):
        globals.logger.debug('history file open: [' + rlhistfile + ']')
        f = open(rlhistfile, "r")
        count = 0
        for line in f.readlines():
            count += 1
            data.append([count, line.strip()])
    utilities.printer( columnar( data, headers=[ colored( '#', 'white', attrs=[ 'bold' ] ), colored( 'Command', 'white', attrs=[ 'bold' ] ) ], justify=[ 'r', 'l'] ) )
#
spadmin_commands[ 'HISTory' ] = history
dynruleinjector(  'HISTory' )


def spadmin_show_config( self, parameters ):
    data  = []

    for configclass in globals.config.getconfiguration():
        for variable in globals.config.getconfiguration()[ configclass ]:
            data.append( [ configclass, variable, '=', globals.config.getconfiguration()[ configclass ][ variable ] ] )
    utilities.printer( columnar( data, headers=[ colored( 'Class', 'white', attrs=[ 'bold' ] ), colored( 'Variable', 'white', attrs=[ 'bold' ] ), colored( '=', 'white', attrs=[ 'bold' ] ) ,colored( 'Value', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'l', 'l', 'l' ] ) )
#
spadmin_commands[ 'SPadmin SHow CONFig' ] = spadmin_show_config
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'CONFig' )
dynruleinjector( 'SPadmin SHow CONFig' )


def spadmin_show_aliases( self, parameters ):
    data  = []
    for key in globals.aliases:
        data.append( [ key, globals.aliases[ key ] ] )
    utilities.printer( columnar( data, headers=[ colored( 'Alias', 'white', attrs=[ 'bold' ] ), colored( 'Command', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'l' ] ) )
#
spadmin_commands[ 'SPadmin SHow ALIases' ] = spadmin_show_aliases
#globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ] = []
#globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'SHow' )
#globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'ALIases' )
dynruleinjector( 'SPadmin SHow ALIases' )


def spadmin_show_version( self, parameters ):
    print( 'spadmin version: v1.0' )
#    
spadmin_commands[ 'SPadmin SHow VERsion' ] = spadmin_show_version
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'VERsion' )
dynruleinjector( 'SPadmin SHow VERsion' )

def spadmin_set_debug( self, parameters ):
    print( 'Debug is set to ON. The pervious debug level was: [' + logging.getLevelName( globals.logger.getEffectiveLevel() ) + '].' )
    globals.logger.setLevel( logging.DEBUG )
#
spadmin_commands[ 'SPadmin SET DEBUG' ] = spadmin_set_debug
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'SET' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SET' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SET' ].append( 'DEBUG' )
dynruleinjector( 'SPadmin SET DEBUG' )


def spadmin_unset_debug( self, parameters ):
    print( 'Debug is set to OFF. The pervious debug level was: [' + logging.getLevelName( globals.logger.getEffectiveLevel() ) + '].' )
    globals.logger.setLevel( logging.INFO )
#
spadmin_commands[ 'SPadmin UNSET DEBUG' ] = spadmin_unset_debug
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'UNSET' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin UNSET' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin UNSET' ].append( 'DEBUG' )
dynruleinjector( 'SPadmin UNSET DEBUG' )


def spadmin_show_rules( self, parameters ):
    
    min = 0
    max = 99
    
    match = search ( '(\d+)\s+(\d+)', parameters )
    if match:
        min = int( match[ 1 ] )
        max = int( match[ 2 ] )
    else:
        match = search ( '(\d+)', parameters )
        if match:
            min = int( match[ 1 ] )
    
    data  = []
    for key in globals.myIBMSPrlCompleter.rules:
        if globals.myIBMSPrlCompleter.rules[key]:
            rulelength = len( key.split() )
            if rulelength >= min and rulelength <= max:
                data.append( [ key, rulelength, globals.myIBMSPrlCompleter.rules[ key ] ] )

    utilities.printer( columnar( sorted( data, key = lambda x: x[ 1 ] ), 
        headers = [ 'Regexp', 'LVL', 'Value' ],
        justify = [ 'l', 'c', 'l' ] ) )
#
spadmin_commands[ 'SPadmin SHow RULes' ] = spadmin_show_rules
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'RULes' )
dynruleinjector( 'SPadmin SHow RULes' )


def spadmin_show_commands( self, parameters ):
    data  = []
    for key in spadmin_commands:
        desc = ""
        if key in command_help:
            desc = command_help[key][0]
        data.append( [ key, desc ] )

    utilities.printer( columnar( sorted( data ), headers=[ 
        colored( 'Command name', 'white', attrs=['bold'] ), colored( 'Short Description', 'white', attrs=['bold'] ) ],
        justify = [ 'l','l' ]) )
#
spadmin_commands[ 'SPadmin SHow COMmands' ] = spadmin_show_commands
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'RULes' )
dynruleinjector( 'SPadmin SHow COMmands' )


def show_actlog ( self, parameters ):
    data = None
    if parameters is None or parameters == '' or parameters == []:
        data = globals.tsm.send_command_array_array_tabdel("q actlog")
    else:
        data = globals.tsm.send_command_array_array_tabdel(str(''.join(["q actlog ", " ".join([parameters])])))

    if len(data) == 0:
        return
        
    data2 = []
    for index, row in enumerate( data ):
                          
        if search( '^ANR\d{4}E', row[ 1 ] ):
            message = colored ( row[ 1 ], 'red', attrs = [ 'bold' ])
        elif search( '^ANR\d{4}W', row[ 1 ] ):
            message = colored ( row[ 1 ], 'yellow', attrs = [ 'bold' ])
        else:
            message = row[ 1 ]

        data2.append( [ row[ 0 ], message ] )

    utilities.printer( columnar( data2,
        headers=[ 'Date/Time', 'Message' ],
        justify=[ 'l', 'l' ] ) )
#
spadmin_commands[ 'SHow ACTlog' ] = show_actlog
# globals.myIBMSPrlCompleter.dynrules['SHow'].append('ACTlog')
dynruleinjector( 'SHow ACTlog' )


def reload( self, parameters ):
    globals.myIBMSPrlCompleter.loadrules( globals.rulefilename )
#
spadmin_commands[ 'REload' ] = reload


def spadmin_show_log( self, parameters ):
    
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system( '/mnt/c/Windows/notepad.exe ./' + globals.config.getconfiguration()['SPADMIN']['logfile'] )
    elif sys.platform == "darwin":
        os.system( 'open ./' + globals.config.getconfiguration()['SPADMIN']['logfile'] )
    
#
spadmin_commands[ 'SPadmin SHow LOG' ] = spadmin_show_log
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'Log' )
dynruleinjector( 'SPadmin SHow LOG' )


def spadmin_add_alias( self, parameters ):
    if len(str(parameters).split(':')) != 2:
        print('Please use the following command format: \'SPadmin Add ALIas cmd:command\'')
        return
    else:
        key, value = str(parameters).split(':')
        key = key.strip()
        value = value.strip()
        globals.aliases[key] = value
        globals.config.getconfiguration()['ALIAS'][key] = value
        globals.config.writeconfig()
        dynruleinjector('SPadmin Add ALIas ' + key)
        globals.myIBMSPrlCompleter.dynrules['SPadmin Add ALIas'].append(key)
#
spadmin_commands[ 'SPadmin Add ALIas' ] = spadmin_add_alias
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin Add' ].append( 'ALIas' )
dynruleinjector( 'SPadmin Add ALIas' )

def spadmin_show_processinfo( self, parameters ):
    data = [["Normal", globals.tsm.get_tsm_normal().pid], ["Tabdelimited", globals.tsm.get_tsm_tabdel().pid]]
    table = columnar(data,
                     headers=['dsmadmc','PID'], justify=[ 'l', 'cl'])
    utilities.printer(table)
spadmin_commands[ 'SPadmin SHow PRocessinfo' ] = spadmin_show_processinfo
dynruleinjector(  'SPadmin SHow PRocessinfo' )

def spadmin_del_alias( self, parameters ):
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
            print (f'The given alias \'{parameters}\' not found')
#
spadmin_commands[ 'SPadmin DELete ALIas' ] = spadmin_del_alias
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin DELete' ].append( 'ALIas' )
dynruleinjector( 'SPadmin DELete ALIas' )
for key in globals.config.getconfiguration()['ALIAS']:
    dynruleinjector('SPadmin DELete ALIas '+ key)


def spadmin_add_server( self, parameters ):
    if len(str(parameters).split(' ')) != 3:
        print('Please use the following command format: \'SPadmin Add SErver server_name user_id password\'')
        return
    else:
        server, userid, password = str(parameters).split(' ')
        server = str(server).upper()
        if globals.config.getconfiguration().has_section(server) or server in disabled_words:
            print (f'The given server name \'{server}\' already exists or not allowed')#
        else:
            if utilities.check_connection(server, userid, password):
                globals.config.getconfiguration().add_section(server)
                globals.config.getconfiguration()[server]['dsmadmc_id'] = userid
                globals.config.getconfiguration()[server]['dsmadmc_password'] = password
                globals.config.writeconfig()
                dynruleinjector('SPadmin DELete SErver ' + server)
                globals.myIBMSPrlCompleter.dynrules['SPadmin DELete SErver'].append(server)
            else:
                print ('Server parameters not saved!')

spadmin_commands[ 'SPadmin Add SErver' ] = spadmin_add_server
dynruleinjector( 'SPadmin Add SErver' )


def spadmin_del_server( self, parameters ):
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
            print (f'The given server \'{server}\' not found')

#
spadmin_commands[ 'SPadmin DELete SErver' ] = spadmin_del_server
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin DELete' ].append( 'SErver' )
dynruleinjector( 'SPadmin DELete SErver' )
for section in globals.config.getconfiguration().sections():
    if section not in disabled_words:
        dynruleinjector('SPadmin DELete SErver ' + section)


def show_server( self, parameters ):
    for section in globals.config.getconfiguration().sections():
        if section not in disabled_words:
            print(section)
#
spadmin_commands[ 'SPadmin SHow SErver' ] = show_server
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'SErver' )
dynruleinjector( 'SPadmin SHow SErver' )

def switch_server( self, parameters ):
    print("SWITCH SERVER")
    if not parameters:
        print('Please use the following command format: \'SPadmin SWitch SErver servername\'')
        return
    else:
        server = str(parameters).upper()
        if globals.config.getconfiguration().has_section(server) and parameters not in disabled_words:
            globals.tsm.quit()
            from dsmadmc_pexpect import dsmadmc_pexpect
            globals.tsm = dsmadmc_pexpect(server, globals.config.getconfiguration()[server]['dsmadmc_id'],
                                          globals.config.getconfiguration()[server]['dsmadmc_password'])

        else:
            print (f'The given server \'{server}\' not found')


#
spadmin_commands[ 'SPadmin SWitch SErver' ] = switch_server
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SWitch' ].append( 'SErver' )
dynruleinjector( 'SPadmin SWitch SErver' )

command_type_and_index = {}
command_help = {}

def help(command_name):
    print(command_help[command_name])


def define_own_command( command_string, function_address, command_type, index, short_help, help):
    spadmin_commands[command_string] = function_address
    dynruleinjector(command_string)
    command_type_and_index[command_string] = [command_type, index]
    command_help[command_string] = [short_help, help]


def define_command(clazz: SpadminCommand):
    define_own_command(clazz.get_command_string(), clazz.execute, clazz.get_command_type(), clazz.get_command_index(), clazz.short_help(), clazz.help())


def show_last_error ( self, parameters):
    print ("Last error message: ", globals.last_error["message"])
    print ("Last return code: ", globals.last_error["rc"])
#
spadmin_commands['SHow LASTerror'] = show_last_error
# globals.myIBMSPrlCompleter.dynrules['SHow'].append('LASTerror')
dynruleinjector( 'SHow LASTerror' )


def spadmin_show_extras( self, parameters ):
    print( 'CLI extra pipe parameter tester' )
    pprint( globals.extras )
#
spadmin_commands[ 'SPadmin SHow EXtras' ] = spadmin_show_extras
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'EXtras' )
dynruleinjector( 'SPadmin SHow EXtras' )

def echo( self, parameters ):
    print( parameters )
#
spadmin_commands[ 'PRint' ] = echo


def show_sessions( self, parameters ):

    data = globals.tsm.send_command_array_array_tabdel( 'select SESSION_ID, STATE, WAIT_SECONDS, BYTES_SENT, BYTES_RECEIVED, SESSION_TYPE, CLIENT_PLATFORM, CLIENT_NAME,MOUNT_POINT_WAIT, INPUT_MOUNT_WAIT, INPUT_VOL_WAIT, INPUT_VOL_ACCESS, OUTPUT_MOUNT_WAIT, OUTPUT_VOL_WAIT, OUTPUT_VOL_ACCESS, LAST_VERB, VERB_STATE from sessions order by 1' )

    if globals.last_error[ 'rc' ] != '0':
        print ( colored( globals.last_error["message"], 'red', attrs=[ 'bold' ] ) )
        return

    data2 = []
    for index, row in enumerate( data ):

        if row[ 1 ] == 'Run':
            state = colored( row[ 1 ], 'green', attrs = [ 'bold' ] )
        else:
            state = row[ 1 ]

        if int( row[ 2 ] ) > 60:
            wait = colored( humanbytes.HumanBytes.format( int( row[ 2 ] ), unit="TIME_LABELS", precision = 0 ), 'red', attrs = [ 'bold' ] )
        else:
            wait = humanbytes.HumanBytes.format( int( row[ 2 ] ), unit="TIME_LABELS", precision = 0 )

        bytes_sent     = humanbytes.HumanBytes.format( int( row[ 3 ] ), unit="BINARY_LABELS", precision = 0 )
        bytes_received = humanbytes.HumanBytes.format( int( row[ 4 ] ), unit="BINARY_LABELS", precision = 0 )

        # mediaaccess = ''.join( row[ 8:14 ] )
        match = search( '(\w+),(.+),(\d+)', row[ 11 ] )
        if match:
            row[ 11 ] = 'Read: ' + colored( match[ 2 ], 'green', attrs=[ 'bold' ] ) + ', ' + match[ 1 ] + ', ' + humanbytes.HumanBytes.format( int( match[ 3 ] ), unit="TIME_LABELS", precision = 0 )
        
        match = search( '(\w+),(.+),(\d+)', row[ 14 ] )
        if match:
            row[ 14 ] = 'Write: ' + colored( match[ 2 ], 'green', attrs=[ 'bold' ] ) + ', ' + match[ 1 ] + ', ' + humanbytes.HumanBytes.format( int( match[ 3 ] ), unit="TIME_LABELS", precision = 0 )
        
        mediaaccess = row[ 8 ] + row[ 9 ] + row[ 10 ] + row[ 11 ] + row[ 12 ] + row[ 13 ] + row[ 14 ]

        data2.append( [ index + 1,  row[ 0 ], state, wait, bytes_sent, bytes_received, row[ 5 ], row[ 6 ], row[ 7 ], mediaaccess, row[ 16 ] + row[ 15 ] ] )

    utilities.printer( columnar( data2, headers = [
        '#', 'Id', 'State', 'Wait', 'Sent', 'Received', 'Type', 'Platform', 'Name', 'MediaAccess', 'Verb' ],
        justify=[ 'r', 'c', 'c', 'r', 'r', 'r', 'r', 'c', 'l', 'l', 'l' ] ) )

    globals.lastdsmcommandtype    = 'SESSIONS'
    globals.lastdsmcommandresults = data2

spadmin_commands[ 'SHow SESsions' ] = show_sessions
dynruleinjector(  'SHow SESsions' )


def show_processes( self, parameters ):

    data = globals.tsm.send_command_array_array_tabdel( 'select PROCESS_NUM, PROCESS, FILES_PROCESSED, BYTES_PROCESSED, STATUS from processes order by 1' )

    if globals.last_error[ 'rc' ] != '0':
        globals.lastdsmcommandtype = 'PROCESSES'
        globals.lastdsmcommandresults = []
        return

    data2 = []
    for index, row in enumerate( data ):

        bytes_prcessed = humanbytes.HumanBytes.format( int( row[ 3 ] ), unit="BINARY_LABELS", precision = 0 )

        # Current input volume: MKP056M8. Current output volume(s): MKP074M8.
        status = row[ 4 ]
        status = sub( '(Current input volume: )([\w\/]+)(\.)',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Current input volumes: )([\w\/,]+)(\()',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Current input volumes: )([\w\/,]+)(\([\w ]+\))([\w\/,]+)(\()',
            # Current input volumes: MKP002M8,(33772 Seconds)MKP049M8,(15618 Seconds)
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ) + colored( m.group( 4 ), 'green', attrs=[ 'bold' ] ) + m.group( 5 ) , status )
        status = sub( '(Current output volume\(' + 's\): )([\w\/]+)(\.)',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Current output volumes: )([\w\/,]+)(\()',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Waiting for mount of input volume )([\w\/]+)( \()',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Waiting for mount of output volume )([\w\/,]+)( \()',
            # Waiting for mount of input volume 000006L4 (3 seconds)
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )
        status = sub( '(Volume )([\w\/]+)( \()',
            lambda m: m.group( 1 ) + colored( m.group( 2 ), 'green', attrs=[ 'bold' ] ) + m.group( 3 ), status )

        data2.append( [ index + 1,  row[ 0 ], row[ 1 ], row[ 2 ], bytes_prcessed, status ] )

    utilities.printer( columnar( data2,
        headers = [ '#', 'Proc#', 'Process', 'Files', 'Bytes', 'Status' ],
        justify = [ 'r', 'l', 'l', 'r', 'r', 'l' ] ) )

    globals.lastdsmcommandtype    = 'PROCESSES'
    globals.lastdsmcommandresults = data2

spadmin_commands[ 'SHow PRocesses' ] = show_processes
dynruleinjector(  'SHow PRocesses' )


def spadmin_locallog( self, parameters ):

    data = []

    logfile = open( globals.logfilename, 'r' )
    lines   = logfile.readlines()
    logfile.close()

    min = -30
    match = search ( '(\d+)', parameters )
    if match:
        min = int( match[ 1 ] ) * -1    

    for line in lines[ min: ]:

        match = search( '^(\d{8})\s(\d{6})\s(\w+)\s(.*)$', line.rstrip() )
        if match:
            data.append( [ match[ 1 ],  match[ 2 ], match[ 3 ], match[ 4 ] ] )
        else:
            data.append( [ '',  '', '', line ] )

    utilities.printer( columnar( data,
        headers = [ 'Date', 'Time', 'Level', 'Text' ],
        justify = [ 'l', 'l', 'l', 'l' ] ) )

spadmin_commands[ 'SPadmin SHow LOCALLOG' ] = spadmin_locallog
dynruleinjector(  'SPadmin SHow LOCALLOG' )

def kill( self, parameters ):

    if globals.lastdsmcommandtype == "PROCESSES" or globals.lastdsmcommandtype == "SESSIONS":
        if parameters.strip().isnumeric():
            if len(globals.lastdsmcommandresults) >= int(parameters) > 0:
                for line in (globals.tsm.send_command_array_tabdel("CANCEL SESSION " + globals.lastdsmcommandresults[int(parameters)-1][1])):
                    print(line)
            else:
                print(colored("The given number is not found!", 'red', attrs=['bold']))
        else:
            print(colored("The given parameter should be a number!", 'red', attrs=['bold']))
    else:
        print(colored("Last command should be SHow SESSions or SHow PRocesses!", 'red', attrs=[ 'bold' ] ))
        globals.logger.debug("Last command type: " + globals.lastdsmcommandtype)


spadmin_commands[ 'KILL' ] = kill


class ShowEvents(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow EVents"
        self.command_type   = "EVENT"
        self.command_index  = 0

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
        data = globals.tsm.send_command_array_array_tabdel('q event * * endd=today f=d' + ' ' + parameters)

        if globals.last_error['rc'] != '0':
            print(colored(globals.last_error["message"], 'red', attrs=['bold']))
            return

        data2 = []
        for index, row in enumerate(data):

            if row[4][0:10] == row[3][0:10]:
                row[4] = '          ' + row[4][10:]
            if row[5][0:10] == row[3][0:10]:
                row[5] = '          ' + row[5][10:]

            if row[6] == 'Missed':
                row[6] = colored(row[6], 'yellow', attrs=['bold'])
            if row[6] == 'Failed':
                row[6] = colored(row[6], 'red', attrs=['bold'])
                row[7] = colored(row[7], 'red', attrs=['bold'])
            if row[6] == 'Pending':
                row[6] = colored(row[6], 'cyan')
            if row[6] == 'Started':
                row[6] = colored(row[6], 'green', attrs=['bold'])
            if row[6] == 'Completed' and row[7] != '0':
                row[7] = colored(row[7], 'red', attrs=['bold'])

            data2.append([row[3], row[4], row[5], row[0], row[1], row[2], row[6], row[7]])

            table = (columnar(data2,
                headers=[ 'StartTime >', 'ActualStart', '< Completed', 'Domain', 'ScheduleName', 'NodeName', 'Result', 'RC'],
                justify=[ 'r', 'c', 'l', 'l', 'l', 'l', 'l', 'r' ] ) )
       
        return table

define_command(ShowEvents())


class ShowStgp(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow STGpools"
        self.command_type   = "STGP"
        self.command_index  = 0

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
        data = globals.tsm.send_command_array_array_tabdel(
            "select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS")
        for index, row in enumerate(data):
            (a, b, c, d, e, f, g, h, i, j) = row
            if d == '':
                data[index][3] = 0
            else:
                # data[index][3] = round((float(d)/1024),1)
                data[index][3] = humanbytes.HumanBytes.format(float(d) * 1024 * 1024, unit="BINARY_LABELS", precision=0)
                
            if row[ 1 ] == 'DISK':
                if float( row[ 5 ] ) > 85:
                    row[ 5 ] = colored( row[ 5 ], 'red', attrs=[ 'bold' ] ) 
                elif float( row[ 5 ] ) > 70: 
                    row[ 5 ] = colored( row[ 5 ], 'yellow', attrs=[ 'bold' ] ) 

        table = columnar(data, 
            headers=['PoolName', 'DeviceClass', 'Coll', 'EstCap', 'PctUtil', 'PctMigr', 'HighMig', 'LowMig', 'Recl', 'Next'],
            justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
        return table

define_command(ShowStgp())

class ShowMount(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow MOUnt"
        self.command_type   = "MOUNT"
        self.command_index  = 0

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
        data = globals.tsm.send_command_array_array_tabdel(
            "Query MOunt")
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
                    # vol = colored( vol, 'green', attrs=[ 'bold' ] )
                    data2.append([index, vol, rw_ro, drive, path, status])
                    index += 1
            elif search("ANR8379I", l[0]):
                for devc, status in re.findall(re.compile(".* device class (.*) is waiting .*, status: (.*)..*"), l[0]):
                    data2.append([index, "N/A", "N/A",  "N/A", "Device Class: " + devc, status])
                    index += 1

        globals.lastdsmcommandresults = data2
        index = 1

        ## for coloring purposes. (dismount)
        data3 = []
        for index, vol, rw_ro, drive, path, status in data2:
            vol = colored( vol, 'green', attrs=[ 'bold' ] )
            data3.append([index, vol, rw_ro, drive, path, status])
            index += 1

        table = columnar(data3,
            headers=['#', 'Volume', 'Access', 'Drive', 'Path', 'Status'],
            justify=['r', 'l', 'l', 'l', 'l', 'l',])

        return table

define_command(ShowMount())

class DISMount(SpadminCommand):
    def __init__(self):
        self.command_string = "DISMount"
        self.command_type   = globals.lastdsmcommandtype
        self.command_index  = 0

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
                    else: # Mount
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd  = "DISMount Volume" + " " + line[1]
                    for l in globals.tsm.send_command_array_tabdel(cmd):
                        print(l)
                else:
                    print(colored("The given number is not found!", 'red', attrs=['bold']))
            else:
                print(colored("The given parameter should be a number!", 'red', attrs=['bold']))
        else:
            print(colored("Last command should be `SHow MOUnt` or `show DRive`!", 'red', attrs=['bold']))
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
        self.command_string = "SHow RULer"
        self.command_type   = "RULER"
        self.command_index  = 0

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
                print(colored('Wrong parameter(s)!', 'red', attrs=['bold']))
        else:
            self.ruler100()
            self.ruler10()
            self.ruler1()
        return ''

    def ruler100(self):
        cc = 1
        for i in range( 1, globals.columns + 1, 1 ):
            if i % 100:
                sys.stdout.write( ' ' )
            else:
                sys.stdout.write( colored( str( cc ), 'green' ) )
                cc += 1
                cc = 0 if cc == 100 else cc
        print()

    def ruler10(self):
        cc = 1
        for i in range( 1, globals.columns + 1, 1 ):
            if i % 10:
                sys.stdout.write( ' ' )
            else:
                sys.stdout.write( colored( str( cc ), 'green' ) )
                cc += 1
                cc = 0 if cc == 10 else cc
        print()

    def ruler1(self):
        for i in range( 1, globals.columns + 1, 1 ):
            c = i % 10
            if c:
                sys.stdout.write( str( c ) )
            else:
                sys.stdout.write( colored( str( c ), 'green' ) )

    def execute(self, dummy, parameters):
        globals.logger.debug("Execution STARTED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        if parameters == "help":
            print(self.help())
        else:
            self._execute(parameters)
        globals.lastdsmcommandtype = self.get_command_type()
        globals.logger.debug("Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + globals.lastdsmcommandtype + ".")

define_command(Ruler())

class Online(SpadminCommand):
    def __init__(self):
        self.command_string = "ONline"
        self.command_type   = globals.lastdsmcommandtype
        self.command_index  = 0
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
                        cmd  = "UPDATE PATH" + " " + line[1] + " " + line[2] + " " + line[3] + " " + line[4] + " " + line[5] + " " + self.online
                    for l in globals.tsm.send_command_array_tabdel(cmd):
                        print(l)
                else:
                    print(colored("The given number is not found!", 'red', attrs=['bold']))
            else:
                print(colored("The given parameter should be a number!", 'red', attrs=['bold']))
        else:
            print(colored("Last command should be SHow DRives or SHow PAth!", 'red', attrs=['bold']))
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
        self.command_type   = globals.lastdsmcommandtype
        self.command_index  = 0
        self.online = "ONLINE=NO"

define_command(Offline())


class ShowDrives(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow DRives"
        self.command_type   = "DRIVE"
        self.command_index  = 0

    def short_help(self) -> str:
        return 'SHow DRives: display information about drives'

    def help(self) -> dict:
        return """"""

    def _execute(self, parameters: str) -> str:
        drives = globals.tsm.send_command_array_array_tabdel(
            "select LIBRARY_NAME,DRIVE_NAME,'ONL='||ONLINE,ELEMENT,DRIVE_STATE,DRIVE_SERIAL,VOLUME_NAME,ALLOCATED_TO from drives order by 1,2")

        data = []
        for i, row in enumerate(drives):
            # row[ 6 ] = colored( row[ 6 ], 'green', attrs=[ 'bold' ] )
            data.append([i+1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
            
        globals.lastdsmcommandresults = data
            
        ## for coloring purposes. (dismount)
        data2 = []
        for i, row in enumerate(drives):
            row[ 6 ] = colored( row[ 6 ], 'green', attrs=[ 'bold' ] )
            data2.append([i+1, row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]])

        table = columnar(data2,
            headers=['#', 'Library', 'Drive', 'Online', 'Element', 'State', 'Serial', 'Volume', 'Allocated'],
            justify=['r', 'l', 'l', 'l', 'c', 'l', 'l', 'l', 'l'])
        return table

define_command(ShowDrives())


class ShowPath(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow PAth"
        self.command_type   = "PATH"
        self.command_index  = 0

    def short_help(self) -> str:
        return 'SHow PAth: display information about library and drive pathes'

    def help(self) -> dict:
        return """Display the following information about pathes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        library = globals.tsm.send_command_array_array_tabdel(
            "select SOURCE_NAME,DESTINATION_NAME,'SRCT='||SOURCE_TYPE,'DESTT='||DESTINATION_TYPE,LIBRARY_NAME,'DEVI='||DEVICE,'ONL='||ONLINE from paths where LIBRARY_NAME is null")
        drive = globals.tsm.send_command_array_array_tabdel(
            "select SOURCE_NAME,DESTINATION_NAME,'SRCT='||SOURCE_TYPE,'DESTT='||DESTINATION_TYPE,'LIBR='||LIBRARY_NAME,'DEVI='||DEVICE,'ONL='||ONLINE from paths where LIBRARY_NAME is not null")

        for i, row in enumerate(drive):
            library.append(row)
        data = []

        for i, row in enumerate(library):
            data.append([i+1, row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

        table = columnar(data,
            headers=['#', 'SourceName', 'DestiName', 'SourceType', 'DestinationType', 'LibraryName', 'Device', 'Online'],
            justify=['r', 'l', 'l', 'l', 'l', 'l', 'l', 'l'])
        globals.lastdsmcommandresults = data
        return table

define_command(ShowPath())

class ShowColumns(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow COLumns"
        self.command_type   = "columns"
        self.command_index  = 0

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
        self.command_string = "SHow LIBVolumes"
        self.command_type   = "LIBVOLUMES"
        self.command_index  = 0

    def short_help(self) -> str:
        return 'SHow Filling: display information about library volumes'

    def help(self) -> dict:
        return """Display the following information about library volumes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        library = globals.tsm.send_command_array_array_tabdel(
            "select vol.volume_name, vol.stgpool_name, libv.library_name from volumes as vol left join libvolumes as libv on vol.volume_name=libv.volume_name where vol.devclass_name != 'DISK' AND vol.devclass_name not in (select devclass_name from devclasses where DEVTYPE = 'FILE' ) order by 1")
        data  = []
        data2 = []

        for i, row in enumerate(library):
            data.append([i+1, row[0], row[1], row[2]])
            if not row[2]:
                row[2]= colored("MISSING", 'yellow', attrs=['bold'])
            data2.append([i+1, colored(row[0], 'green', attrs=['bold']), row[1], row[2]])
        globals.lastdsmcommandresults = data
        
        table = columnar(data2,
            headers=['#', 'VolName', 'PoolName', 'LibName'],
            justify=['r', 'l', 'l', 'l'])
        
        return table

define_command(ShowLIBVolumes())

class ShowFilling(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow FILLings"
        self.command_type   = "VOLUMES"
        self.command_index  = 0

    def short_help(self) -> str:
        return 'SHow Filling: display information about fillings volumes'

    def help(self) -> dict:
        return """Display the following information about library volumes in the following order and format:
"""

    def _execute(self, parameters: str) -> str:
        library = globals.tsm.send_command_array_array_tabdel(
            "select VOLUME_NAME, STGPOOL_NAME, PCT_UTILIZED from volumes where STATUS='FILLING' and ACCESS='READWRITE' order by PCT_UTILIZED")
        data  = []
        data2 = []
        
        for i, row in enumerate(library):
            data.append([i+1, row[0], row[1], row[2]])
            data2.append([i+1, colored(row[0], 'green', attrs=['bold']), row[1], row[2]])
        globals.lastdsmcommandresults = data

        table = columnar(data2,
            headers=['#', 'VolName', 'PoolName', 'PctUtil'],
            justify=['r', 'l', 'l', 'r'])
        
        return table

define_command(ShowFilling())

class Move(SpadminCommand):
    def __init__(self):
        self.command_string = "MOve"
        self.command_type   = "MOVE"
        self.command_index  = 0

    def short_help(self) -> str:
        return 'Move data '

    def help(self) -> dict:
        return """Move data """

    def _execute(self, parameters: str) -> str:
        if globals.lastdsmcommandtype == "VOLUMES":
            if parameters.strip().isnumeric():
                if len(globals.lastdsmcommandresults) >= int(parameters) > 0:
                        line = globals.lastdsmcommandresults[int(parameters) - 1]
                        cmd = "MOVE DATA" + " " + line[1]
                        for l in globals.tsm.send_command_normal(cmd):
                            print(l)
                else:
                    print(colored("The given number is not found!", 'red', attrs=['bold']))
            else:
                print(colored("The given parameter should be a number!", 'red', attrs=['bold']))
        else:
            print(colored("Last command should be SHow Filling!", 'red', attrs=['bold']))
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


define_command(Move())


def show_scratches( self, parameters ):
    
    data = globals.tsm.send_command_array_array_tabdel( "select LIBRARY_NAME, MEDIATYPE, count(*) from libvolumes where upper(status)='SCRATCH' group by LIBRARY_NAME,MEDIATYPE" )

    if globals.last_error[ 'rc' ] != '0':
        globals.lastdsmcommandtype    = 'SCRATCHES'
        globals.lastdsmcommandresults = []
        return

    data2 = []
    for index, row in enumerate( data ):
             
        if int( row[ 2 ] ) < 5:
            scratches = colored( row[ 2 ], 'yellow', attrs=[ 'bold' ] )
        elif int( row[ 2 ] ) < 3:          
            scratches = colored( row[ 2 ], 'red', attrs=[ 'bold' ] )
        else:
            scratches = row[ 2 ]
              
        data2.append( [  row[ 0 ], row[ 1 ], scratches ] )
    
    utilities.printer( columnar( data2, 
        headers = [ 'LibraryName', 'Type', '#Scratch' ],
        justify = [ 'l', 'l', 'r' ] ) )
    
    globals.lastdsmcommandtype    = 'SCRATCHES'
    globals.lastdsmcommandresults = data2
    
spadmin_commands[ 'SHow SCRatches' ] = show_scratches
dynruleinjector(  'SHow SCRatches' )


def show_copygroups( self, parameters ):
    
    data = globals.tsm.send_command_array_array_tabdel( "select bu.DOMAIN_NAME, bu.SET_NAME, bu.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where bu.DOMAIN_NAME = DOMAIN_NAME and bu.SET_NAME = SET_NAME and bu.CLASS_NAME = CLASS_NAME ), bu.VEREXISTS, bu.VERDELETED, bu.RETEXTRA, bu.RETONLY, bu.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where bu.DESTINATION = stgp.STGPOOL_NAME) from BU_COPYGROUPS bu" )

    # data = globals.tsm.send_command_array_array_tabdel( "select bu.DOMAIN_NAME, bu.SET_NAME, bu.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where bu.DOMAIN_NAME = DOMAIN_NAME and bu.SET_NAME = SET_NAME and bu.CLASS_NAME = CLASS_NAME ), bu.VEREXISTS, bu.VERDELETED, bu.RETEXTRA, bu.RETONLY, bu.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where bu.DESTINATION = stgp.STGPOOL_NAME), ar.RETVER, ar.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where ar.DESTINATION = stgp.STGPOOL_NAME) from BU_COPYGROUPS bu, AR_COPYGROUPS ar" )

    if globals.last_error[ 'rc' ] != '0':
        globals.lastdsmcommandtype    = 'COPYGROUPS'
        globals.lastdsmcommandresults = []
        return

    unique = {}
    bu     = {}

    for index, row in enumerate( data ):
        
        if row[ 3 ] == 'Yes':
            default = colored( 'y', 'green', attrs=[ 'bold' ] )
        else:
            default = ''
            
        bunextdest = '' 
        if row[ 9 ] != '':
            bunextdest += '-> ' + row[ 9 ]
                           
        bu[ row[ 0 ] + row[ 1 ] + row[ 2 ] + default ] = [ row[ 4 ].rstrip() + ', ' + row[ 5 ].rstrip() + ', ' + row[ 6 ].rstrip() + ', ' + row[ 7 ].rstrip(), row[ 8 ], bunextdest ]

        unique[ row[ 0 ] + row[ 1 ] + row[ 2 ] + default ] = [ row[ 0 ], row[ 1 ], row[ 2 ], default ]
    
    data = globals.tsm.send_command_array_array_tabdel( "select ar.DOMAIN_NAME, ar.SET_NAME, ar.CLASS_NAME, (select DEFAULTMC from MGMTCLASSES where ar.DOMAIN_NAME = DOMAIN_NAME and ar.SET_NAME = SET_NAME and ar.CLASS_NAME = CLASS_NAME ), ar.RETVER, ar.DESTINATION, (select NEXTSTGPOOL from STGPOOLS stgp where ar.DESTINATION = stgp.STGPOOL_NAME) from AR_COPYGROUPS ar" )
    
    if globals.last_error[ 'rc' ] != '0':
        globals.lastdsmcommandtype    = 'COPYGROUPS'
        globals.lastdsmcommandresults = []
        return
    
    ar = {}
    
    for index, row in enumerate( data ):
        
        if row[ 3 ] == 'Yes':
            default = colored( 'y', 'green', attrs=[ 'bold' ] )
        else:
            default = ''
            
        arnextdest = '' 
        if row[ 6 ] != '':
            arnextdest += '-> ' + row[ 6 ]
                           
        ar[ row[ 0 ] + row[ 1 ] + row[ 2 ] + default ] = [ row[ 4 ].rstrip(), row[ 5 ], arnextdest ]

        unique[ row[ 0 ] + row[ 1 ] + row[ 2 ] + default ] = [ row[ 0 ], row[ 1 ], row[ 2 ], default ]

    data2 = []
    for key in unique:
        
        if key in bu and key in ar:
            data2.append( unique[ key ] + bu[ key ] + ar[ key ] )
        elif key in bu:
            data2.append( unique[ key ] + bu[ key ] + [ '', '', '' ] )
        elif key in ar:
            data2.append( unique[ key ] + [ '', '', '' ] + ar[ key ] )

    utilities.printer( columnar( data2, 
            headers = [ 'Domain', 'PolicySet', 'MgmtClass', 'd', 'BACopy(ve,vd,re,ro)', 'BADest', 'Next', 'ARCopy(d)', 'ARDest', 'Next' ],
            justify = [ 'l', 'l', 'l', 'l', 'c', 'l', 'l', 'c', 'l', 'l' ] ) )
    
    # utilities.printer( columnar( data2, 
    #     headers = [ 'Domain', 'PolicySet', 'MgmtClass', 'd', 'ARCopy (d)', 'ARDest', 'Next' ],
    #     justify = [ 'l', 'l', 'l', 'l', 'l', 'l', 'l' ] ) )
    
    globals.lastdsmcommandtype    = 'COPYGROUPS'
    globals.lastdsmcommandresults = data2
    
spadmin_commands[ 'SHow COPYGroups' ] = show_copygroups
dynruleinjector(  'SHow COPYGroups' )


# merge these commands to the global rules
utilities.dictmerger( globals.myIBMSPrlCompleter.rules, globals.myIBMSPrlCompleter.dynrules )
