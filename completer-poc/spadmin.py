#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# v1.0.0
#
#       Changed: IBMSPcompleter regression algorithm to a faster one
#         Added: simple debug, grep, invgrep, count, mailto handling (a later check maybe needed or not, BUT a collector certainly!!! Don't know hot to hadnle it)
#       Changed: all print( ..., end='' ) to sys.stdout.write() for better compatibility with python2
#         Added: simple cache mechanism to spsqlengine
#         Added: new rules up to 4th levels
#         Added: DSM and DSM2 pexpect classes for testing         
#         Added: ruler sub
#         Added: spadmin_settings
#         Added: simple logo
#         Added: simple match_display_hook sub
#       Changed: regexpgenerator to be able to handle multiple members
#         Added: regexpgenerator functionality
#              .
#              .
#              .
#
#         Added:
#       Changed: 
#         Fixed: 

# Let's do some mess!!!
import sys
import utilities
from DSM import DSM
import columnar
from configuration import Configuration
from IBMSPrlCompleter import IBMSPrlCompleter
columnar = columnar.Columnar()

from time import time

prgstart = time()

import datetime

try:
    import gnureadline as readline
except ImportError:
    import readline
readline.parse_and_bind( 'tab: complete' )
readline.set_completer_delims( ' ' )

import os

import platform

from termcolor import colored
if platform.system() == 'Windows':
    os.system('color')

from pprint import pprint, pformat

from re import search, IGNORECASE

import logging

import atexit

import argparse

#############
# Functions # ####################################################################
#############




def refreshrowscolumns():
    row, column = os.popen( 'stty size', 'r' ).read().split()
    globals.rows    = int( row )
    globals.columns = int( column )



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser( description = 'Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.', epilog='''
    epilog szaskalska sal slak lskal sla ksla lskskl a''')
    
    parser.add_argument( '-d', '--debug', action=argparse.BooleanOptionalAction, help='debug help' )
    parser.add_argument( '-p', '--prereqcheck', action=argparse.BooleanOptionalAction, help='prereqcheck help' )
    parser.add_argument( '--consoleonly', default=True, type=bool, help='consoleonly help' )
    parser.add_argument( '-c', '--commands', nargs='?', help='consoleonly help' )
    parser.add_argument( '-v', '--version', action='version', version='%(prog)s v1.0', help='show version information')
    
    #parser.parse_args( ['--version'] )
    #parser.print_help()
    
    ########## ###############################################################################################################
    # main() #
    ########## ###############################################################################################################

    # GLOBAL variables
    import globals
    globals.initialize()

    # SPadmin settings
    globals.config = Configuration("spadmin.ini")

    # Clear screen
    if platform.system() == 'Windows':
        os.system( 'cls' )
    else:
        os.system( 'clear' )

    refreshrowscolumns()

    # https://patorjk.com/software/taag/#p=testall&f=Slant&t=SPadmin.py
    print( colored( '''
     ███████╗ ██████╗   █████╗  ██████╗  ███╗   ███╗ ██╗ ███╗   ██╗     ██████╗  ██╗   ██╗
     ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██║ ████╗  ██║     ██╔══██╗ ╚██╗ ██╔╝
     ███████╗ ██████╔╝ ███████║ ██║  ██║ ██╔████╔██║ ██║ ██╔██╗ ██║     ██████╔╝  ╚████╔╝ 
     ╚════██║ ██╔═══╝  ██╔══██║ ██║  ██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║     ██╔═══╝    ╚██╔╝  
     ███████║ ██║      ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ██╗ ██║         ██║   
     ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝''' ))
    print( colored(' Powerful CLI administration tool for ', 'white', attrs=[ 'bold' ] ) + colored( ' IBM ', 'white', 'on_blue', attrs=[ 'bold' ] ) + colored(' Spectrum Protect aka Tivoli Storage Manager', 'white', attrs=[ 'bold' ] ) )

    print()
    print( colored( '= Python3 [' + sys.version + '] spadmin + readline DEMO POC', 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= Welcome! Enter any IBM Spectrum Protect commands and if you're lost type help!", 'grey', attrs=[ 'bold' ] ) )
    print( colored( '= Your current Operating System platform is: ' + platform.platform(), 'grey', attrs=[ 'bold' ] ) )
    print( colored( '= Terminal properties: [', 'grey', attrs=[ 'bold' ] ) +  colored( str( globals.columns ), 'white', attrs=[ 'bold' ]  ) +  colored( 'x', 'grey', attrs=[ 'bold' ] ) + colored( str( globals.rows ), 'white', attrs=[ 'bold' ] ) + colored( ']', 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= We're trying to breathe new life into this old school character based management interface.", 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= Once you start to use it, you can't live without it!!!", 'magenta', attrs=[ 'bold', 'underline' ] ) + ' 😀' )
    print()

    # Logger settings
    logfilename                   = globals.config.getconfiguration()['DEFAULT']['logfile']
    logging.basicConfig( filename = logfilename,
                         filemode = 'a',
                         format   = '%(asctime)s %(levelname)s %(message)s',
                         datefmt  = '%Y%m%d %H%M%S',
                         level    = logging.DEBUG )

    tsm = DSM(globals.config.getconfiguration()['DEFAULT'][ 'dsmadmc_id' ], globals.config.getconfiguration()['DEFAULT'][ 'dsmadmc_password' ])

    myIBMSPrlCompleter = IBMSPrlCompleter( tsm )

    print( utilities.consolefilledline( '', '-', '', globals.columns ) )

    # Command line history
    # Based on this: https://docs.python.org/3/library/readline.html
    # rlhistfile = os.path.join( os.path.expanduser( "~" ), ".python_history" )
    rlhistfile = os.path.join( "./", globals.config.getconfiguration()['DEFAULT'][ 'historyfile' ] )
    try:
        readline.read_history_file( rlhistfile )
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length( 1000 )
    except FileNotFoundError:
        pass

    # Register history file as "autosaver"
    atexit.register( readline.write_history_file, rlhistfile )
    readline.set_completer( myIBMSPrlCompleter.IBMSPcompleter )
    readline.set_completion_display_matches_hook( myIBMSPrlCompleter.match_display_hook )

    # Short text help
    print()
    print( ' ' + colored( 'Short HELP:', 'cyan', attrs=[ 'bold', 'underline' ] ) )
    print( '''
      Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program or
      use: "REload" to reload the rule file! and
      use: "SHow LOG" to reach the local log file!''' )

    utilities.ruler( '' )
    print()

    logging.info( utilities.consolefilledline( 'INPUT LOOP START ', '-', '', 120 ) )

    # sub injection test
    spadmin_commands = {
        
    }
    # command injection
    spadmin_commands[ 'SHow RULer' ] = utilities.ruler
    myIBMSPrlCompleter.rules[ 'SHow' ].append( 'RULer' )
    myIBMSPrlCompleter.rules[ 'SHow RULer' ] = []
    myIBMSPrlCompleter.rules[ 'SHow RULer' ].append( 'Help' )
    myIBMSPrlCompleter.rules[ 'SHow RULer' ].append( 'INVerse' )
    
    # Infinite loop
    while True:

        refreshrowscolumns()

        try:
          line = input( myIBMSPrlCompleter.prompt() )

          # Skip the empty command
          if not line.rstrip():
            continue

        except KeyboardInterrupt:
            # Suppress ctrl-c
            print( '\a' ) # Bell
            print('Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program ')
            continue

                                    # Own commands
        if search( '^' + utilities.regexpgenerator( 'REload' ),     line, IGNORECASE ):
            myIBMSPrlCompleter.loadrules( globals.config.getconfiguration()['DEFAULT'][ 'rulesfilename' ] )
            continue
        elif search( '^' + utilities.regexpgenerator( 'Show Log' ), line, IGNORECASE ):
            os.system( 'open ./' + logfilename )
            continue
        elif search('^' + utilities.regexpgenerator('Show STGP'), line, IGNORECASE):
            data = tsm.send_command_array_array("select STGPOOL_NAME,DEVCLASS,COLLOCATE,EST_CAPACITY_MB,PCT_UTILIZED,PCT_MIGR,HIGHMIG,LOWMIG,RECLAIM,NEXTSTGPOOL from STGPOOLS")
            for index, row in enumerate(data):
                (a, b, c, d, e, f, g, h, i, j) = row
                if d == '':
                    data[index][3] = 0
                else:
                    data[index][3] = round((float(d)/1024),1)

            table = columnar(data, headers=['Pool Name', 'Device class', 'Coll.', 'Est. Cap. (GB)',
                                            'Pct. Utilized','Pct. Migr.','High Mig.','Low Mig.','Recl. ','Next'],
                             no_borders=True, preformatted_headers=True, justify=['l', 'l', 'l', 'r', 'r', 'r', 'r', 'r', 'r', 'l'])
            print(table)
            continue
        elif search('^' + utilities.regexpgenerator('Show Actlog'), line, IGNORECASE):
            data = tsm.send_command_array_array("q actlog" )

            table = columnar(data, headers=['Date/Time', 'Message'],  no_borders=True, preformatted_headers=True)
            print(table)
            continue
        elif search( '^' + utilities.regexpgenerator( 'CAChe' ), line, IGNORECASE ):
            pprint( myIBMSPrlCompleter.cache_hitratio )
            continue
        elif search( '^' + utilities.regexpgenerator( 'QUIt' ),     line, IGNORECASE ) or \
             search( '^' + utilities.regexpgenerator( 'LOGout' ),   line, IGNORECASE ) or \
             search( '^' + utilities.regexpgenerator( 'Exit' ),     line, IGNORECASE ) or \
             search( '^' + utilities.regexpgenerator( 'BYe' ),      line, IGNORECASE ):

            # Quit the program
            break

        # simple command runner engine
        for command in line.split( ';' ):
            command = command.strip()
            # q actlog | grep alma | grep alma | count ;
            # disassembly it first
            # $->grep
            # $->invgrep
            # $->count
            # $->mailto
            # $->SPadmin

            # ha van \([\w\d|]+\), akkor védeni kell

            # own command executor
            match = False
            for key in spadmin_commands: 
                if search( '^' + utilities.regexpgenerator( key ), command, IGNORECASE ):
                    # just transfer the parameters
                    spadmin_commands[ key ]( command.split()[ 2: ] )
                    match = True
                    break 
            
            if match:
                continue
            # own command executor

            for textline in tsm.send_command2(  command ):
                if textline != '':
                    print( textline )

        #consoleline( '-' )

    logging.info( utilities.consolefilledline( 'INPUT LOOP END ', '-', '', 120 ) )

    # End of the prg
    prgend = time()
    utilities.consoleline( '-' )
    print ( 'Program execution time:', colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
    utilities.consoleline( '-' )

    sys.exit( 0 )

    __author__     = [ "Fleischmann György", "Szabó Marcell" ]
    __copyright__  = "Copyright 2022, The SPadmin Project"
    __credits__    = [ "Fleischmann György", "Szabó Marcell"]
    __license__    = "MIT"
    __version__    = "1.0.0"
    __maintainer__ = "Fleischmann György"
    __email__      = "gyorgy@fleischmann.hu"
    __status__     = "Production"