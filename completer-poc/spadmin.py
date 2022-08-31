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
from DSM import DSM
from DSM2 import DSM2
import columnar
from configuration import Configuration

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
# it moved to refreshrowscolumns()
#rows, columns = os.popen( 'stty size', 'r' ).read().split()
#rows    = int( rows )
#columns = int( columns )

import platform

from termcolor import colored
if platform.system() == 'Windows':
    os.system('color')

from pprint import pprint, pformat

from re import search, IGNORECASE

import logging

import atexit

from click import style



#####################################
# IBMSPrlCompleter Class definition #
#####################################
class IBMSPrlCompleter:

    def __init__( self, rulefilename ):
        print( ' Loading rules...                                          ')
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
        print( colored( ' Imported LEVEL 0 starters', 'green', attrs=[ 'bold' ] ) + ' from this file:\t[' + colored( rulefilename, 'green' ) + ']' )
        #pprint( self.start )
        print( colored( ' Imported LEVEL >1 other rules', 'green', attrs=[ 'bold' ] ) + ' from this file:\t[' + colored(  rulefilename, 'green' ) + ']' )
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
              # skip the previous level entries
              if len( key.split() ) + 1 < 2:
                  continue
              #logging.info( ' and searching for regexp pattern [' + key + ']' )
              #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + '(?!.*\w)' + ']' )
              if search( '^' + regexpgenerator( key ), tokens[ -2 ], IGNORECASE ):
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
                if len( key.split() ) + 1 < 3:
                    continue
                elif key.startswith( 'select' ): # ???????????????????????????????
                    continue
                #logging.info( ' and searching for regexp pattern [' + key + ']' )
                #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + ']' )
                #logging.info( ' and searching in text [' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ']' )
                if search( '^' + regexpgenerator( key ), tokens[ -3 ] + ' ' + tokens[ -2 ] + ' ' + tokens[ -1 ] , IGNORECASE ):
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
# Idea test POC $$$$$$$$$$$$$$$$$$$$$ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
###########
#             if search( '(query|quer|que|qu|q)\s+(node|nod|no|n)', tokens[ -3 ] + ' ' + tokens[ -2 ], IGNORECASE):
#                 logging.info( ' QUERY NODE command detected!' )
#                 nodelist = [ 'node1', 'node2', 'node3', 'node4' ]              
#                 for x in nodelist:
#                     if x.startswith( tokens[ -1 ] ):
#                         ret.append( x + ' ' )
#             #elif tokens[ -3 ] == 'query' and tokens[ -2 ] == 'stgpool':
#             elif search( '(query|quer|que|qu|q)\s+(stgpool|stgpoo|stgpo|stgp|stg)', tokens[ -3 ] + ' ' + tokens[ -2 ], IGNORECASE):    
#                 logging.info( ' QUERY STGPOOLS command detected!' )
#                 stgpoollist = [ 'stgpool1', 'stgpool2', 'stgpool3', 'stgpool4' ]
#                 for x in stgpoollist:
#                     if x.startswith( tokens[ -1 ] ):
#                         ret.append( x + ' ' )
#             elif search( '(nodename|nodenam|nodena|noden|node)=\w*', tokens[ -1 ], IGNORECASE ):
#                 logging.info( ' NODEname= detected!' )
#                 nodelist = [ 'node11', 'node22', 'node33', 'node44' ]              
#                 for x in nodelist:
#                     if search( '=(\w*)$', tokens[ -1 ], IGNORECASE ) and x.startswith( search( '=(\w*)$', tokens[ -1 ], IGNORECASE )[1] ):
#                         ret.append( x + ' ' )  
###########
# Idea test POC $$$$$$$$$$$$$$$$$$$$$ >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
###########
            
        elif len( tokens ) == 4:
            # LEVEL 4
            logging.info( ' Stepped into LEVEL 4.' )
            
            for key in self.rules:
                # skip the previous level entries
                if len( key.split() ) + 1 < 4:
                    continue
                elif key.startswith( 'select' ): # ???????????????????????????????
                    continue
                #logging.info( ' and searching for regexp pattern [' + key + ']' )
                #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + ']' )
                #logging.info( ' and searching in text [' + tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ']' )
                if search( '^' + regexpgenerator( key ), tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ' ' + tokens[ -1 ] , IGNORECASE ):
                    logging.info( ' and found [' + tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + '] command in the 4th LEVEL dictionary item: [' + key + '].' )
                    
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
                          
        elif len( tokens ) == 5:
            # LEVEL 5
            logging.info( ' Stepped into LEVEL 5.' )
            
            for key in self.rules:
                # skip the previous level entries
                if len( key.split() ) + 1 < 5:
                    continue
                elif key.startswith( 'select' ): # ???????????????????????????????
                    continue
                #logging.info( ' and searching for regexp pattern [' + key + ']' )
                #logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + ']' )
                #logging.info( ' and searching in text [' + tokens[ -5 ] + ' ' + tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ']' )
                if search( '^' + regexpgenerator( key ), tokens[ -5 ] + ' ' + tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ' ' + tokens[ -1 ] , IGNORECASE ):
                    logging.info( ' and found [' + tokens[ -5 ] + ' ' + tokens[ -4 ] + ' ' + tokens[ -3 ] + ' ' + tokens[ -2 ] + '] command in the 5th LEVEL dictionary item: [' + key + '].' )
                    
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
             
        else:
            logging.info( ' Stepped into LEVEL Bzzz...' )
        
        logging.info( ' Here\'s what we have in ret: [' + pformat( ret, width=180 ) + ']' )
        logging.info( ' PROCESS RETURNED.' )
        
        return ret
        
    ##################      
    # IBMSPcompleter #
    ##################
    def IBMSPcompleter_( self, text, state ):
 
      logging.info( '' )
      logging.info( consolefilledline( 'COMPLETER Text: ', '-', '[' + text + '] and state[' + str( state ) + '].', 120 ) )
      try:
          logging.info( 'Readline buffer: [' + readline.get_line_buffer() + '].' )
          
          # Read CLI and split commands
          # first ;
          # tokens = readline.get_line_buffer().split()
          tokens = readline.get_line_buffer().split( ';' )[ -1 ].split( '|' )[-1].split()
          if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
              tokens.append( '' )
          
          # Call the Engine
          self.results = self.tokenEngine( tokens ) + [ None ]
                      
          logging.info( 'RETURNED results from the engine: ' + pformat( self.results, width=180 ) )
          if self.results[ state ] == None:
              logging.info( 'COMPLETER RESULT PUSH CYCLES ENDED! --------------------------------------------------------------------------' )
              logging.info( '' )
          else:
              logging.info( consolefilledline( 'COMPLETER results push cycle: [' + results[ state ] + ']', '-', '[' + str( state ) + '] [' + self.results[ state ] + '].', 120 ) )
          
          return self.results[ state ] 
          
      except Exception as e:
          consoleline( coloreed( 'E', 'red' ) )
          print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
          consoleline( coloreed( 'E', 'red' ) )
          
      return None
      
    # v2 optimization
    rrr = []
    def IBMSPcompleter( self, text, state ):
    
        logging.info( '' )
        logging.info( consolefilledline( 'COMPLETER Text: ', '-', '[' + text + '] and state[' + str( state ) + '].', 120 ) )
        
        if len( self.rrr ) == 0:
        
            try:
                logging.info( 'Readline buffer: [' + readline.get_line_buffer() + '].' )
                
                # Read CLI and split commands
                # first ;
                # tokens = readline.get_line_buffer().split()
                tokens = readline.get_line_buffer().split( ';' )[ -1 ].split( '|' )[-1].split()
                if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
                    tokens.append( '' )
                
                # Call the Engine
                self.rrr = self.tokenEngine( tokens ) + [ None ]
                                        
                logging.info( 'RETURNED results from the engine: ' + pformat( self.rrr, width=180 ) )
                
                tmp = self.rrr.pop( 0 ) 
                logging.info( ': ' + pformat( self.rrr, width=180 ) )
                
                if tmp == None:
                    logging.info( 'COMPLETER RESULT PUSH CYCLES ENDED! --------------------------------------------------------------------------' )
                    logging.info( '' )
                else:
                  logging.info( consolefilledline( 'COMPLETER results push cycle: [' + tmp + ']', '-', '[' + str( state ) + '] [' + '].', 120 ) )
                
                return tmp
                
            except Exception as e:
                consoleline( coloreed( 'E', 'red' ) )
                print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
                consoleline( coloreed( 'E', 'red' ) )
                
        else: 
          
          tmp = self.rrr.pop( 0 )
          if tmp == None:
              self.rrr = []
          return tmp           
            
        return None

    ######################      
    # match_display_hook #
    ######################  
    def match_display_hook( self, substitution, matches, longest_match_length ):
      
      word = 1
      
      print()
      for match in matches:
        
          # cleanup for PARAMETER= values
          if search ( '^\w+=(\w+)', match ):
              ppp = search ( '^\w+=(\w+)', match )[ 1 ]
          else:
              ppp = match
              
          sys.stdout.write( ppp + '   ' )
          
          # line separation
          if word == spadmin_settings[ 'rlwordseparation' ]:
            word = 1
            print()
          word += 1
          
      sys.stdout.write( '\n' + prompt() + '' + readline.get_line_buffer() )
      # sys.stdout.flush()


#############      
# Functions # ####################################################################
#############

def consoleline( char = '-' ):
    print( char * columns )

def consolefilledline( left = '', pattern = '-', right = '', width = 80 ):
    patternwith = width - len( left ) - len( right ) - 2
    return left + ' ' + pattern * patternwith + ' ' + right
        
def progressbar( count, total ):
    barlength = columns - 2   # [...]
    filledlength = int( round( ( barlength ) * count / float( total ) ) )

    percent = round( 100.0 * count / float( total ), 1)
    barline = '=' * filledlength + colored ( '-', 'grey', attrs=[ 'bold' ] ) * ( barlength - filledlength )
    
    sys.stdout.write( '[%s]\r' % ( barline ) )
    sys.stdout.write( '[%s%s\r' % ( colored( percent, 'grey', 'on_white' ), colored( '%', 'grey', 'on_white' ) ) )
    sys.stdout.flush()

def regexpgenerator( regexp ):
  
    savelastchar = '' 
    if regexp[ -1 ] == '=':
      savelastchar = regexp[ -1 ]
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
    
    logging.info( ' SP SQL Engine reached with this select: [' + select  + '] command and' )
    logging.info( ' SP SQL Engine reached with these tokens: [' + pformat( tokens ) + '].' )

    ret = []
    
    # select preparation 
    if search( '\'(-\d)\'', select ):
        # extra index
        index = search( '\'(-\d)\'', select )[ 1 ]
        select = select.replace( str( index ), tokens[ int( index ) ] )
        logging.info( ' SP SQL Engine select index preparation result: [' + select + '].' )
    
    if search( '\{Prefix:\s+(\w+=)}', select ):
        # extra prefix
        prefix = search( '\{Prefix: (\w+=)}', select )[ 1 ]
        select = select.replace( '{Prefix: ' + prefix + '}', '' ) # remove the logic description
        select = select.replace( '%PREFIX%', prefix )   
            
        logging.info( ' SP SQL Engine select prefix preparation result: [' + select  + '].' )

    # logging.info( ' CACHE: [' + pformat( cache ) + '].' )

    # cache engine
#    if select in cache.keys() and time() - cache_timestamp[ select ] > spadmin_settings[ 'cache_age' ]:
    if select in cache.keys():
        cache_hitratio[ 'hit' ] += 1
        if time() - cache_timestamp[ select ] > spadmin_settings[ 'cache_age' ]:
            # refresh needed
            logging.info( " SP SQL Engine hit the cache but the stored one is too old." )
            logging.info( ' CACHE TIMEDIFF in second(s): [' + str( time() - cache_timestamp[ select ] ) + '].' )
            cache[ select ]           = tsm.send_command_array( select )
            cache_timestamp[ select ] = time()
            cache_hitratio[ 'hitupdate' ] += 1
    else:
        # new, init 
        logging.info( " SP SQL Engine still no cached data store a new one." )
        cache[ select ]           = tsm.send_command_array( select )
        cache_timestamp[ select ] = time()
        cache_hitratio[ 'new' ] += 1

    # logging.info( ' CACHE2: [' + pformat( cache ) + '].' )

    sqlresults = cache[ select ]
    cache_hitratio[ 'request' ] += 1 

    # if select == "select node_name from nodes":
    #     sqlresults = [ 'WINnode', 'SQLnode', 'AIXnode', 'LINUXnode', 'HPUXnode' ]
    #     sqlresults = tsm.send_command_array( select )
    # elif select == "select node_name from nodes where domain_name like where domain_name like upper( '-3' )":
    #     sqlresults = [ 'NODE_1_' + tokens[ -3 ] + '_', 'NODE_2_' + tokens[ -3 ] + '_', 'NODE_3_' + tokens[ -3 ] + '_' ]
    # elif select == "select session_id from sessions":
    #     sqlresults = [ '28', '456', '12345' ]
    #     sqlresults = tsm.send_command_array(  select )
    # elif select == "select domain_name from domains":
    #     sqlresults = [ 'WIN', 'SQL', 'AIX', 'LINUX', 'HPUX', 'TEST_DOM' ]
    #     sqlresults = tsm.send_command_array( select )
    # elif select == "select domain_name from domains {Prefix: DOmain=}":
    #     prefix = search( '(\w+=*)', tokens[ -1 ] )[ 1 ]
    #     sqlresults = [ prefix + 'WIN', prefix + 'SQL', prefix + 'AIX', prefix + 'LINUX', prefix + 'HPUX', prefix + 'TEST_DOM' ]
    # elif select == "select set_name from policysets where set_name != 'ACTIVE' and domain_name like upper( '-2' )":
    #     sqlresults = [ 'STANDARD_' + tokens[ -2 ] + '_', 'STANDARD_2_' + tokens[ -2 ] + '_', 'NONSTANDARD_' + tokens[ -2 ] + '_' ]
    # elif select == "select schedule_name from client_schedules where domain_name like upper( '-2' )":
    #     sqlresults = [ 'SCHED_1_' + tokens[ -2 ] + '_', 'SCHED_2_' + tokens[ -2 ] + '_', 'SCHED_3_' + tokens[ -2 ] + '_' ]
        
    # Filter the sqlresults with the last word if possible    
    for x in sqlresults:
        if search( '^' + tokens[ -1 ], x, IGNORECASE ):
            ret.append( x + ' ' )
        
    return ret

def prompt():
    prompt = spadmin_settings[ 'prompt' ]

    # versions    
    prompt = prompt.replace( '%SPVERSION%',  spversion )
    prompt = prompt.replace( '%SPRELEASE%',  sprelease )
    prompt = prompt.replace( '%SPLEVEL%',    splevel )
    prompt = prompt.replace( '%SPSUBLEVEL%', spsublevel )
    
    # prompt
    return prompt.replace( '%SPSERVERNAME%', spprompt )
     
def ruler():
    cc = 1
    for i in range( 1, columns + 1, 1 ):
        if i % 100:
            sys.stdout.write( ' ' ) 
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 100 else cc
    print()
    
    cc = 1
    for i in range( 1, columns + 1, 1 ):
        if i % 10:
            sys.stdout.write( ' ' ) 
        else:
            sys.stdout.write( colored( str( cc ), 'green' ) )
            cc += 1
            cc = 0 if cc == 10 else cc
    print()
    
    for i in range( 1, columns + 1, 1 ):
        c = i % 10
        if c:
            sys.stdout.write( str( c ) ) 
        else:
            sys.stdout.write( colored( str( c ), 'green' ) )


def refreshrowscolumns():
    global rows, columns
    rows, columns = os.popen( 'stty size', 'r' ).read().split()
    rows    = int( rows )
    columns = int( columns )


if __name__ == "__main__":

    ########## ###############################################################################################################
    # main() #
    ########## ###############################################################################################################

    # GLOBAL variables

    # SPadmin settings
    config = Configuration("spadmin.ini")

    spadmin_settings = {
               'cache_age'        : 60,              # cache entry age (seconds)
               'cache_disable'    : False,           # disable the dynamic SQL queries for readline
               'cache_prefetch'   : True,            # prefetch cache data when the program starts
               'rulefile'         : 'spadmin.rules', # rule file name
               'historyfile'      : '',              # history file name
               'dsmadmc_path'     : 'dsmadmc',       # the patch of dsmadmc
               'dsmadmc_id'       : 'support',       # username for dsmadmc
               'dsmadmc_password' : 'userkft1q2',    # password for dsmadmc
               'DSM_DIR'          : '',
               'DSM_OPT'          : '',
               'DSM_LOG'          : '',
               'logfile'          : 'spadmin.log',   # SPadmin main logfile
               'debug'            : False,           # enable debug info to the main logfile
               'autoexec'	        : '',              # auto command execution when spadmin starts
               'dynamic_readline' : True,            # dynamic SQL queries when TAB + TAB
               'prompt'           : '[' + colored( '%SPSERVERNAME%', 'white', attrs=[ 'bold' ] ) + '] ' + colored( '>', 'red', attrs=[ 'bold' ] ) + ' ',
               'rlwordseparation' : 8
    }

    # screen properies
    columns = 80
    rows    = 25

    # cache store
    cache           = {} # global cache data store
    cache_timestamp = {} # global cache timestamp store
    cache_hitratio  = { 'new' : 0, 'request' : 0, 'hit' : 0, 'hitupdate' : 0 }

    # SP prompt
    spprompt = ''

    # SP version
    spversion  = ''
    sprelease  = ''
    splevel    = ''
    spsublevel = ''


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
    print( colored( '= Terminal properties: [', 'grey', attrs=[ 'bold' ] ) +  colored( str( columns ), 'white', attrs=[ 'bold' ]  ) +  colored( 'x', 'grey', attrs=[ 'bold' ] ) + colored( str( rows ), 'white', attrs=[ 'bold' ] ) + colored( ']', 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= We're trying to breathe new life into this old school character based management interface.", 'grey', attrs=[ 'bold' ] ) )
    print( colored( "= Once you start to use it, you can't live without it!!!", 'magenta', attrs=[ 'bold', 'underline' ] ) + ' 😀' )
    print()

    # Logger settings
    logfilename                   = 'spadmin.log'
    logging.basicConfig( filename = logfilename,
                         filemode = 'a',
                         format   = '%(asctime)s %(levelname)s %(message)s',
                         datefmt  = '%Y%m%d %H%M%S',
                         level    = logging.DEBUG )

    print( consolefilledline( '', '-', '', columns ) )

    rulesfilename  = "spadmin.rules"
    histoyfilename = ".spadmin_history"
    #rlprompt       = colored( 'SP>', 'white', 'on_green', attrs=[ 'bold' ] ) + ' '
    sys.stdout.write( " Let's try to get the name of the server...\r" )
    tsm = DSM(spadmin_settings[ 'dsmadmc_id' ], spadmin_settings[ 'dsmadmc_password' ])
    tsm2 = DSM2(spadmin_settings[ 'dsmadmc_id' ], spadmin_settings[ 'dsmadmc_password' ])
    spprompt       = tsm.send_command_array('select SERVER_NAME from STATUS' )[ 0 ]
    sys.stdout.write( " and get the version of the IBM SP server...\r" )
    spversion, sprelease, splevel, spsublevel = tsm.send_command_array_array( 'select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS' )[ 0 ]

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
    readline.set_completion_display_matches_hook( myIBMSPrlCompleter.match_display_hook )

    # Short text help
    print()
    print( ' ' + colored( 'Short HELP:', 'cyan', attrs=[ 'bold', 'underline' ] ) )
    print( '''
      Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program or
      use: "REload" to reload the rule file! and
      use: "SHow LOG" to reach the local log file!''' )
    #print()

    #def showspadmncommand():
    #  print( '> showspadmncommand <' )
    #  return
    #spadmincommands = { 'SHow Commands' : showspadmncommand() }
    #rules[ '^' + regexpgenerator( 'SHow' ) + '\s+' + regexpgenerator( 'COMmands' )  ].append( second )
    # locals()["myfunction"]()
    #

    ruler()
    print()

    logging.info( consolefilledline( 'INPUT LOOP START ', '-', '', 120 ) )

    # Infinite loop
    while True:

        refreshrowscolumns()

        try:
          line = input( prompt() )

          # Skip the empty command
          if not line.rstrip():
            continue

        except KeyboardInterrupt:
            # Suppress ctrl-c
            print( '\a' ) # Bell
            print('Use: "QUIt", "BYe", "LOGout" or "Exit" commands to leave the program ')
            continue

        # Command executor
        #consoleline( '-' )
        #print ( ' You said: [' + line.strip() + ']' )

        # Own commands
        if search( '^' + regexpgenerator( 'REload' ),     line, IGNORECASE ):
            myIBMSPrlCompleter.loadrules( rulesfilename )
            continue
        elif search( '^' + regexpgenerator( 'Show Log' ), line, IGNORECASE ):
            os.system( 'open ./' + logfilename )
            continue
        elif search('^' + regexpgenerator('Show STGP'), line, IGNORECASE):
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
        elif search('^' + regexpgenerator('Show Actlog'), line, IGNORECASE):
            data = tsm.send_command_array_array("q actlog")
            patterns = [
                ('ANR....E', lambda text: style(text, fg='red')),
                ('ANR....W', lambda text: style(text, fg='yellow')),
            ]
            table = columnar(data, headers=['Date/Time', 'Message'], patterns=patterns, no_borders=True, preformatted_headers=True)
            print(table)
            continue
        elif search( '^' + regexpgenerator( 'CAChe' ), line, IGNORECASE ):
            pprint( cache_hitratio )
            continue
        elif search( '^' + regexpgenerator( 'QUIt' ),     line, IGNORECASE ) or \
             search( '^' + regexpgenerator( 'LOGout' ),   line, IGNORECASE ) or \
             search( '^' + regexpgenerator( 'Exit' ),     line, IGNORECASE ) or \
             search( '^' + regexpgenerator( 'BYe' ),      line, IGNORECASE ):

            # Quit the program
            break

        # simple command runner engine
        for command in line.split( ';' ):

            # q actlog | grep alma | grep alma | count ;
            # disassembly it first
            # $->grep
            # $->invgrep
            # $->count
            # $->mailto
            # $->SPadmin

            # ha van \([\w\d|]+\), akkor védeni kell

            for textline in tsm2.send_command2(  command ):
                if textline != '':
                    print( textline )

        #consoleline( '-' )

    logging.info( consolefilledline( 'INPUT LOOP END ', '-', '', 120 ) )

    # End of the prg
    prgend = time()
    consoleline( '-' )
    print ( 'Program execution time:', colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
    consoleline( '-' )

    sys.exit( 0 )

    __author__     = [ "Fleischmann György", "Szabó Marcell" ]
    __copyright__  = "Copyright 2022, The SPadmin Project"
    __credits__    = [ "Fleischmann György", "Szabó Marcell"]
    __license__    = "MIT"
    __version__    = "1.0.0"
    __maintainer__ = "Fleischmann György"
    __email__      = "gyorgy@fleischmann.hu"
    __status__     = "Production"