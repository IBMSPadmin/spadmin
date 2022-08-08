#!/usr/bin/python

import sys

from time import time, sleep
start = time()

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

logging.basicConfig( filename='spcompl.log',
                     filemode='a',
                     format=  '%(asctime)s %(levelname)s %(message)s',
                     datefmt= '%Y%m%d %H%M%S',
                     level=   logging.INFO )

class SFACompleter:
    def __init__( self, rulefilename ):
        rulefile = open( rulefilename, 'r' )
        rulefilelines = rulefile.readlines()
        self.start = []
        self.rules = {}
        i = 0
        for line in rulefilelines:
            i += 1
            progressbar( i, len( rulefilelines ) )
            assert( '->' in line )
            line = line.strip()
            first, second = line.split( '->' )
            if first == '$':
                self.start.append( second )
                if second not in self.rules:
                    self.rules[second] = []
            else:
                if first not in self.rules:
                    self.rules[ first ] = []
                if second not in self.rules:
                    self.rules[ second ] = []
                self.rules[ first ].append( second )
                sleep( .05 )
        rulefile.close()
        print()
        
        consoleline( '#' )
        print( colored( 'Imported LEVEL 0 starters', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
        pprint( self.start )
        print( colored( 'Imported LEVEL >1 other rules', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
        pprint( self.rules )
        logging.info( 'Rule file imported as starters:\n'    + pformat( self.start ) )
        logging.info( 'Rule file imported as other rules:\n' + pformat( self.rules ) )
        consoleline( '#' )

    def process( self, tokens ):
        logging.info( 'PROCESS TOKENS:\n' + pformat( tokens ) )
        if len( tokens )   == 0:
            # LEVEL ?
            print( 'LEVEL ?' )
            logging.info( 'Stepped into LEVEL 0.' )
            ret = []
        elif len( tokens ) == 1:
            # LEVEL 1
            logging.info( 'Stepped into LEVEL 1.' )
            ret = [ x + ' ' for x in self.start if x.startswith( tokens[ -1 ] ) ]
        elif len( tokens ) == 2:
            # LEVEL 2
            logging.info( 'Stepped into LEVEL 2.' )
            ret = [ x + ' ' for x in self.rules[ tokens[ -2 ] ] if x.startswith( tokens[ -1 ] ) ]
        elif len( tokens ) == 3 or len( tokens ) == 4 :
            # LEVEL 3 and 4
            logging.info( 'Stepped into LEVEL 3.' )
            ret = [ x + '' for x in self.rules[ tokens[ -2 ] ] if x.startswith( tokens[ -1 ] ) ]
        else:
            logging.info( 'Stepped into LEVEL Bzzz...' )
        logging.info( 'RETURN:\n' + pformat( ret ) )
        return ret

    def complete( self, text, state ):
        logging.info( 'COMPLETE Text: [' + text + '].' )
        try:
            logging.info( 'readline buffer: [' + readline.get_line_buffer() + '].' )
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
                tokens.append( '' )
            results = self.process( tokens ) + [ None ]
            logging.info( 'Results:\n' + pformat( results ) )
            logging.info( 'Results return: [' + results[ state ] + '].' )
            return results[ state ]   
        except Exception as e:
            print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
            consoleline( 'E' )
        return None

#############      
# Functions #
#############

def consoleline( char ):
        print( char * columns )
        
def progressbar( count, total ):
    barlength = columns - 2
    filledlength = int( round( ( barlength ) * count / float( total ) ) )

    percent = round( 100.0 * count / float( total ), 1)
    barline = '=' * filledlength + colored ('-', 'red', attrs=[ 'bold' ] ) * ( barlength - filledlength )
    
    sys.stdout.write( '[%s]\r' % ( barline ) )
    sys.stdout.write( '[%s%s\r' % ( colored( percent, 'grey', 'on_white' ), colored( '%', 'grey', 'on_white' ) ) )
    sys.stdout.flush()
    
##########      
# main() #
##########

completer = SFACompleter( "sprules.txt" )
readline.set_completer( completer.complete )

line = input( colored( 'SP>', 'white', 'on_green', attrs=[ 'bold' ] ) + ' ' )

consoleline( '-' )
print ( "You said: [" + line.strip() + "]" )
end = time()
print ( "Execution time (s):", end - start )
consoleline( '-' )