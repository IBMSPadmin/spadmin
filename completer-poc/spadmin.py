#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source skeleton came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# v1.0.0

#
#       Changed: refactoring utilities, globals, IBMSPrlCompleter, DSM
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

import sys

from dsmadmc_pexpect import dsmadmc_pexpect

import columnar
columnar = columnar.Columnar()

from configuration import Configuration
from IBMSPrlCompleter import IBMSPrlCompleter

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
import utilities

########## ###############################################################################################################
# main() #  Let's dance
########## ###############################################################################################################
if __name__ == "__main__":
    
    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser( prog = colored( 'spadmin.py', 'white', attrs=[ 'bold' ] ), description = 'Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.', epilog = colored( 'Thank you very much for downloading and starting to use it!', 'white', attrs = [ 'bold' ] ) )
    
    parser.add_argument( '-d', '--debug',       action = 'store_const', const = True,          help = 'debug messages into log file' )
    parser.add_argument( '-p', '--prereqcheck', action = 'store_const', const = True,          help = 'prerequisite check' )
    parser.add_argument( '--consoleonly',       action = 'store_const', const = True,          help = 'run console mode only!' )
    parser.add_argument( '-c', '--commands',    nargs = '?',                                   help = 'autoexec command(s). Enclose the commands in quotation marks " " when multiple commands are separated by: ;' )
    parser.add_argument( '-v', '--version',     action = 'version', version = '%(prog)s v1.0', help = 'show version information' )
    
    args = parser.parse_args()

    # create a namespace for global variables
    import globals
    
    # SPadmin settings
    globals.config = Configuration( "spadmin.ini" )
    
    # Logger settings
    logging.basicConfig( filename = globals.config.getconfiguration()['DEFAULT']['logfile'],
                         filemode = 'a',
                         format   = '%(asctime)s %(levelname)s %(message)s',
                         datefmt  = '%Y%m%d %H%M%S',
                         level    = logging.INFO )
    
    globals.logger = logging.getLogger( 'spadmin.py logger' )

    # override config with cli parameters
    if args.debug:
        globals.config.getconfiguration()[ 'DEFAULT' ][ 'debug' ]       = 'True'
        globals.logger.setLevel( logging.DEBUG )
    if args.prereqcheck:
        globals.config.getconfiguration()[ 'DEFAULT' ][ 'prereqcheck' ] = 'True'     
    if args.commands:
        globals.config.getconfiguration()[ 'DEFAULT' ][ 'autoexec' ]    = args.commands

    globals.logger.info( utilities.consolefilledline( 'START ' ) )
    globals.logger.info( utilities.consolefilledline( 'START ' ) )
    globals.logger.info( utilities.consolefilledline( 'START ' ) )

    globals.logger.debug( 'ARGS: ' + pformat( args ) )
        
    # Clear screen
    if platform.system() == 'Windows':
        os.system( 'cls' )
    else:
        os.system( 'clear' )
    
    # get the screen size and store it as a global variable
    utilities.refreshrowscolumns()

    # https://patorjk.com/software/taag/#p=testall&f=Slant&t=SPadmin.py
    print( colored( '''
 ███████╗ ██████╗   █████╗  ██████╗  ███╗   ███╗ ██╗ ███╗   ██╗     ██████╗  ██╗   ██╗
 ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██║ ████╗  ██║     ██╔══██╗ ╚██╗ ██╔╝
 ███████╗ ██████╔╝ ███████║ ██║  ██║ ██╔████╔██║ ██║ ██╔██╗ ██║     ██████╔╝  ╚████╔╝ 
 ╚════██║ ██╔═══╝  ██╔══██║ ██║  ██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║     ██╔═══╝    ╚██╔╝  
 ███████║ ██║      ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ██╗ ██║         ██║   
 ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝''' ))
    print()
    print( colored(' Powerful CLI administration tool for ', 'white', attrs=[ 'bold' ] ) + colored( 'IBM', 'white', 'on_blue', attrs=[ 'bold' ] ) + colored(' Spectrum Protect aka Tivoli Storage Manager', 'white', attrs=[ 'bold' ] ) )

    print()
    print( colored( "= Welcome! Enter any IBM Spectrum Protect commands and if you're lost type Help!", 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= We're trying to breathe new life into this old school character based management interface.", 'grey', attrs=[ 'bold' ] ) )
    print( colored(  '= ', 'grey', attrs=[ 'bold' ] ) + colored( "Once you start to use it, you can't live without it!!!", 'grey', attrs=[ 'bold', 'underline' ] ) + ' 😀' )
    print( colored( '= Python3 [' + sys.version + ']', 'grey', attrs=[ 'bold' ] ) )
    print( colored( '= Your current Operating System platform is: ' + platform.platform(), 'grey', attrs=[ 'bold' ] ) )
    print( colored( '= Terminal properties: [', 'grey', attrs=[ 'bold' ] ) +  colored( str( globals.columns ), 'white', attrs=[ 'bold' ]  ) +  colored( 'x', 'grey', attrs=[ 'bold' ] ) + colored( str( globals.rows ), 'white', attrs=[ 'bold' ] ) + colored( ']', 'grey', attrs=[ 'bold' ] ) )    
    print()
    
    globals.logger.debug( 'Fork dsmadmc processes.' )
    globals.tsm = dsmadmc_pexpect( globals.config.getconfiguration()['DEFAULT']['dsmadmc_id'], globals.config.getconfiguration()['DEFAULT']['dsmadmc_password'] )
    
    globals.logger.debug( 'readline class instance' )
    globals.myIBMSPrlCompleter = IBMSPrlCompleter( )

    #print( utilities.consolefilledline( '', '-', '', globals.columns ) )

    # Command line history
    # Based on this: https://docs.python.org/3/library/readline.html
    # rlhistfile = os.path.join( os.path.expanduser( "~" ), ".python_history" )
    rlhistfile = os.path.join( "./", globals.config.getconfiguration()['DEFAULT'][ 'historyfile' ] )
    globals.logger.debug( 'readline history file: [' + rlhistfile + ']' )
    try:
        readline.read_history_file( rlhistfile )
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length( 1000 )
    except FileNotFoundError:
        pass
    # Register history file as "autosaver"
    atexit.register( readline.write_history_file, rlhistfile )
    
    globals.logger.debug( 'Inject new readline handlers for compelter and display.' )
    readline.set_completer( globals.myIBMSPrlCompleter.IBMSPcompleter )
    readline.set_completion_display_matches_hook( globals.myIBMSPrlCompleter.match_display_hook )

    # Short text help
    print()
    print( ' ' + colored( 'Short HELP:', 'cyan', attrs=[ 'bold', 'underline' ] ) )
    print( '''
      Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program or
      use: "REload" to reload the rule file! and
      use: "SHow LOG" to reach the local log file!''' )

    #utilities.ruler( utilities, '' )
    print()

    globals.logger.debug( 'Import own command.' )
    import owncommands
        
    # -----------------------------------------

    # push the autoexec command(s)
    line = ''
    if globals.config.getconfiguration()[ 'DEFAULT' ][ 'autoexec' ]:
        globals.logger.info( utilities.consolefilledline( 'Push autoexec commands into global config: [' + globals.config.getconfiguration()[ 'DEFAULT' ][ 'autoexec' ] + ']' ) )
        line = globals.config.getconfiguration()[ 'DEFAULT' ][ 'autoexec' ]

    globals.extras = {}
    # Infinite loop
    globals.logger.debug( utilities.consolefilledline( 'INPUT LOOP START ' ) )
    while True:
    
        # refresh the terminal size 
        utilities.refreshrowscolumns()

        try:
            if line == '':
                line = input( globals.myIBMSPrlCompleter.prompt() )
            
            # Skip the empty command
            if not line.rstrip():
                continue

        except KeyboardInterrupt:
            # Suppress ctrl-c
            print( '\a' ) # Bell
            #print( 'Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program ' )
            continue

        # protect the || as ##
        line = line.replace( '||', '##' )
        # simple command runner engine
        for command in line.split( ';' ):
            command = command.strip()
            # q actlog | grep alma | invgrep alma | count | mailto alma@alma.hu,korte@korte.hu ; q node
            
            # $->grep
            # $->invgrep
            # $->count
            # $->mailto
            
            # disassembly it first
            commandparts = command.split( '|' )
            # keep the first one as the main command
            command = commandparts.pop( 0 ).strip()
            
            for extracommand in commandparts:
                pairs = extracommand.split()
                if len( pairs ) > 1:
                    globals.extras[ pairs[ 0 ] ] = pairs[ 1 ].replace( '##', '|' ) # change back if exists
                else:
                    globals.extras[ pairs[ 0 ] ] = None
                    
            # it's not own command. Does the user want to possibly exit???
            if search( '^' + utilities.regexpgenerator( 'QUIt' ),   command, IGNORECASE ) or \
               search( '^' + utilities.regexpgenerator( 'LOGout' ), command, IGNORECASE ) or \
               search( '^' + utilities.regexpgenerator( 'Exit' ),   command, IGNORECASE ) or \
               search( '^' + utilities.regexpgenerator( 'BYe' ),    command, IGNORECASE ):
            
                globals.logger.debug( utilities.consolefilledline( 'INPUT LOOP END ' ) )
                
                # End of the prg
                prgend = time()
                utilities.consoleline( '-' )
                print ( 'Program execution time:', colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
                utilities.consoleline( '-' )
                
                print ( 'Background dsmadmc processes cleaning...' )
                globals.tsm.quit()
                
                sys.exit( 0 )

            # own command executor
            match = False
            # let's try to find maybe it's an own command
            for key in owncommands.spadmin_commands: 
                if search( '^' + utilities.regexpgenerator( key ), command, IGNORECASE ):
                    # just transfer the parameters
                    owncommands.spadmin_commands[ key ]( owncommands, search( '^' + utilities.regexpgenerator( key ) + '(.*)$', command, IGNORECASE )[2].strip() )
                    match = True
                    break 
            
            # if it was then go to the next command
            if match:
                line   = ''
                globals.extras = {}
                continue
            

            # No own command, no exit then let dsmadmc run the command!
            for textline in globals.tsm.send_command_normal(  command ):
                if textline != '':
                    print( textline )
            line   = ''
            globals.extras = {}
            # continue
    
    # 
    __author__     = [ "Fleischmann György", "Szabó Marcell" ]
    __copyright__  = "Copyright 2022, as The SPadmin Python Project"
    __credits__    = [ "Fleischmann György", "Szabó Marcell"]
    __license__    = "MIT"
    __version__    = "1.0.0"
    __maintainer__ = "Fleischmann György"
    __email__      = "gyorgy@fleischmann.hu"
    __status__     = "Production"