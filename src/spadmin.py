#!/usr/bin/env python3 -B

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

from lib import dsmadmc_pexpect
from lib.configuration import Configuration
from lib.IBMSPrlCompleter import IBMSPrlCompleter
import lib.utilities as utilities
import lib.columnar
import lib.globals as globals

import datetime
import os
import platform
import logging
import atexit
import argparse
import readchar
import traceback
from time import time
from termcolor import colored
from pprint import pformat
from re import search, IGNORECASE, split

columnar = lib.columnar.Columnar()
prgstart = time()

try:
    import gnureadline as readline
except ImportError:
    import readline


class Spadmin(object):
    
    def run(self):
        
        args = self.getargs()
        self.setglobals(args)
        globals.logger.debug('Import own commands.')
        import commands.owncommands as owncommands

        # push the autoexec command(s)
        line = ''
        if globals.config.getconfiguration()['SPADMIN']['autoexec']:
            globals.logger.info(utilities.consolefilledline(
                'Push autoexec commands into global config: [' + globals.config.getconfiguration()['SPADMIN'][
                    'autoexec'] + ']'))
            line = globals.config.getconfiguration()['SPADMIN']['autoexec']

        globals.extras = {}
        globals.aliases = {}
        
        # load aliases
        if globals.config.getconfiguration().has_section( 'ALIAS' ):
            for key in globals.config.getconfiguration()[ 'ALIAS' ].keys():
                globals.aliases[key] = globals.config.getconfiguration()[ 'ALIAS' ][key]
                globals.logger.debug( 'Alias added at start: ' + pformat( key ) )
                IBMSPrlCompleter.start.append( key )
                # owncommands.dynruleinjector( 'SPadmin DELete ALIas ' + key.replace( ' ', '_' ) ) # this line not working! move to owncommands INIT section... ???

        # Infinite loop
        globals.logger.debug(utilities.consolefilledline('>>> INPUT LOOP START '))
        while True:

            try:
                if line == '':
                    line = input(globals.myIBMSPrlCompleter.prompt())
                    # refresh the terminal size
                    utilities.refreshrowscolumns()  # MOVED to utilities.refreshrowscolumns()

                    globals.logger.info('COMMAND line received: [' + line + '].')

                # Skip the empty command
                if not line.rstrip():
                    continue

            except KeyboardInterrupt:
                # Suppress ctrl-c
                print('\a')  # Bell
                # print( 'Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program ' )
                continue
            except EOFError:
                # Suppress ctrl-d
                print('\a')  # Bell
                # print( 'Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program ' )
                continue

            # protect the || as ##
            # line = line.replace( '||', '##' )
            # simple command runner engine
            for command in line.split(';'):
                command = command.strip()

                # handling aliases
                # firstcmdpart = command.split( ' ' )[ 0 ]
                # if firstcmdpart.lower() in globals.aliases:
                #     command = command.replace( firstcmdpart,  globals.aliases[ firstcmdpart.lower() ] )

                # handling aliases v2
                for alias in globals.aliases:
                    aliasmatch = search('^' + utilities.regexpgenerator(alias) + '\s+', command + ' ', IGNORECASE)
                    if aliasmatch:
                        command = command.replace(aliasmatch[1], globals.aliases[alias])
                        break

                # protect the || as ##
                command = command.replace('||', '##')

                # disassembly it first
                commandparts = command.split('|')

                # keep the first one as the main command
                command = commandparts.pop(0).strip()

                for extracommand in commandparts:
                    pairs = extracommand.split( None, maxsplit = 1 )
                    if len( pairs ) > 1:
                        globals.extras[pairs[0].lower()] = pairs[1].replace( '##', '|' ).strip()  # change back if exists
                    elif len( pairs ) == 1:
                        globals.extras[pairs[0].lower()] = None
                    else:
                        continue

                globals.logger.info('Base command: [' + command + '] and extras: ' + pformat(globals.extras))

                # system command 
                systemcommand = search( '^!(.+)', command )
                if systemcommand:
                    os.system( systemcommand[1] )
                    # next command               
                    line = ''
                    break
                      
                # it's not own command. Does the user want to possibly exit???
                if search('^' + utilities.regexpgenerator('QUIt') + '(?!.*\w+)', command, IGNORECASE) or \
                        search('^' + utilities.regexpgenerator('LOGOut') + '(?!.*\w+)', command, IGNORECASE) or \
                        search('^' + utilities.regexpgenerator('Exit') + '(?!.*\w+)', command, IGNORECASE) or \
                        search('^' + utilities.regexpgenerator('Exit') + '\s+\d+', command, IGNORECASE) or \
                        search('^' + utilities.regexpgenerator('BYe') + '(?!.*\w+)', command, IGNORECASE):

                    globals.logger.debug(utilities.consolefilledline('<<< INPUT LOOP END '))

                    # exit code override if exists
                    exitcode = 0
                    match = search('^\w+\s+(\d+)', command, IGNORECASE)
                    if match:
                        exitcode = int(match[1])

                    # End of the prg
                    prgend = time()
                    utilities.consoleline('-')
                    exetime = datetime.timedelta(seconds=prgend - prgstart)
                    print('Program execution time:', colored(exetime, globals.color_green))
                    globals.logger.info('Program execution time: ' + str(exetime) + 's')
                    utilities.consoleline('-')

                    print('Background dsmadmc processes cleaning...')
                    globals.logger.info('Background dsmadmc processes cleaning...')
                    globals.tsm.quit()

                    globals.logger.info(utilities.consolefilledline('END'))
                    globals.logger.info(utilities.consolefilledline('END'))
                    globals.logger.info(utilities.consolefilledline('END'))

                    sys.exit(exitcode)

                # own command executor
                match = False
                # let's try to find maybe it's an own command
                for key in owncommands.spadmin_commands:
                    maincommandpart = search('^' + utilities.regexpgenerator(key) + '\s+', command + ' ', IGNORECASE)
                    if maincommandpart:
                        # just transfer the parameters
                        globals.logger.info('Own command found: [' + command + '] and try to execute.')
                        owncommands.spadmin_commands[key](owncommands,
                                                          command.replace(maincommandpart[0].strip(), '').strip())
                        match = True
                        break

                # if it was own command then go to the next command
                if match:
                    line = ''
                    globals.extras = {}
                    continue

                # No own command, no exit then let dsmadmc run the command!
                globals.logger.info('Pass it on to dsmadmc: [' + command + '].')


                ret = []
                # Remove empty lines and other "technical/administartive' texts
                for i in globals.tsm.send_command_normal(command).splitlines()[1:]:
                    if search('^Session established with server \w+:', i):
                        continue
                    elif search('^\s\sServer Version \d+, Release \d+, Level \d+.\d\d\d', i):
                        continue
                    elif search('^\s\sServer date\/time\:', i):
                        continue
                    elif i is None or i == '':
                        continue
                    tmp = []
                    tmp.append(i)
                    ret.append(tmp)

                # use grep and invgrep, which uses 'array in an array' as an input
                data = []
                for i in lib.columnar.invgrep(lib.columnar.grep(ret)):
                    data.append(i[0])

                # printer: handles more, count, etc. in a plain string
                utilities.printer('\n'.join(data))

                line           = ''
                globals.extras = {}

                # not nice, but this is now what we have
                globals.lastdsmcommandtype = 'DSMADMC'
                globals.lastdsmcommandresults.clear()

                # continue

    def setglobals(self, args):
        # SPadmin global settings

        ## COLORS:
        globals.color_cyan = 'cyan'
        globals.color_white = 'white'
        globals.color_green = 'green'
        globals.color_red = 'red'
        globals.color_yellow = 'yellow'
        globals.color_on_blue = 'on_blue'
        globals.color_on_white = 'on_white'
        globals.color_grey = 'grey'
        globals.color_attrs_bold= 'bold'
        globals.color_attrs_underline = 'underline'

        # prereq check
        globals.spadmin_path = os.path.expanduser( '~/spadmin/' )
        if not os.path.exists( globals.spadmin_path ):
            os.makedirs( globals.spadmin_path )
            print( globals.spadmin_path + ' directory created.' )
        
        globals.spadmin_logpath = os.path.join( globals.spadmin_path, 'log' )
        if not os.path.exists( globals.spadmin_logpath ):
            os.makedirs( globals.spadmin_logpath )
            print( globals.spadmin_logpath + ' directory created.' )
        
        globals.spadmin_tmpath = os.path.join( globals.spadmin_path, 'TMQueries' )
        if not os.path.exists( globals.spadmin_tmpath ):
            os.makedirs( globals.spadmin_tmpath )
            print( globals.spadmin_tmpath + ' directory created.' )
            
        if args.inifilename:
            globals.config = Configuration(args.inifilename)
        else:
            globals.config = Configuration(None)

        if args.logfilename:
            globals.logfilename = args.logfilename
        else:
            globals.logfilename = globals.config.getconfiguration()['SPADMIN']['logfile']

        globals.logfilename = os.path.join( globals.spadmin_logpath, globals.logfilename )

        #if args.rulefilename:
        #    globals.rulefilename = args.rulefilename
        #else:
        #    globals.rulefilename = globals.config.getconfiguration()['SPADMIN']['rulefile']
        # Logger settings
        logging.basicConfig(filename=globals.logfilename,
                            filemode='a',
                            format='%(asctime)s %(levelname)s %(message)s',
                            datefmt='%Y%m%d %H%M%S',
                            level=logging.INFO)
        # and a global object
        globals.logger = logging.getLogger('spadmin.py logger')

        # override config with the cli parameters
        if args.debug:
            globals.config.getconfiguration()['SPADMIN']['debug'] = 'True'
            globals.logger.setLevel(logging.DEBUG)

        globals.server = ''
        globals.userid = globals.config.getconfiguration()['SPADMIN']['dsmadmc_id']
        globals.password = utilities.decode(globals.config.getconfiguration()['SPADMIN']['dsmadmc_password'])

        if args.SErveraddress:
            globals.server = str(args.SErveraddress).upper()
            globals.userid = globals.config.getconfiguration()[globals.server]['dsmadmc_id']
            globals.password = utilities.decode(globals.config.getconfiguration()[globals.server]['dsmadmc_password'])


        if args.prereqcheck:
            globals.config.getconfiguration()['SPADMIN']['prereqcheck'] = 'True'

        if args.autoexec:
            globals.config.getconfiguration()['SPADMIN']['autoexec'] = args.autoexec
            
        globals.basecommandname = "SHow"    
        if args.basecommandname:
            globals.basecommandname = args.basecommandname
        elif globals.config.getconfiguration()['SPADMIN'].get( 'basecommandname' ) is not None:
            globals.basecommandname = globals.config.getconfiguration()['SPADMIN']['basecommandname']
        
        if args.consoleonly:
            print("\nConsole mode...")
            utilities.start_console(globals.server, globals.userid,  globals.password)
            quit(0)

        globals.logger.info(utilities.consolefilledline('START'))
        globals.logger.info(utilities.consolefilledline('START'))
        globals.logger.info(utilities.consolefilledline('START'))

        globals.logger.debug('ARGS: ' + pformat(args))


        # get the screen size and store it as a global variable
        utilities.refreshrowscolumns()

        if not args.nowelcome:
            self.welcome()
        utilities.validate_license()
        
        globals.logger.debug('Fork dsmadmc processes.')
        globals.tsm = dsmadmc_pexpect.dsmadmc_pexpect(globals.server, globals.userid, globals.password )

        globals.logger.debug('readline class instance')
        globals.myIBMSPrlCompleter = IBMSPrlCompleter()
        rlhistfile = os.path.join(globals.spadmin_path, globals.config.getconfiguration()['SPADMIN']['historyfile'] )
        globals.logger.debug( 'readline history file: [' + rlhistfile + ']' )
        try:
            readline.read_history_file(rlhistfile)
            # default history len is -1 (infinite), which may grow unruly
            readline.set_history_length(1000)
        except FileNotFoundError:
            pass
        # Register history file as "autosaver"
        atexit.register( readline.write_history_file, rlhistfile )

        globals.logger.debug('Inject new readline handlers for compelter and display.')

        if not args.disablerl:
            readline.parse_and_bind('tab: complete')
            readline.set_completer_delims(' ')
            readline.set_completer(globals.myIBMSPrlCompleter.IBMSPcompleter)
            readline.set_completion_display_matches_hook(globals.myIBMSPrlCompleter.match_display_hook)

        if args.fetch or globals.config.getconfiguration()['SPADMIN']['cache_prefetch'] == 'True':
            globals.logger.info('SQL prefetch for faster readline queries.')
            print('SQL prefetch for faster readline queries...')
            globals.myIBMSPrlCompleter.spsqlengine('select node_name from nodes', ['prefetch'])
            globals.myIBMSPrlCompleter.spsqlengine('select domain_name from domains', ['prefetch'])
            globals.myIBMSPrlCompleter.spsqlengine('select stgpool_name from stgpools', ['prefetch'])
        # -----------------------------------------

    def welcome(self):
           # Clear screen
            if platform.system() == 'Windows':
                os.system('cls')
            else:
                os.system('clear')

            # https://patorjk.com/software/taag/#p=testall&f=Slant&t=SPadmin.py
            print(colored('''
 ███████╗ ██████╗   █████╗  ██████╗  ███╗   ███╗ ██╗ ███╗   ██╗     ██████╗  ██╗   ██╗
 ██╔════╝ ██╔══██╗ ██╔══██╗ ██╔══██╗ ████╗ ████║ ██║ ████╗  ██║     ██╔══██╗ ╚██╗ ██╔╝
 ███████╗ ██████╔╝ ███████║ ██║  ██║ ██╔████╔██║ ██║ ██╔██╗ ██║     ██████╔╝  ╚████╔╝ 
 ╚════██║ ██╔═══╝  ██╔══██║ ██║  ██║ ██║╚██╔╝██║ ██║ ██║╚██╗██║     ██╔═══╝    ╚██╔╝  
 ███████║ ██║      ██║  ██║ ██████╔╝ ██║ ╚═╝ ██║ ██║ ██║ ╚████║ ██╗ ██║         ██║   
 ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝'''))
            print()
            print(colored(' Powerful CLI administration tool for ', globals.color_white, attrs=[globals.color_attrs_bold]) + colored('IBM', globals.color_white,
                                                                                                       globals.color_on_blue,
                                                                                                       attrs=[
                                                                                                           globals.color_attrs_bold]) + colored(
                ' Spectrum Protect aka Tivoli Storage Manager', globals.color_white, attrs=[globals.color_attrs_bold]))

            print()
            print(colored("= Welcome! Enter any IBM Spectrum Protect commands and if you're lost type Help!", 'grey', attrs=[globals.color_attrs_bold]))
            print(colored("= We're trying to breathe new life into this old school character based management interface.", 'grey', attrs=[globals.color_attrs_bold]))
            print(colored('= ', 'grey', attrs=[globals.color_attrs_bold]) + colored("Once you start to use it, you can't live without it!!!", 'grey', attrs=[globals.color_attrs_bold, 'underline']) + ' 😀')
            print(colored('= Python3 [' + sys.version + ']', 'grey', attrs=[globals.color_attrs_bold]))
            print(colored('= Your current Operating System platform is: ' + platform.platform(), 'grey', attrs=[globals.color_attrs_bold]))
            print(colored('= Your first mac address is: ' + utilities.getmac(), 'grey', attrs=[globals.color_attrs_bold]))
            print(colored('= Terminal properties: [', 'grey', attrs=[globals.color_attrs_bold]) + colored(str(globals.columns), globals.color_white, attrs=[globals.color_attrs_bold]) + colored('x', 'grey', attrs=[ globals.color_attrs_bold]) + colored(
                str(globals.rows), globals.color_white, attrs=[globals.color_attrs_bold]) + colored(']', 'grey', attrs=[globals.color_attrs_bold]))
            # Short text help
            print()
            print(' ' + colored('Short HELP:', globals.color_cyan, attrs=[globals.color_attrs_bold, globals.color_attrs_underline]))
            print('''
    Use: "QUIt", "BYe", "LOGOut" or "Exit" commands to leave the program or
    Use: "SPadmin SHow LOG" or "SPadmin SHow LOCALLOG" to load the log file!''')
            print()

    def getargs(self):
        # https://docs.python.org/3/library/argparse.html
        parser = argparse.ArgumentParser(prog=colored('spadmin.py', 'white', attrs=['bold']),
                                         description='Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager.',
                                         epilog=colored('Thank you very much for downloading and starting to use it!',
                                                        'white', attrs=['bold']))
        parser.add_argument('-a', '--autoexec', type=str,
                             help='autoexec command(s). Enclose the commands in quotation marks " " when multiple commands are separated by: ;')
        parser.add_argument('-b', '--basecommandname', type=str, help='custom base command name, default: SHow')
        parser.add_argument('-c', '--consoleonly', action='store_const', const=True, help='run console only mode!')
        parser.add_argument('-d', '--debug', action='store_const', const=True, help='debug messages into log file')
        parser.add_argument('-f', '--fetch', action='store_const', const=True, help='enable SQL prefetch queries')
        parser.add_argument('-i', '--inifilename', type=str, help='ini filename')
        parser.add_argument('-l', '--logfilename', type=str, help='log filename')
        parser.add_argument('-m', '--norlsqlcache', action='store_const', const=True,
                            help='no cache for SQL queries in reradline')
        parser.add_argument('-n', '--norlsqlhelper', action='store_const', const=True,
                            help='no SQL queries in reradline')
        parser.add_argument('-p', '--prereqcheck', action='store_const', const=True, help='prerequisite check')
        # parser.add_argument('-r', '--rulefilename', type=str, help='custom rule filename')
        parser.add_argument('-s', '--disablerl', action='store_const', const=True,
                            help='disable readline functionality')
        parser.add_argument('-se', '--SErveraddress', type=str,
                            help='spadmin uses the server stanza to determine the server to connects to')

        parser.add_argument('-t', '--textcolor', type=str, help='specify the text color [default: "white"]')
        parser.add_argument('-u', '--nohumanreadable', action='version', version='%(prog)s v1.0',
                            help='no human readable conversions')
        parser.add_argument('-v', '--version', action='version', version='%(prog)s v1.0',
                            help='show version information')
        parser.add_argument('-w', '--nowelcome', action='store_const', const=True, help='no welcome messages')
        return parser.parse_args()

if __name__ == '__main__':
    try:
        Spadmin().run()
    except Exception as e:
        print ("Strange things are always happens...")
        print (traceback.format_exc())

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
