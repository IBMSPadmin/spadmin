#!/usr/bin/python

from time import time
start = time()

import readline
readline.parse_and_bind( 'tab: complete' )

import os
rows, columns = os.popen( 'stty size', 'r' ).read().split()

import platform

from termcolor import colored
if platform.system() == 'Windows':
    os.system('color')

from pprint import pprint

class SFACompleter:
    def __init__( self, rulefilename ):
        rulefile = open( rulefilename, 'r' )
        self.rules = {}
        self.start = []
        for line in rulefile:
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
        rulefile.close()
        
        consoleline( '#' )
        print( colored( 'Imported rules', 'green', attrs=[ 'bold' ] ) + ' from this file: [' + colored(  rulefilename, 'green' ) + ']' )
        pprint( self.rules )
        consoleline( '#' )

    def process( self, tokens ):
        if len( tokens ) == 0:
            return []
        elif len( tokens ) == 1:
            ret = [ x + ' ' for x in self.start if x.startswith( tokens[ -1 ] ) ]
        else:
            ret = [ x + ' ' for x in self.rules[ tokens[ -2 ] ] if x.startswith( tokens[ -1 ] ) ]
        return ret

    def complete( self, text, state ):
        #print( '\n' )
        #consoleline( 'D' )
        #print( 'Text:  [' + text  + ']\n' )
        #print( 'State: [' + state + ']\n' )
        #consoleline( '-' )
        #print( '\n' )
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[ -1 ] == ' ':
                tokens.append( '' )
            results = self.process( tokens )+[ None ]
            #consoleline( 'd' )
            return results[ state ]   
        except Exception as e:
            print( coloreed( '\nOS error: {0}'.format(e), 'red' ) )
            consoleline( 'E' )
        return None

def consoleline( char ):
        print( char * int( columns ) )

##########      
# main() #
##########

completer = SFACompleter( "sprules.txt" )
readline.set_completer( completer.complete )

line = input( 'SP> ' )

consoleline( '-' )
print ( "You said: [" + line.strip() + "]" )
end = time()
print ( "Execution time (s):", end - start )
consoleline( '-' )