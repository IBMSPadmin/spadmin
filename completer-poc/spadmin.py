#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# Let's do some mess!!!

import sys

from time import time, sleep
prgstart = time()

import datetime

try:
    import gnureadline as readline
except ImportError:
    import readline
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
            # lower ??? QUIt Query
            #line = line.strip().lower()
            line = line.strip()
            first, second = line.split( '->' )
            first = first.strip()
            second = second.strip()
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

        rulefile.close()
        print()
        
        consoleline( '#' )
        print( colored( ' Imported LEVEL 0 starters', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored( rulefilename, 'green' ) + ']' )
        #pprint( self.start )
        print( colored( ' Imported LEVEL >1 other rules', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
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
        
        # Reset the results dictionary
        ret = []
        
        if len( tokens )   == 0:
            # Never happen this
            logging.info( 'Stepped into LEVEL 0.' )
            
        elif len( tokens ) == 1:
            # LEVEL 1 searches in start commands
            logging.info( ' Stepped into LEVEL 1.' )
            
            # Simple check the beginning of the command on start list
            for x in self.start:
                if search( '^' + tokens[ -1 ], x, IGNORECASE ):
                    logging.info( ' found this part [' + tokens[ -1 ] + '] of the command in the 1st LEVEL list items: [' + x + '].' )        
                    ret.append( x + ' ' )
                    
        elif len( tokens ) == 2:
            # LEVEL 2
            logging.info( ' Stepped into LEVEL 2.' )
            
            for key in self.rules:            
              #logging.info( ' and searching for regexp pattern [' + key + ']' )
              #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + '(?!.*\w)' + ']' )
              if search( '^' + regexpgenerator( key ) + '(?!.*\w)', tokens[ -2 ], IGNORECASE ):
                  logging.info( ' Found this part [' + tokens[ -2 ] + '] of the command in the 2nd LEVEL dictionary items: [' + key + '].' )
                  logging.info( ' Let\'s continue searching with this pattern [' + pformat( self.rules[key], width=180 ) + ']' )
                  for x in self.rules[key]:
                      if search( '^' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' as (regexp) starts with [' + tokens[ -1 ] + ' > ' + x + ']' )
                          ret.append( x + ' ' )
                          continue
            
        elif len( tokens ) == 3:
            # LEVEL 3 
            logging.info( ' Stepped into LEVEL 3.' )
            
            for key in self.rules:
                # skip the previous level entries
                if len( key.split() ) < 3:
                    continue
                #logging.info( ' and searching for regexp pattern [' + key + ']' )
                #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + ']' )
                #logging.info( ' and searching in text [' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ']' )
                if search( '^' + regexpgenerator( key ), tokens[ -3 ] + ' ' + tokens[ -2 ] + ' ', IGNORECASE ):
                    logging.info( ' and found [' + tokens[ -3 ] + ' ' + tokens[ -2 ] + '] command in the 3rd LEVEL dictionary item: [' + key + '].' )
                    logging.info( ' let\'s continue searching with this item(s) [' + pformat( self.rules[key], width=180 ) + ']' )
                    for x in self.rules[key]:
                      if x.startswith( 'select' ):
                          # First try as an SQL pattern!
                          logging.info( ' it\'s an SQL select [' + tokens[ -1 ] + ' > ' + x + ']' )
                          ret += spsqlengine( x.strip(), tokens )
                          continue
                      elif search( '^' + tokens[ -1 ], x, IGNORECASE ):
                          logging.info( ' as a regexp starts with [' + tokens[ -1 ] + ' > ' + x + ']' )
                          separator = '' if x[ -1 ] == '=' else ' '
                          ret.append( x + separator )
                          continue

            ###########
            # Idea test POC $$$$$$$$$$$$$$$$$$$$$
            ###########
            if search( '(query|quer|que|qu|q)\s+(node|nod|no|n)', tokens[ -3 ] + ' ' + tokens[ -2 ], IGNORECASE):
                logging.info( ' QUERY NODE command detected!' )
                nodelist = [ 'node1', 'node2', 'node3', 'node4' ]              
                for x in nodelist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            #elif tokens[ -3 ] == 'query' and tokens[ -2 ] == 'stgpool':
            elif search( '(query|quer|que|qu|q)\s+(stgpool|stgpoo|stgpo|stgp|stg)', tokens[ -3 ] + ' ' + tokens[ -2 ], IGNORECASE):    
                logging.info( ' QUERY STGPOOLS command detected!' )
                stgpoollist = [ 'stgpool1', 'stgpool2', 'stgpool3', 'stgpool4' ]
                for x in stgpoollist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            elif search( '(nodename|nodenam|nodena|noden|node)=\w*', tokens[ -1 ], IGNORECASE ):
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
        
        logging.info( ' Here\'s what we have in ret: [' + pformat( ret, width=180 ) + ']' )
        logging.info( ' PROCESS RETURNED.' )
        
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
          # first ;
          # tokens = readline.get_line_buffer().split()
          tokens = readline.get_line_buffer().split( ';' )[ -1 ].split()
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
    barline = '=' * filledlength + colored ( '-', 'grey', attrs=[ 'bold' ] ) * ( barlength - filledlength )
    
    sys.stdout.write( '[%s]\r' % ( barline ) )
    sys.stdout.write( '[%s%s\r' % ( colored( percent, 'grey', 'on_white' ), colored( '%', 'grey', 'on_white' ) ) )
    sys.stdout.flush()

def regexpgenerator( regexp ):
  
    savelastchar = '' 
    if regexp[-1] == '=':
      savelastchar = regexp[-1]
      regexp = regexp[ : -1 ]
    
    result = ''
    for part in regexp.split():
    
      if part[ 0 ].isupper():
          
        tmpregexp = part
        tmpstring = part
        for x in part:
          if tmpstring[ -1 ].isupper():
            break
          tmpstring = part[ 0 : len( tmpstring ) - 1 ]	
          tmpregexp += '|' + tmpstring
          
        result += '(' + tmpregexp + ')' 
          
      else:
        result += '(' + part + ')'	
      
      result += '\s+'
    
    return result[ :-3 ] + savelastchar

def old_regexpgenerator( regexp ):
    # Generate regular expressions pattern     
    
    tmpstring = regexp
    
    for x in regexp:
      if tmpstring[ -1 ].isupper():
        break
        
      tmpstring = regexp[ 0 : len( tmpstring ) - 1 ]	
      regexp += '|' + tmpstring
    
    return '(' + regexp + ')'
    
def spsqlengine( select, tokens = [] ):
    # Handle SQL requests
    
    logging.info( ' SP SQL Engine reached with select: [' + select  + ']' )
    logging.info( ' SP SQL Engine reached with tokens: [' + pformat( tokens ) + ']' )

    ret = []

    if select == 'select domain_name from domains':
        sqlresults = [ 'WIN', 'SQL', 'AIX', 'LINUX', 'HPUX' ] 
    elif select == "select set_name from POLICYSETS where set_name != 'ACTIVE' and domain_name like upper( '-2' )":
        sqlresults = [ 'STANDARD' ]
        
    # Filter the sqlresults with the last word if possible    
    for x in sqlresults:
        if search( '^' + tokens[ -1 ], x, IGNORECASE ):
            ret.append( x + ' ' )
        
    return ret
 
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
print( colored( '= Terminal properties: [' + str( columns ) + 'x' + str( rows ) + ']', 'grey', attrs=[ 'bold' ] ) )
print( colored( '= We\'re trying to breathe new life into this old character based management interface.', 'grey', attrs=[ 'bold' ] ) )
print()
 
# Logger settings
logfilename = 'spadmin.log'
logging.basicConfig( filename = logfilename,
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

#def showspadmncommand():
#  print( '> showspadmncommand <' )
#  return
#spadmincommands = { 'SHow Commands' : showspadmncommand() }
#rules[ '^' + regexpgenerator( 'SHow' ) + '\s+' + regexpgenerator( 'COMmands' )  ].append( second )
# locals()["myfunction"]()
#

logging.info( consolefilledline( 'INPUT LOOP START ', '-', '', 120 ) )

# Infinite loop
while True:
    try:
      line = input( rlprompt )
    
      # Skip the empty command
      if not line.rstrip():
        continue
        
    except KeyboardInterrupt:
        # Suppress ctrl-c
        print( '\a' ) # Bell
        continue
    
    # Command executor
    consoleline( '-' )
    print ( ' You said: [' + line.strip() + ']' )
    
    # Own commands
    if search( '^' + regexpgenerator( 'REload' ), line, IGNORECASE ):
        myIBMSPrlCompleter.loadrules( rulesfilename )
    elif search( '^' + regexpgenerator( 'Show Log' ), line, IGNORECASE ):
        os.system( 'open ./' + logfilename )
    elif search( '^' + regexpgenerator( 'QUIt' ), line, IGNORECASE ) or \
         search( '^' + regexpgenerator( 'LOGout' ), line, IGNORECASE ) or \
         search( '^' + regexpgenerator( 'Exit' ), line, IGNORECASE ) or \
         search( '^' + regexpgenerator( 'BYe' ), line, IGNORECASE ):
        
        # Quit the program
        break
    
    consoleline( '-' )

logging.info( consolefilledline( 'INPUT LOOP END ', '-', '', 120 ) )

# End of the prg
prgend = time()
consoleline( '-' )
print ( 'Program execution time:', colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
consoleline( '-' )

__author__     = [ "Fleischmann György", "Szabó Marcell" ]
__copyright__  = "Copyright 2022, The SPadmin Project"
__credits__    = [ "Fleischmann György", "Szabó Marcell"]
__license__    = "MIT"
__version__    = "1.0.0"
__maintainer__ = "Fleischmann György"
__email__      = "gyorgy@fleischmann.hu"
__status__     = "Production"