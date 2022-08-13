#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# Let's do some mess!!!

import sys

from time import time, sleep
prgstart = time()

import datetime

import readline
#import gnureadline as readline
readline.parse_and_bind( 'tab: complete' )

import os
rows, columns = os.popen( 'stty size', 'r' ).read().split()
rows    = int( rows )
columns = int( columns )

import platform

from termcolor import colored
if platform.system() == 'Windows':
    os.system('color')

from pprint import pprint, pformat

from re import search, IGNORECASE

import logging

import atexit

#####################################
# IBMSPrlCompleter Class definition #
#####################################
class IBMSPrlCompleter:

    def __init__( self, rulefilename ):
        print( ' Loading rules...')
        self.loadrules( rulefilename )

    def loadrules( self, rulefilename ):
        rulefile = open( rulefilename, 'r' )
        rulefilelines = rulefile.readlines()
        self.start = [] # 1. level list
        self.rules = {} # >2. level dictionary
        i = 0
        for line in rulefilelines:
            i += 1
            progressbar( i, len( rulefilelines ) )
            # ez mi? assert?
            # assert( '->' in line )
            # Skip the remark and empty lines
            if line.startswith( "#" ) or not line.rstrip():
                continue
            line = line.strip().lower()
            first, second = line.split( '->' )
            if first == '$':
                # Starter
                self.start.append( second )
                # ??? kell ez? bezavar regexp-nél
                #if second not in self.rules:
                #    self.rules[second] = []
            else:
                if first not in self.rules:
                    self.rules[ first ] = []
                if second not in self.rules:
                    self.rules[ second ] = []
                self.rules[ first ].append( second )
                sleep( .01 )
        rulefile.close()
        print()
        
        consoleline( '#' )
        print( colored( 'Imported LEVEL 0 starters', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored( rulefilename, 'green' ) + ']' )
        #pprint( self.start )
        print( colored( 'Imported LEVEL >1 other rules', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
        #pprint( self.rules )
        logging.info( 'Rule file imported as starters:\n'    + pformat( self.start ) )
        logging.info( 'Rule file imported as other rules:\n' + pformat( self.rules ) )
        consoleline( '#' )
        
        #self.results = self.start
        #self.results += [ None ]
        
        return None

    ###############      
    # tokenEngine #
    ###############  
    def tokenEngine( self, tokens ):
        logging.info( ' PROCESS TOKENS, received tokens: ' + pformat( tokens ) )
        # Reset the results
        ret = []
        if len( tokens )   == 0:
            # LEVEL ?
            print( ' LEVEL ?' )
            logging.info( 'Stepped into LEVEL 0.' )
            
        elif len( tokens ) == 1:
            # LEVEL 1 searches in start commands
            logging.info( ' Stepped into LEVEL 1.' )
            
            # Simple check the beginning of the command
            for x in self.start:
                if search( '^' + tokens[ -1 ], x, IGNORECASE ):
                    logging.info( ' and found [' + tokens[ -1 ] + '] text in the 1st LEVEL list item: [' + x + '].' )        
                    ret.append( x + ' ' )
                    
        elif len( tokens ) == 2:
            # LEVEL 2
            logging.info( ' Stepped into LEVEL 2.' )
            
            # Let's search 
            for key in self.rules:            
              logging.info( ' and searching for regexp pattern  [' + key + ']' )
              if search( key, tokens[ -2 ], IGNORECASE ):
                  logging.info( ' and found [' + tokens[ -2 ] + '] command in the 2nd LEVEL dictionary item: [' + key + '].' )        
                  logging.info( ' let\'s continue searching with this item [' + pformat( self.rules[key], width=180 ) + ']' )
                  for x in self.rules[key]:
                      # First try as a regexp pattern!
                      if search( '^\(' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' it (regexp) starts with [' + x + ' > ' + tokens[ -1 ] + ']' )
                          ret.append( search( '^\((\w+)|', x, IGNORECASE )[1] + ' ' )
                          continue
                      # At last try as a simple text
                      elif search( '^' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' it (text) starts with [' + x + ' > ' + tokens[ -1 ] + ']' )
                          ret.append( x + ' ' )
                          continue
            
        elif len( tokens ) == 3:
            # LEVEL 3 
            logging.info( ' Stepped into LEVEL 3.' )
            
            for key in self.rules:
                logging.info( ' and searching for regexp pattern  [' + key + ']' )
                if search( key, tokens[ -3 ] + ' ' + tokens[ -2 ], IGNORECASE ):
                    logging.info( ' and found [' + tokens[ -3 ] + ' ' + tokens[ -2 ] + '] command in the 3rd LEVEL dictionary item: [' + key + '].' )
                    logging.info( ' let\'s continue searching with this item [' + pformat( self.rules[key], width=180 ) + ']' )
                    for x in self.rules[key]:
                      # First try as a regexp pattern!
                      if search( '^\(' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' it (regexp) starts with [' + x + ' > ' + tokens[ -1 ] + ']' )
                          separator = '=' if x[ -1 ] == '=' else ' '
                          ret.append( search( '^\((\w+)|', x, IGNORECASE )[1] + separator )
                          continue
                      # At last try as a simple text
                      elif search( '^' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' it (text) starts with [' + x + ' > ' + tokens[ -1 ] + ']' )
                          ret.append( x + ' ' )
                          continue
            ###########
            # Idea test POC $$$$$$$$$$$$$$$$$$$$$
            ###########
            if search( '(query|quer|que|qu|q)\s+(node|nod|no|n)', tokens[ -3 ] + ' ' + tokens[ -2 ]):
                logging.info( ' QUERY NODE command detected!' )
                nodelist = [ 'node1', 'node2', 'node3', 'node4' ]              
                for x in nodelist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            #elif tokens[ -3 ] == 'query' and tokens[ -2 ] == 'stgpool':
            elif search( '(query|quer|que|qu|q)\s+(stgpool|stgpoo|stgpo|stgp|stg)', tokens[ -3 ] + ' ' + tokens[ -2 ]):    
                logging.info( ' QUERY STGPOOLS command detected!' )
                stgpoollist = [ 'stgpool1', 'stgpool2', 'stgpool3', 'stgpool4' ]
                for x in stgpoollist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            elif search( '(nodename|nodenam|nodena|noden|node)=\w*', tokens[ -1 ] ):
                logging.info( ' NODEname= detected!' )
                nodelist = [ 'node11', 'node22', 'node33', 'node44' ]              
                for x in nodelist:
                    if search( '=(\w*)$', tokens[ -1 ], IGNORECASE ) and x.startswith( search( '=(\w*)$', tokens[ -1 ], IGNORECASE )[1] ):
                        ret.append( x + ' ' )  
        elif len( tokens ) == 4:
            # LEVEL 4
            logging.info( ' Stepped into LEVEL 4.' )
         
        else:
            logging.info( ' Stepped into LEVEL Bzzz...' )
        
        logging.info( ' PROCESS RETURNED: ' + pformat( ret, width=180 ) )
        
        return ret
        
    ##################      
    # IBMSPcompleter #
    ##################
    def IBMSPcompleter( self, text, state ):
 
        logging.info( '' )
        logging.info( consolefilledline( 'COMPLETER Text: ', '-', '[' + text + '] and state[' + str( state ) + '].', 120 ) )
        try:
            logging.info( 'Readline buffer: [' + readline.get_line_buffer() + '].' )
            
            # Read CLI and split commands
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
                tokens.append( '' )
            
            # Call the Engine
            self.results = self.tokenEngine( tokens ) + [ None ]
                        
            logging.info( 'RETURNED results from the engine: ' + pformat( self.results, width=180 ) )
            if self.results[ state ] == None:
                logging.info( 'COMPLETER RESULT PUSH CYCLES ENDED! --------------------------------------------------------------------------' )
                logging.info( '' )
            else:
                logging.info( consolefilledline( 'COMPLETER results push cycle: ', '-', '[' + str( state ) + '] [' + self.results[ state ] + '].', 120 ) )
            
            return self.results[ state ] 
            
        except Exception as e:
            consoleline( coloreed( 'E', 'red' ) )
            print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
            consoleline( coloreed( 'E', 'red' ) )
            
        return None

#############      
# Functions # ####################################################################
#############

def consoleline( char = '-' ):
    print( char * columns )

def consolefilledline( left = '', pattern = '-', right = '', width = 80 ):
    patternwith = width - len( left ) - len( right ) - 2
    return left + ' ' + pattern * patternwith + ' ' + right
        
def progressbar( count, total = columns ):
    barlength = columns - 2   # [...]
    filledlength = int( round( ( barlength ) * count / float( total ) ) )

    percent = round( 100.0 * count / float( total ), 1)
    barline = '=' * filledlength + colored ( '-', 'red', attrs=[ 'bold' ] ) * ( barlength - filledlength )
    
    sys.stdout.write( '[%s]\r' % ( barline ) )
    sys.stdout.write( '[%s%s\r' % ( colored( percent, 'grey', 'on_white' ), colored( '%', 'grey', 'on_white' ) ) )
    sys.stdout.flush()
    
########## ###############################################################################################################
# main() # 
########## ###############################################################################################################

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
 ╚══════╝ ╚═╝      ╚═╝  ╚═╝ ╚═════╝  ╚═╝     ╚═╝ ╚═╝ ╚═╝  ╚═══╝ ╚═╝ ╚═╝         ╚═╝
 Powerful CLI administration tool for IBM Spectrum Protect aka Tivoli Storage Manager''', 'white', attrs=[ 'bold' ] ) )

print()
print( colored( '= Python3 [' + sys.version + '] readline DEMO POC', 'grey', attrs=[ 'bold' ] ) )
print( colored( '= Welcome, enter SP commands if you\'re lost type help', 'grey', attrs=[ 'bold' ] ) )
print( colored( '= Your current platform is: ' + platform.platform(), 'grey', attrs=[ 'bold' ] ) )
print( colored( '= Terminal properties: [' + str(columns) + 'x' + str(rows) + ']', 'grey', attrs=[ 'bold' ] ) )
print()
 
# Logger settings
logging.basicConfig( filename = 'spcompl.log',
                      filemode = 'a',
                      format   = '%(asctime)s %(levelname)s %(message)s',
                      datefmt  = '%Y%m%d %H%M%S',
                      level    = logging.INFO )
 
print( consolefilledline( '', '-', '', columns ) )

rulesfilename  = "spadmin.rules"
histoyfilename = ".spadmin_history"
rlprompt = colored( 'SP>', 'white', 'on_green', attrs=[ 'bold' ] ) + ' '
rlprompt = '[' + colored( 'SERVER1', 'white', attrs=[ 'bold' ] ) + '] ' + colored( '>', 'red', attrs=[ 'bold' ] ) + ' '

# Command line history
# Based on this: https://docs.python.org/3/library/readline.html
# rlhistfile = os.path.join( os.path.expanduser( "~" ), ".python_history" )
rlhistfile = os.path.join( "./", histoyfilename )
try:
    readline.read_history_file( rlhistfile )
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length( 1000 )
except FileNotFoundError:
    pass

# Register history file as "autosaver"
atexit.register( readline.write_history_file, rlhistfile )

myIBMSPrlCompleter = IBMSPrlCompleter( rulesfilename )
readline.set_completer( myIBMSPrlCompleter.IBMSPcompleter )

# Short text help
print()
print( colored( 'Short HELP:', 'cyan' ) )
print( '''  Use: "quit" or "exit" command to leave the program or
  use: "reload" to reload the rule file!''' )
print()

# Infinite loop
while True:
    try:
      line = input( rlprompt )
    
      if not line.rstrip():
        continue
        
    except KeyboardInterrupt:
      # Suppress ctrl-c
      print( '\a' )
      continue
               
    consoleline( '-' )
    print ( " You said: [" + line.strip() + "]" )
    
    # Own commands
    if search( '^(reload|reloa|relo|rel|re)', line ):
        myIBMSPrlCompleter.loadrules( rulesfilename )
    elif search( '^(quit|qui)', line ) or \
         search( '^(exit|exi|ex|e)', line ):
        break
    
    consoleline( '-' )

# End of the prg
prgend = time()
consoleline( '-' )
print ( "Program execution time:", colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
consoleline( '-' )

__author__     = [ "Fleischmann György", "Szabó Marcell" ]
__copyright__  = "Copyright 2022, The SPadmin Project"
__credits__    = [ "Fleischmann György", "Szabó Marcell"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "Fleischmann György"
__email__      = "gyorgy@fleischmann.hu"
__status__     = "Production"