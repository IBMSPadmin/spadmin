import globals
import utilities
import IBMSPrlCompleter
import logging

from termcolor import colored

import columnar
columnar = columnar.Columnar()

import os
import sys

from pprint import pprint, pformat

from re import search, IGNORECASE

import humanbytes

# sub injection test
spadmin_commands = {}
disabled_words = ['DEFAULT','ALIAS','SPADMIN']

def ruler( self, parameters = '' ):
    if len( parameters ) > 0:
        if search( utilities.regexpgenerator( 'Help!' ) + '(?!.*.+)' , parameters, IGNORECASE ):
            print( '''SHow RULer: Help message!

This command will print a simple text ruler.

    SHow RULer Help!    - print this help message
    SHow RULer          - print simple ruler
    SHow RULer INVerse  - print simple inverse ruler''' )

        elif search( utilities.regexpgenerator( 'INVerse' ), parameters, IGNORECASE ):
            ruler1()
            ruler10()
            ruler100()
        else:
            print( colored( 'Wrong parameter(s)!', 'red', attrs=[ 'bold' ] ) )
    else:
        ruler100()
        ruler10()
        ruler1()

def ruler100():
    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 100:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 100 else cc
    print()


def ruler10():
    cc = 1
    for i in range( 1, globals.columns + 1, 1 ):
        if i % 10:
            sys.stdout.write( ' ' )
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 10 else cc
    print()


def ruler1():
    for i in range( 1, globals.columns + 1, 1 ):
        c = i % 10
        if c:
            sys.stdout.write( str( c ) )
        else:
            sys.stdout.write( colored( str( c ), 'green' ) )

            
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
    

# command injection
spadmin_commands[ 'SHow RULer' ] = ruler
dynruleinjector( 'SHow RULer' )
dynruleinjector( 'SHow RULer Help!' )
dynruleinjector( 'SHow RULer INVerse' )


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
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'SHow' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'Add' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin Add' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'DELete' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin DELete' ] = []
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'CAche' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'SWitch' )
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SWitch' ] = []


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
dynruleinjector( 'SPadmin SET DEBUG' )


def spadmin_show_rules( self, parameters ):
    data  = []
    for key in globals.myIBMSPrlCompleter.rules:
        if globals.myIBMSPrlCompleter.rules[ key ] != []:
            data.append( [ key, len( key.split() ),  globals.myIBMSPrlCompleter.rules[ key ] ] )

    utilities.printer( columnar( data, headers=[
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
        justify = [ 'l' ], max_column_width = 120 ) )
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

    for index, row in enumerate(data):
        (a, b) = row
       # data[index][1] = str(b).replace("Session",colored("Session","blue"))
    table = columnar(data, headers=['Date/Time', 'Message'])
    utilities.printer( table )
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
spadmin_commands[ 'SPadmin SHow Log' ] = spadmin_show_log
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'Log' )
dynruleinjector( 'SPadmin SHow Log' )


def spadmin_add_alias( self, parameters ):
    if len(str(parameters).split(':')) != 2:
        print('Please use the following command format: \'SPadmin Add ALIas cmd:command\'')
        return
    else:
        key,value = str(parameters).split(':')
        globals.aliases[key] = value
        globals.config.getconfiguration()['ALIAS'][key] = value
        globals.config.writeconfig()

#
spadmin_commands[ 'SPadmin Add ALIas' ] = spadmin_add_alias
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin Add' ].append( 'ALIas' )
dynruleinjector( 'SPadmin Add ALIas' )

def spadmin_del_alias( self, parameters ):
    if not parameters:
        print('Please use the following command format: \'SPadmin DELete ALIas cmd\'')
        return
    else:
        if parameters in globals.config.getconfiguration()['ALIAS']:
            globals.aliases.pop(parameters)
            globals.config.getconfiguration()['ALIAS'].pop(parameters)
            globals.config.writeconfig()
        else:
            print (f'The given alias \'{parameters}\' not found')
#
spadmin_commands[ 'SPadmin DELete ALIas' ] = spadmin_del_alias
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin DELete' ].append( 'ALIas' )
dynruleinjector( 'SPadmin DELete ALIas' )


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
            globals.config.getconfiguration().add_section(server)
            globals.config.getconfiguration()[server]['dsmadmc_id'] = userid
            globals.config.getconfiguration()[server]['dsmadmc_password'] = password
            globals.config.writeconfig()

spadmin_commands[ 'SPadmin Add SErver' ] = spadmin_add_server
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin Add' ].append( 'SErver' )
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
        else:
            print (f'The given server \'{server}\' not found')

#
spadmin_commands[ 'SPadmin DELete SErver' ] = spadmin_del_server
# globals.myIBMSPrlCompleter.dynrules[ 'SPadmin DELete' ].append( 'SErver' )
dynruleinjector( 'SPadmin DELete SErver' )

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
            print ("switch")
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


def show_stgpool( self, parameters ):
    data = globals.tsm.send_command_array_array_tabdel(
        "select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS")
    for index, row in enumerate(data):
        (a, b, c, d, e, f, g, h, i, j) = row
        if d == '':
            data[index][3] = 0
        else:
            data[index][3] = round((float(d)/1024),1)

    table = columnar(data, headers = [ 'Pool Name', 'Device class', 'Coll.', 'Est. Cap. (GB)', 'Pct. Utilized', 'Pct. Migr.', 'High Mig.', 'Low Mig.', 'Recl. ', 'Next' ],
                justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
    utilities.printer( table )
#
spadmin_commands[ 'SHow STGpools' ] = show_stgpool
# globals.myIBMSPrlCompleter.dynrules[ 'SHow' ].append( 'STGpools' )
dynruleinjector( 'SHow STGpools' )


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
    
    data2 = []
    for index, row in enumerate( data ):
               
        if int( row[ 2 ] ) > 60:
            wait = colored( row[ 2 ], 'red', attrs = [ 'bold' ] )            
        else: 
            wait = row[ 2 ]            
        
        bytes_sent     = humanbytes.HumanBytes.format( int( row[ 3 ] ), precision = 0 )
        bytes_received = humanbytes.HumanBytes.format( int( row[ 4 ] ), precision = 0 )
        
        mediaaccess = ''.join( row[ 8:14 ] )
        
        data2.append( [ index + 1,  row[ 0 ], row[ 1 ], row[ 2 ], bytes_sent, bytes_received, row[ 5 ], row[ 6 ], row[ 7 ], mediaaccess, row[ 16 ] + row[ 15 ] ] )
    
    utilities.printer( columnar( data2, headers = [ 
        '#', 'Id', 'State', 'Wait', 'Sent', 'Received', 'Type', 'Platform', 'Name', 'MediaAccess', 'Verb' ],
        justify=[ 'r', 'c', 'c', 'c', 'r', 'r', 'r', 'c', 'r', 'l', 'l' ] ) )
    
spadmin_commands[ 'SHow SESsions' ] = show_sessions
dynruleinjector(  'SHow SESsions' )


def show_processes( self, parameters ):
    
    data = globals.tsm.send_command_array_array_tabdel( 'select PROCESS_NUM, PROCESS, FILES_PROCESSED, BYTES_PROCESSED, STATUS from processes order by 1' )
    
    data2 = []
    for index, row in enumerate( data ):
               
        bytes_prcessed = humanbytes.HumanBytes.format( int( row[ 3 ] ), precision = 0 )
              
        data2.append( [ index + 1,  row[ 0 ], row[ 1 ], row[ 2 ], bytes_prcessed, row[ 4 ] ] )
    
    utilities.printer( columnar( data2, headers = [ 
        '#', 'Proc#', 'Process', 'Files', 'Bytes', 'Status' ],
        justify=[ 'r', 'l', 'l', 'r', 'r', 'l' ] ) )
    
spadmin_commands[ 'SHow PROCesses' ] = show_processes
dynruleinjector(  'SHow PROCesses' )

# merge these commands to the global rules
utilities.dictmerger( globals.myIBMSPrlCompleter.rules, globals.myIBMSPrlCompleter.dynrules )