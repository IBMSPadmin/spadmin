#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source skeleton came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# v1.0.0

# 
#       Changed: LVL4, 5, 6 test
#       Changed: alias v2 handler hopefully can handle regexps in aliases
#       Changed: after TAB-TAB alignment POC
#         Added: simple alias handling without alias command
#         Added: more parameters: ini, log files, rldisable, nosql, nocache, ... 
#         Fixed: owncommands parameters transfer 
#       Changed: logging to globals.logger
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

from lib import dsmadmc_pexpect as dsmadmc_pexpect

import lib.columnar
columnar = lib.columnar.Columnar()

from lib.configuration import Configuration
from lib.IBMSPrlCompleter import IBMSPrlCompleter as IBMSPrlCompleter

from time import time
prgstart = time()

import datetime

try:
    import gnureadline as readline
except ImportError:
    import readline

import os

import platform

from termcolor import colored
if platform.system() == 'Windows':
    os.system('color')

from pprint import pformat

from re import search, IGNORECASE

import logging

import atexit

import argparse


#############
# Functions # ####################################################################
#############
import lib.utilities as utilities

########## ###############################################################################################################
# main() #  Let's dance
########## ###############################################################################################################
if __name__ == '__main__':

    # https://docs.python.org/3/library/argparse.html
    parser = argparse.ArgumentParser( prog = colored( 'spadmin.py', 'white', attrs=[ 'bold' ] ), description = 'Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.', epilog = colored( 'Thank you very much for downloading and starting to use it!', 'white', attrs = [ 'bold' ] ) )

    parser.add_argument( '--consoleonly',          action = 'store_const', const = True,          help = 'run console only mode!' )
    parser.add_argument( '-c', '--commands',       type=str,                                      help = 'autoexec command(s). Enclose the commands in quotation marks " " when multiple commands are separated by: ;' )
    parser.add_argument( '-d', '--debug',           action = 'store_const', const = True,          help = 'debug messages into log file' )
    parser.add_argument( '-i', '--inifilename',     type=str,                                      help = 'ini filename' )
    parser.add_argument( '-l', '--logfilename',     type=str,                                      help = 'log filename' )
    parser.add_argument( '-m', '--norlsqlcache',    action = 'store_const', const = True,          help = 'no cache for sql queries in reradline' )
    parser.add_argument( '-n', '--norlsqlhelpepr',  action = 'store_const', const = True,          help = 'no sql queries in reradline' )
    parser.add_argument( '-p', '--prereqcheck',     action = 'store_const', const = True,          help = 'prerequisite check' )
    parser.add_argument( '-r', '--rulefilename',    type=str,                                      help = 'custom rule filename' )
    parser.add_argument( '-s', '--disablerl',       action = 'store_const', const = True,          help = 'disable readline functionality' )
    parser.add_argument( '-t', '--textcolor',       type=str,                                      help = 'specify the text color [default: "white"]' )
    parser.add_argument( '-u', '--nohumanreadable', action = 'version', version = '%(prog)s v1.0', help = 'no human readable conversions' )
    parser.add_argument( '-v', '--version',         action = 'version', version = '%(prog)s v1.0', help = 'show version information' )
    parser.add_argument( '-w', '--nowelcome',       action = 'store_const', const = True,          help = 'no welcome messages' )

    args = parser.parse_args()

    # create a namespace for global variables
    import lib.globals as globals

    # SPadmin global settings
    if args.inifilename:
        globals.config = Configuration(args.inifilename)
    else:
        globals.config = Configuration('spadmin.ini')

    if args.logfilename:
        globals.logfilename = args.logfilename
    else:
        globals.logfilename = globals.config.getconfiguration()['SPADMIN']['logfile']

    if args.rulefilename:
        globals.rulefilename = args.rulefilename
    else:
        globals.rulefilename = globals.config.getconfiguration()['SPADMIN']['rulefile']

    # Logger settings
    logging.basicConfig(filename = globals.logfilename,
                        filemode = 'a',
                        format   = '%(asctime)s %(levelname)s %(message)s',
                        datefmt  = '%Y%m%d %H%M%S',
                        level    = logging.INFO)
    # and a global object
    globals.logger = logging.getLogger('spadmin.py logger')

    # override config with the cli parameters
    if args.debug:
        globals.config.getconfiguration()['SPADMIN']['debug']       = 'True'
        globals.logger.setLevel(logging.DEBUG)

    if args.prereqcheck:
        globals.config.getconfiguration()['SPADMIN']['prereqcheck'] = 'True'

    if args.commands:
        globals.config.getconfiguration()['SPADMIN']['autoexec']    = args.commands

    if args.consoleonly:
        print("\nConsole mode...")
        utilities.start_console('', globals.config.getconfiguration()['SPADMIN']['dsmadmc_id'],
                                globals.config.getconfiguration()['SPADMIN']['dsmadmc_password'])
        quit(0)

    globals.logger.info(utilities.consolefilledline('START'))
    globals.logger.info(utilities.consolefilledline('START'))
    globals.logger.info(utilities.consolefilledline('START'))

    globals.logger.debug('ARGS: ' + pformat(args))

    # get the screen size and store it as a global variable
    utilities.refreshrowscolumns()

    if not args.nowelcome:
        # Clear screen
        if platform.system() == 'Windows':
            os.system( 'cls' )
        else:
            os.system( 'clear' )

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
        print(colored( '= Your first mac address is: ' + utilities.getmac(), 'grey', attrs=['bold']))
        print(colored( '= Terminal properties: [', 'grey', attrs=[ 'bold' ] ) + colored(str(globals.columns), 'white', attrs=['bold']) + colored('x', 'grey', attrs=['bold']) + colored(str(globals.rows), 'white', attrs=['bold']) + colored(']', 'grey', attrs=['bold']))
        print()

    globals.logger.debug('Fork dsmadmc processes.')
    globals.tsm = dsmadmc_pexpect.dsmadmc_pexpect('', globals.config.getconfiguration()['SPADMIN']['dsmadmc_id'], globals.config.getconfiguration()['SPADMIN']['dsmadmc_password'])

    globals.logger.debug('readline class instance')
    globals.myIBMSPrlCompleter = IBMSPrlCompleter()

    #print( utilities.consolefilledline( '', '-', '', globals.columns ) )

    # Command line history
    # Based on this: https://docs.python.org/3/library/readline.html
    # rlhistfile = os.path.join( os.path.expanduser( "~" ), ".python_history" )
    rlhistfile = os.path.join( "./", globals.config.getconfiguration()['SPADMIN']['historyfile'])
    globals.logger.debug('readline history file: [' + rlhistfile + ']')
    try:
        readline.read_history_file( rlhistfile )
        # default history len is -1 (infinite), which may grow unruly
        readline.set_history_length( 1000 )
    except FileNotFoundError:
        pass
    # Register history file as "autosaver"
    atexit.register( readline.write_history_file, rlhistfile )

    globals.logger.debug('Inject new readline handlers for compelter and display.')

    if not args.disablerl:
        readline.parse_and_bind( 'tab: complete' )
        readline.set_completer_delims( ' ' )
        readline.set_completer(globals.myIBMSPrlCompleter.IBMSPcompleter)
        readline.set_completion_display_matches_hook(globals.myIBMSPrlCompleter.match_display_hook)

    if not args.nowelcome:
        # Short text help
        print()
        print( ' ' + colored( 'Short HELP:', 'cyan', attrs=[ 'bold', 'underline' ] ) )
        print( '''
  Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program or
  Use: "REload" to reload the rule file! and
  Use: "SPadmin SHow LOG" or "SPadmin SHow LOCALLOG" to reach the local log file!''' )

        #utilities.ruler( utilities, '' )
        print()

    globals.logger.debug('Import own commands.')
    import commands.owncommands as owncommands

    # -----------------------------------------

    # push the autoexec command(s)
    line = ''
    if globals.config.getconfiguration()['SPADMIN']['autoexec']:
        globals.logger.info(utilities.consolefilledline('Push autoexec commands into global config: [' + globals.config.getconfiguration()['SPADMIN']['autoexec'] + ']'))
        line = globals.config.getconfiguration()['SPADMIN']['autoexec']

    globals.extras  = {}
    globals.aliases = {}
    # test aliases
    if globals.config.getconfiguration().has_section('ALIAS'):
        for key in globals.config.getconfiguration()['ALIAS'].keys():
            globals.aliases[key] = globals.config.getconfiguration()['ALIAS'][key]

 #   globals.aliases[ 'shrlr' ] = 'SHow Ruler'
 #   globals.aliases[ 'shtim' ] = 'SHow TIME'
 #   globals.aliases[ 'shtgp' ] = 'SHow STGp'
 #   globals.aliases[ 'shcac' ] = 'SPadmin SHow CAche'
 #   globals.aliases[ 'ver' ]   = 'SPadmin SHow VERsion'
 #   globals.aliases[ 'rul' ]   = 'SPadmin SHow RULes'
 #   globals.aliases[ 'deb' ]   = 'SPadmin SET DEBUG'

    # ???
    IBMSPrlCompleter.start.append( 'SESs' )
    IBMSPrlCompleter.start.append( 'DISKs' )

    # Infinite loop
    globals.logger.debug(utilities.consolefilledline('>>> INPUT LOOP START '))
    while True:

        # refresh the terminal size
        utilities.refreshrowscolumns()

        try:
            if line == '':
                line = input(globals.myIBMSPrlCompleter.prompt())
                globals.logger.info('COMMAND line received: [' + line + '].')

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
            command      = command.strip()

            # handling aliases
            # firstcmdpart = command.split( ' ' )[ 0 ]
            # if firstcmdpart.lower() in globals.aliases:
            #     command = command.replace( firstcmdpart,  globals.aliases[ firstcmdpart.lower() ] )

            # handling aliases v2
            for alias in globals.aliases:
                aliasmatch = search( '^' + utilities.regexpgenerator(alias), command, IGNORECASE)
                if aliasmatch:
                    command = command.replace(aliasmatch[ 0 ], globals.aliases[ alias])
                    break

            # disassembly it first
            commandparts = command.split( '|' )

            # keep the first one as the main command
            command = commandparts.pop( 0 ).strip()

            for extracommand in commandparts:
                pairs = extracommand.split()
                if len( pairs ) > 1:
                    globals.extras[ pairs[ 0]] = pairs[ 1].replace('##', '|') # change back if exists
                elif len( pairs ) == 1:
                    globals.extras[ pairs[ 0]] = None
                else:
                    continue

            globals.logger.info('Base command: [' + command + '] and extras: ' + pformat(globals.extras))

            # it's not own command. Does the user want to possibly exit???
            if search( '^' + utilities.regexpgenerator('QUIt'), command, IGNORECASE) or \
               search( '^' + utilities.regexpgenerator('LOGOut'), command, IGNORECASE) or \
               search( '^' + utilities.regexpgenerator('Exit'), command, IGNORECASE) or \
               search( '^' + utilities.regexpgenerator('BYe'), command, IGNORECASE):

                globals.logger.debug(utilities.consolefilledline('<<< INPUT LOOP END '))

                # exit code override if exists
                exitcode = 0
                match    = search( '^\w+\s+(\d+)', command, IGNORECASE )
                if match:
                    exitcode = int( match[ 1 ] )

                # End of the prg
                prgend = time()
                utilities.consoleline('-')
                exetime = datetime.timedelta( seconds = prgend - prgstart )
                print ( 'Program execution time:', colored( exetime, 'green' ) )
                globals.logger.info('Program execution time: ' + str(exetime) + 's')
                utilities.consoleline('-')

                print ( 'Background dsmadmc processes cleaning...' )
                globals.logger.info('Background dsmadmc processes cleaning...')
                globals.tsm.quit()

                globals.logger.info(utilities.consolefilledline('END'))
                globals.logger.info(utilities.consolefilledline('END'))
                globals.logger.info(utilities.consolefilledline('END'))

                sys.exit( exitcode )

            # own command executor
            match = False
            # let's try to find maybe it's an own command
            for key in owncommands.spadmin_commands:
                maincommandpart = search( '^' + utilities.regexpgenerator(key) + '\s+', command + ' ', IGNORECASE)
                if maincommandpart:
                    # just transfer the parameters
                    globals.logger.info('Own command found: [' + command + '] and try to execute.')
                    owncommands.spadmin_commands[ key](owncommands, command.replace(maincommandpart[ 0].strip(), '').strip())
                    match = True
                    break

            # if it was own command then go to the next command
            if match:
                line   = ''
                globals.extras = {}
                continue

            # No own command, no exit then let dsmadmc run the command!
            globals.logger.info('Pass it on to dsmadmc: [' + command + '].')
            for textline in globals.tsm.send_command_normal(command):
                if textline != '':
                    print( textline )
            line   = ''
            globals.extras = {}
            # not nice, but this is now what we have
            owncommands.lastdsmcommandtype = 'DSMADMC'
            owncommands.lastdsmcommandresults.clear()
            # continue
            
    # ---------------------------------------------------------------------------------
    # 
    __author__     = [ "Fleischmann György", "Szabó Marcell" ]
    __copyright__  = "Copyright 2022, as The SPadmin Python Project"
    __credits__    = [ "Fleischmann György", "Szabó Marcell"]
    __license__    = "MIT"
    __version__    = "1.0.0"
    __maintainer__ = "Fleischmann György"
    __email__      = "gyorgy@fleischmann.hu"
    __status__     = "Production"