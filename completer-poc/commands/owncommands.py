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

columnar = columnar.Columnar() # columnar: table creator/formatter utility
spadmin_commands      = {}  # dictionary for the spadmin commands
disabled_words        = ['DEFAULT', 'ALIAS', 'SPADMIN']  # disabled words: used in the configuration .ini file
lastdsmcommandtype    = '?'  # last command type: used by "kill", "on", "off", etc. commands
lastdsmcommandresults = []  # last command result: used by "kill", "on", "off", etc. commands


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
        lastdsmcommandtype = self.get_command_type()
        globals.logger.debug("Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + lastdsmcommandtype + ".")


def dynruleinjector( command ):
            
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
        data.append( [ key.strip(), globals.myIBMSPrlCompleter.cache[ key ] ] )
    utilities.printer( columnar( data, headers=[ colored( 'Query', 'white', attrs=[ 'bold' ] ), colored( 'Result', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'l' ] ) )

#
spadmin_commands[ 'SPadmin SHow CAche' ] = spadmin_show_cache
dynruleinjector( 'SPadmin SHow CAche' )


def history(self, parameters):
    data = []
    rlhistfile = os.path.join("../", globals.config.getconfiguration()['SPADMIN']['historyfile'])
    if os.path.exists(rlhistfile):
        f = open(rlhistfile, "r")
        count = 0
        for line in f.readlines():
            count += 1
            data.append([count, line.strip()])
    utilities.printer( columnar( data, headers=[ colored( '#', 'white', attrs=[ 'bold' ] ), colored( 'Command', 'white', attrs=[ 'bold' ] ) ], justify=[ 'r', 'l'] ) )
#
spadmin_commands[ 'HISTory' ] = history
dynruleinjector( 'HISTory' )

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

    utilities.printer( columnar( sorted( data, key = lambda x: x[ 1 ] ), headers=[
        colored( 'Regexp', 'white', attrs=['bold'] ),
        colored( 'LVL',    'white', attrs=['bold'] ),
        colored( 'Value',  'white', attrs=['bold'] ) ],
        justify = [ 'l', 'c', 'l' ], max_column_width = 120 ) )
#
spadmin_commands[ 'SPadmin SHow RULes' ] = spadmin_show_rules
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'RULes' )
dynruleinjector( 'SPadmin SHow RULes' )


def spadmin_show_commands( self, parameters ):
    data  = []
    for key in spadmin_commands:
            data.append( [ key ] )

    utilities.printer( columnar( sorted( data ), headers=[ 
        colored( 'Command name', 'white', attrs=['bold'] ) ], 
        justify = [ 'l' ]) )
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
                     headers=['dsmadmc','PID'])
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
               
        if int( row[ 2 ] ) > 60:
            wait = colored( humanbytes.HumanBytes.format( int( row[ 2 ] ), unit="TIME_LABELS", precision = 0 ), 'red', attrs = [ 'bold' ] )            
        else: 
            wait = humanbytes.HumanBytes.format( int( row[ 2 ] ), unit="TIME_LABELS", precision = 0 )            
        
        bytes_sent     = humanbytes.HumanBytes.format( int( row[ 3 ] ), unit="BINARY_LABELS", precision = 0 )
        bytes_received = humanbytes.HumanBytes.format( int( row[ 4 ] ), unit="BINARY_LABELS", precision = 0 )
        
        mediaaccess = ''.join( row[ 8:14 ] )
                
        data2.append( [ index + 1,  row[ 0 ], row[ 1 ], wait, bytes_sent, bytes_received, row[ 5 ], row[ 6 ], row[ 7 ], mediaaccess, row[ 16 ] + row[ 15 ] ] )

    utilities.printer( columnar( data2, headers = [
        '#', 'Id', 'State', 'Wait', 'Sent', 'Received', 'Type', 'Platform', 'Name', 'MediaAccess', 'Verb' ],
        justify=[ 'r', 'c', 'c', 'r', 'r', 'r', 'r', 'c', 'l', 'l', 'l' ] ) )
    
    self.lastdsmcommandtype    = 'SESSIONS'
    self.lastdsmcommandresults = data2
    
spadmin_commands[ 'SHow SESsions' ] = show_sessions
dynruleinjector(  'SHow SESsions' )


def show_processes( self, parameters ):
    
    data = globals.tsm.send_command_array_array_tabdel( 'select PROCESS_NUM, PROCESS, FILES_PROCESSED, BYTES_PROCESSED, STATUS from processes order by 1' )

    if globals.last_error[ 'rc' ] != '0':
        self.lastdsmcommandtype = 'PROCESSES'
        self.lastdsmcommandresults = []
        return

    data2 = []
    for index, row in enumerate( data ):
               
        bytes_prcessed = humanbytes.HumanBytes.format( int( row[ 3 ] ), unit="BINARY_LABELS", precision = 0 )
              
        # Current input volume: MKP056M8. Current output volume(s): MKP074M8.
        status = row[ 4 ]
        status = sub( 'Current input volume: ([\w]+)\.', 
            lambda m: colored( m.group(1), 'green', attrs=[ 'bold' ] ), status )
        status = sub( 'Current output volume(s): ([\w]+)\.', 
            lambda m: colored( m.group(1), 'green', attrs=[ 'bold' ] ), status )
        status = sub( 'Waiting for mount of input volume ([\w]+) \(', 
        lambda m: colored( m.group(1), 'green', attrs=[ 'bold' ] ), status )


        data2.append( [ index + 1,  row[ 0 ], row[ 1 ], row[ 2 ], bytes_prcessed, status ] )
    
    utilities.printer( columnar( data2, 
        headers = [ '#', 'Proc#', 'Process', 'Files', 'Bytes', 'Status' ],
        justify = [ 'r', 'l', 'l', 'r', 'r', 'l' ] ) )
    
    self.lastdsmcommandtype    = 'PROCESSES'
    self.lastdsmcommandresults = data2
    
spadmin_commands[ 'SHow PRocesses' ] = show_processes
dynruleinjector(  'SHow PRocesses' )


def spadmin_locallog( self, parameters ):

    data = []

    logfile = open( globals.logfilename, 'r' )
    lines = logfile.readlines()
    logfile.close()

    for line in lines[ -30: ]:
        
        match = search( '^(\d{8})\s(\d{6})\s(\w+)\s(.*)$', line.rstrip() )
        if match:
            data.append( [ match[ 1 ],  match[ 2 ], match[ 3 ], match[ 4 ] ] )
        else:    
            data.append( [ '',  '', '', line ] )
                         
    
    utilities.printer( columnar( data, headers = [ 
        'Date', 'Time', 'Level', 'Text' ],
        justify=[ 'l', 'l', 'l', 'l' ] ) )
    
spadmin_commands[ 'SPadmin SHow LOCALLOG' ] = spadmin_locallog
dynruleinjector(  'SPadmin SHow LOCALLOG' )

def kill( self, parameters ):

    if lastdsmcommandtype == "PROCESSES" or lastdsmcommandtype == "SESSIONS":
        if parameters.strip().isnumeric():
            if len(lastdsmcommandresults) >= int(parameters) > 0:
                print("cancel session", lastdsmcommandresults[int(parameters)-1][1])
                for line in (globals.tsm.send_command_array_tabdel("cancel session " + lastdsmcommandresults[int(parameters)-1][1])):
                    print(line)
            else:
                print(colored("The given number is not found!", 'red', attrs=['bold']))
        else:
            print(colored("The given parameter should be a number!", 'red', attrs=['bold']))
    else:
        print(colored("Last command should be SHow SESSions or SHow PRocesses!", 'red', attrs=[ 'bold' ] ))
        print(lastdsmcommandtype)
        pprint(lastdsmcommandresults)
    
spadmin_commands[ 'KILL' ] = kill


class ShowEvents(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow EVents"
        self.command_type = "EVENT"
        self.command_index = 0

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
09/27/2022 13:00:00                                14:00:00 FILES  INC_1300     SERVER_D            Missed
        """

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

            table = (columnar(data2, headers=['StartTime >', 'ActualStart', '< Completed', 'Domain', 'ScheduleName', 'NodeName', 'Result', 'RC'], justify=['r', 'c', 'l', 'l', 'l', 'l', 'l', 'r']))
        return table


class ShowStgp(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow STGpools"
        self.command_type = "STGP"
        self.command_index = 0

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
 - Next Storage Pool name
        """

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

        table = columnar(data, headers=['PoolName', 'DeviceClass', 'Coll', 'EstCap', 'PctUtil', 'PctMigr', 'HighMig',
                                        'LowMig', 'Recl', 'Next'],
                         justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
        return table


class Ruler(SpadminCommand):
    def __init__(self):
        self.command_string = "SHow RULer"
        self.command_type = "RULER"
        self.command_index = 0

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
        lastdsmcommandtype = self.get_command_type()
        globals.logger.debug("Execution ENDED for command: " + self.get_command_string() + ". Parameters: " + parameters + ".")
        globals.logger.debug("Last command type set to: " + lastdsmcommandtype + ".")


define_command(ShowStgp())
define_command(ShowEvents())
define_command(Ruler())

# merge these commands to the global rules
utilities.dictmerger( globals.myIBMSPrlCompleter.rules, globals.myIBMSPrlCompleter.dynrules )
