#!/usr/bin/env python3

# Python based readline completions POC
# Original idea and the base source came from: https://sites.google.com/site/xiangyangsite/home/technical-tips/software-development/python/python-readline-completions
# 

# Let's do soma mess!!!

import sys

from time import time, sleep
prgstart = time()

import datetime

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

from re import search

import logging

import atexit

# Logger settings
logging.basicConfig( filename = 'spcompl.log',
                     filemode = 'a',
                     format   = '%(asctime)s %(levelname)s %(message)s',
                     datefmt  = '%Y%m%d %H%M%S',
                     level    = logging.INFO )

#####################################
# IBMSPrlCompleter Class definition #
#####################################
class IBMSPrlCompleter:

    def __init__( self, rulefilename ):
        print( 'Loading rules...')
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
            line = line.strip()
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
        pprint( self.start )
        print( colored( 'Imported LEVEL >1 other rules', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
        pprint( self.rules )
        logging.info( 'Rule file imported as starters:\n'    + pformat( self.start ) )
        logging.info( 'Rule file imported as other rules:\n' + pformat( self.rules ) )
        consoleline( '#' )
        
        return None

    ###############      
    # tokenEngine #
    ###############  
    def tokenEngine( self, tokens ):
        logging.info( ' PROCESS TOKENS: ' + pformat( tokens ) )
        ret = []
        if len( tokens )   == 0:
            # LEVEL ?
            print( ' LEVEL ?' )
            logging.info( 'Stepped into LEVEL 0.' )
            #ret = []
        elif len( tokens ) == 1:
            # LEVEL 1 searches in start commands
            logging.info( ' Stepped into LEVEL 1.' )
            # ret = [ x + ' ' for x in self.start if x.startswith( tokens[ -1 ] ) ]
            for x in self.start:
                if x.startswith( tokens[ -1 ] ):
                    ret.append( x + ' ' )
        elif len( tokens ) == 2:
            # LEVEL 2
            logging.info( ' Stepped into LEVEL 2.' )
            # ret = [ x + ' ' for x in self.rules[ tokens[ -2 ] ] if x.startswith( tokens[ -1 ] ) ]
            #logging.info( ' and searching for pattern  I. [' + tokens[ -2 ] + ']' )
            #for x in self.rules[ tokens[ -2 ] ]:
            #    if x.startswith( tokens[ -1 ] ):
            #    #if search( tokens[ -1 ], x ):
            #        ret.append( x + ' ' )
            # try all as regexps and don't need the above part which fails if there is no real item!!!
            logging.info( ' and searching for pattern II. [' + tokens[ -2 ] + ']' )
            for key in self.rules:
                logging.info( ' and searching for pattern II. regexp [' + key + ']' )
                if search( key, tokens[ -2 ] ):
                    logging.info( ' FOUND for pattern: II. regexp [' + pformat( self.rules[key] ) + ']' )
                    for x in self.rules[key]:
                        if x.startswith( tokens[ -1 ] ):
                            ret.append( x + ' ' )
            ret = list( dict.fromkeys( ret ) ) # easy unique list just to be on the safe side, maybe we don't need this CHECK later!
        elif len( tokens ) == 3 or len( tokens ) == 4 :
            # LEVEL 3 and 4
            logging.info( ' Stepped into LEVEL 3. and 4.' )
            #if tokens[ -3 ] == 'query' and tokens[ -2 ] == 'node':
            if search( '(query|quer|que|qu|q)\s+(node|nod|no|n)', tokens[ -3 ] + ' ' + tokens[ -2 ]):
                logging.info( ' QUERY NODE command detected!' )
                nodelist = [ 'node1', 'node2', 'node3', 'node4' ]
                # ret = [ x + ' ' for x in nodelist if x.startswith( tokens[ -1 ] ) ]
                for x in nodelist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            #elif tokens[ -3 ] == 'query' and tokens[ -2 ] == 'stgpool':
            elif search( '(query|quer|que|qu|q)\s+(stgpool|stgpoo|stgpo|stgp|stg)', tokens[ -3 ] + ' ' + tokens[ -2 ]):    
                logging.info( ' QUERY STGPOOLS command detected!' )
                stgpoollist = [ 'stgpool1', 'stgpool2', 'stgpool3', 'stgpool4' ]
                # ret = [ x + ' ' for x in nodelist if x.startswith( tokens[ -1 ] ) ]
                for x in stgpoollist:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
            else:
                # ret = [ x + '' for x in self.rules[ tokens[ -2 ] ] if x.startswith( tokens[ -1 ] ) ]
                for x in self.rules[ tokens[ -2 ] ]:
                    if x.startswith( tokens[ -1 ] ):
                        ret.append( x + ' ' )
        else:
            logging.info( ' Stepped into LEVEL Bzzz...' )
        
        logging.info( ' PROCESS RETURN: ' + pformat( ret ) )
        
        return ret
        
    ##################      
    # IBMSPcompleter #
    ##################    
    def IBMSPcompleter( self, text, state ):
        logging.info( 'COMPLETER Text:  [' + text + '] and state[' + str( state ) + ']. ------------------------------------------------------------' )
        try:
            logging.info( 'readline buffer: [' + readline.get_line_buffer() + '].' )
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
                tokens.append( '' )
            results = self.tokenEngine( tokens ) + [ None ]
            logging.info( 'Results: ' + pformat( results ) + '???????????????????' )
            logging.info( 'COMPLETER results return: [' + results[ state ] + ']. -----------------------------------------------------------' )
            return results[ state ]   
        except Exception as e:
            consoleline( coloreed( 'E', 'red' ) )
            print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
            consoleline( coloreed( 'E', 'red' ) )
            
        return None

#############      
# Functions # ####################################################################
#############

def consoleline( char ):
        print( char * columns )
        
def progressbar( count, total ):
    barlength = columns - 2
    filledlength = int( round( ( barlength ) * count / float( total ) ) )

    percent = round( 100.0 * count / float( total ), 1)
    barline = '=' * filledlength + colored ( '-', 'red', attrs=[ 'bold' ] ) * ( barlength - filledlength )
    
    sys.stdout.write( '[%s]\r' % ( barline ) )
    sys.stdout.write( '[%s%s\r' % ( colored( percent, 'grey', 'on_white' ), colored( '%', 'grey', 'on_white' ) ) )
    sys.stdout.flush()
    
########## ###############################################################################################################
# main() # 
########## ###############################################################################################################

# https://patorjk.com/software/taag/#p=testall&f=Slant&t=SPadmin.py
print( colored( '''
 ███████╗██████╗  █████╗ ██████╗ ███╗   ███╗██╗███╗   ██╗   ██████╗ ██╗   ██╗
 ██╔════╝██╔══██╗██╔══██╗██╔══██╗████╗ ████║██║████╗  ██║   ██╔══██╗╚██╗ ██╔╝
 ███████╗██████╔╝███████║██║  ██║██╔████╔██║██║██╔██╗ ██║   ██████╔╝ ╚████╔╝ 
 ╚════██║██╔═══╝ ██╔══██║██║  ██║██║╚██╔╝██║██║██║╚██╗██║   ██╔═══╝   ╚██╔╝  
 ███████║██║     ██║  ██║██████╔╝██║ ╚═╝ ██║██║██║ ╚████║██╗██║        ██║   
 ╚══════╝╚═╝     ╚═╝  ╚═╝╚═════╝ ╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝╚═╝        ╚═╝''', 'white', attrs=[ 'bold' ] ) )

# Command line history
# Based on this: https://docs.python.org/3/library/readline.html
# rlhistfile = os.path.join( os.path.expanduser( "~" ), ".python_history" )
rlhistfile = os.path.join( "./", ".python_history" )
try:
    readline.read_history_file( rlhistfile )
    # default history len is -1 (infinite), which may grow unruly
    readline.set_history_length( 1000 )
except FileNotFoundError:
    pass

# Register history file autosaver
atexit.register( readline.write_history_file, rlhistfile )

myIBMSPrlCompleter = IBMSPrlCompleter( "sprules.txt" )
readline.set_completer( myIBMSPrlCompleter.IBMSPcompleter )

# Short text help
print( colored( 'Short HELP:', 'cyan' ) )
print( '''  Use: "quit" or "exit" command to leave the program or
  use: "reload" to reload the rule file!''' )

# Infinite loop
while True:
    line = input( colored( 'SP>', 'white', 'on_green', attrs=[ 'bold' ] ) + ' ' )
    if not line.rstrip():
        continue
            
    consoleline( '-' )
    print ( "You said: [" + line.strip() + "]" )
    
    if search( '^(reload|reloa|relo|rel|re)', line ):
       alma = myIBMSPrlCompleter.loadrules( "sprules.txt" )
    elif search( '^(quit|qui)', line ) or search( '^(exit|exi|ex|e)', line ):
        break
    
    consoleline( '-' )

prgend = time()
consoleline( '-' )
print ( "Program execution time:", colored( datetime.timedelta( seconds = prgend - prgstart ), 'green' ) )
consoleline( '-' )