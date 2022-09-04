import globals
import utilities
import IBMSPrlCompleter

import columnar
from termcolor import colored

columnar = columnar.Columnar()

import os

# sub injection test
global spadmin_commands
spadmin_commands = {
    
}
# command injection
spadmin_commands[ 'SHow RULer' ] = utilities.ruler
globals.myIBMSPrlCompleter.dynrules[ 'SHow' ] = []
globals.myIBMSPrlCompleter.dynrules[ 'SHow' ].append( 'RULer' )
globals.myIBMSPrlCompleter.dynrules[ 'SHow RULer' ] = []
globals.myIBMSPrlCompleter.dynrules[ 'SHow RULer' ].append( 'Help' )
globals.myIBMSPrlCompleter.dynrules[ 'SHow RULer' ].append( 'INVerse' )


def spadmin_show_cache( self, parameters ):
    data  = []
    for key in globals.myIBMSPrlCompleter.cache_hitratio:
        data.append( [ key, globals.myIBMSPrlCompleter.cache_hitratio[ key ] ] )
    
    print( columnar( data, headers=[ colored( 'Name', 'white', attrs=[ 'bold' ] ), colored( 'Value', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'c' ] ) )
#    
spadmin_commands[ 'SPadmin SHow CAche' ] = spadmin_show_cache
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ] = []
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin' ].append( 'SHow' )
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ] = []
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'CAche' )


def spadmin_show_version( self, parameters ):        
    print( 'Version: v1.0' )        
#    
spadmin_commands[ 'SPadmin SHow VERsion' ] = spadmin_show_version
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'VERsion' )


def spadmin_show_rules( self, parameters ):        
    data  = [] 
    for key in globals.myIBMSPrlCompleter.rules:
        if globals.myIBMSPrlCompleter.rules[ key ] != []:
            data.append( [ key, globals.myIBMSPrlCompleter.rules[ key ] ] )
    
    print( columnar( data, headers=[ colored( 'Regexp', 'white', attrs=[ 'bold' ] ), colored( 'Value', 'white', attrs=[ 'bold' ] ) ], justify=[ 'l', 'l' ], max_column_width = 120 ) )
    
#    
spadmin_commands[ 'SPadmin SHow RULes' ] = spadmin_show_rules
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'RULes' )


def show_actlog ( self, parameters ):
    data = None
    if parameters == None or parameters == '' or parameters == []:
        data = tsm.send_command_array_array_tabdel("q actlog")
    else:
        data = tsm.send_command_array_array_tabdel("q actlog " + parameters[0] )
    table = columnar(data, headers=['Date/Time', 'Message'])
    print(table)
#
spadmin_commands[ 'SHow ACTlog' ] = show_actlog
globals.myIBMSPrlCompleter.dynrules['SHow'].append('ACTlog')


def reload( self, parameters ):
    globals.myIBMSPrlCompleter.loadrules( globals.config.getconfiguration()['DEFAULT']['rulefile'] )
#
spadmin_commands[ 'REload' ] = reload

def spadmin_show_log( self, parameters ):
    os.system( 'open ./' + globals.config.getconfiguration()['DEFAULT']['logfile'] )
#    
spadmin_commands[ 'SPadmin SHow Log' ] = spadmin_show_log
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'Log' )


def show_stgpool( self, parameters ):
    data = globals.tsm.send_command_array_array_tabdel(
        "select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS")
    for index, row in enumerate(data):
        (a, b, c, d, e, f, g, h, i, j) = row
        if d == '':
            data[index][3] = 0
        else:
            data[index][3] = round((float(d)/1024),1)
    
    table = columnar(data, headers = [ 'Pool Name', 'Device class', 'Coll.', 'Est. Cap. (GB)',
                                    'Pct. Utilized', 'Pct. Migr.', 'High Mig.', 'Low Mig.', 'Recl. ', 'Next' ],
                     justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
    print(table)
#
spadmin_commands[ 'SHow STGpools' ] = show_stgpool
globals.myIBMSPrlCompleter.dynrules[ 'SHow' ].append( 'STGpools' )

def show_last_error ( self, parameters):
    print ("Last error message: ", globals.last_error["message"])
    print ("Last return code: ", globals.last_error["rc"])
#
spadmin_commands['SHow LASTerror'] = show_last_error
globals.myIBMSPrlCompleter.dynrules['SHow'].append('LASTerror')


def spadmin_show_extras( self, parameters ):
    print( 'CLI extra' )
    pprint( extras)        
#    
spadmin_commands[ 'SPadmin SHow EXtras' ] = spadmin_show_extras
globals.myIBMSPrlCompleter.dynrules[ 'SPadmin SHow' ].append( 'EXtras' )
    
utilities.dictmerger( globals.myIBMSPrlCompleter.rules, globals.myIBMSPrlCompleter.dynrules )