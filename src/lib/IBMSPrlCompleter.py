import sys
from . import utilities
from . import globals
import logging
import os

from termcolor import colored
from pprint import pformat
from re import search, IGNORECASE, escape, findall
from time import time

try:
    import gnureadline as readline
except ImportError:
    import readline
#readline.parse_and_bind( 'tab: complete' )
#readline.set_completer_delims( ' ' )


#####################################
# IBMSPrlCompleter Class definition #
#####################################
class IBMSPrlCompleter:
    # rows = None
    # columns = None
    # logging = None
    # config = None
    # tsm = None
    # spversion = None
    # sprelease = None
    # splevel = None
    # spsublevel = None
    # spprompt = None

    # cache store
    cache           = {} # global cache data store
    cache_timestamp = {} # global cache timestamp store
    cache_hitratio  = { 'new' : 0, 'request' : 0, 'hit' : 0, 'hitupdate' : 0 }

    def __init__( self ):
        
        sys.stdout.write("Let's try to get the name of the server... ")
        sys.stdout.flush()
        globals.spservername = globals.tsm.send_command_array_tabdel('select SERVER_NAME from STATUS')[0]
        sys.stdout.write( '\r' )
        
        sys.stdout.write("and get the version of the IBM SP server...")
        sys.stdout.flush()
        globals.spversion, globals.sprelease, globals.splevel, globals.spsublevel = globals.tsm.send_command_array_array_tabdel('select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS')[0]
        sys.stdout.write( '\r' )

        # self.rows       = globals.rows
        # self.columns    = globals.columns
        # self.config     = globals.config
        # self.tsm        = tsm
        # self.spversion  = spversion
        # self.sprelease  = sprelease
        # self.splevel    = splevel
        # self.spsublevel = spsublevel
        # self.spprompt   = spprompt

        # print(' and loading rules: ')        
        self.loadrules()

    def prompt(self):
        if globals.config.getconfiguration().has_section(globals.server) and globals.config.getconfiguration()[globals.server].get( 'prompt' ) != None:
            prompt = globals.config.getconfiguration()[globals.server]['prompt'].strip( '"' )
        else:
            prompt = globals.config.getconfiguration()['SPADMIN']['prompt'].strip( '"' )

        # versions
        prompt = prompt.replace('%SPVERSION%', globals.spversion)
        prompt = prompt.replace('%SPRELEASE%', globals.sprelease)
        prompt = prompt.replace('%SPLEVEL%', globals.splevel)
        prompt = prompt.replace('%SPSUBLEVEL%', globals.spsublevel)

        # prompt
        return prompt.replace('%SPSERVERNAME%', globals.spservername)

    def spsqlengine( self, select, tokens = [] ):
        
        # Handle SQL requests

        globals.logger.debug('  SP SQL Engine reached with this select:  [' + select + '] command and')
        globals.logger.debug('  SP SQL Engine reached with these tokens: [' + pformat(tokens) + '].')

        ret = []

        # select preparation
        if search( '\'(-\d)\'', select ):
            # extra index
            globals.logger.debug('  Extra select has found: [' + select + '].')
            for element in findall('\'(-\d)\'', select):
                select = select.replace(str(element), tokens[int(element)])
                globals.logger.debug('  SP SQL Engine select index preparation result: [' + select + '].')

            #index = search( '\'(-\d)\'', select )[ 1 ]
            #select = select.replace( str( index ), tokens[ int( index ) ])
            #globals.logger.debug('  SP SQL Engine select index preparation result: [' + select + '].')

        if search( '{Prefix: (.+)}', select ):
            # extra prefix
            prefix = search( '{Prefix: (.+)}', select )[ 1 ]
            select = select.replace( '{Prefix: ' + prefix + '}', '' )  # remove the logic description
            match = search( '(\w+=)\w*', tokens[ int( prefix ) ] )
            if match:
                select = select.replace( '%PREFIX%', match[ 1 ] )

            globals.logger.debug('  SP SQL Engine select prefix preparation result: [' + select + '].')

        # logging.info( ' CACHE: [' + pformat( cache ) + '].' )

        # if globals.config.getconfiguration()['SPADMIN']['dynamic_readline_toprows']:
        #     select += ' fetch first ' + globals.config.getconfiguration()['SPADMIN']['dynamic_readline_toprows'] + ' rows only'

        # cache engine
        if select in self.cache.keys():
            self.cache_hitratio[ 'hit' ] += 1
            if time() - self.cache_timestamp[ select ] > int(globals.config.getconfiguration()['SPADMIN']['cache_age']):
                # refresh needed
                globals.logger.debug('  SP SQL Engine hit the cache but the stored one is too old!')
                globals.logger.debug('  CACHE timediff in second(s): [' + str(time() - self.cache_timestamp[select]) + '].')
                self.cache[ select ] = globals.tsm.send_command_array_tabdel(select)
                self.cache_timestamp[ select ] = time()
                self.cache_hitratio[ 'hitupdate' ] += 1
        else:
            # new, init
            globals.logger.debug('  SP SQL Engine still no cached data store a new one.')
            self.cache[ select ] = globals.tsm.send_command_array_tabdel(select)
            self.cache_timestamp[ select ] = time()
            self.cache_hitratio[ 'new' ] += 1

        # logging.info( ' CACHE2: [' + pformat( cache ) + '].' )

        sqlresults = self.cache[ select ]
        self.cache_hitratio[ 'request' ] += 1

        # Filter the sqlresults with the last word if possible
        for x in sqlresults:
            if search( '^' + escape( tokens[ -1 ] ), x, IGNORECASE ):
                ret.append( x + ' ' )

        # return ret[ :int( globals.config.getconfiguration()['SPADMIN']['dynamic_readline_toprows'] ) ]
        # This return only needed when truncating the resultset.
        return ret

    start    = []  # 1. level list
    rules    = {}  # >2. level dictionary
    dynrules = {}  # >2. level dynamic dictionary
    
    retfixed = []

    def loadrules( self ):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            os.chdir(sys._MEIPASS)
            rulefilename = 'spadmin.rules'
        else:
            rulefilename = 'lib/spadmin.rules'
        rulefile = open( rulefilename, 'r' )
        rulefilelines = rulefile.readlines()
        #self.start = []  # 1. level list
        #self.rules = {}  # >2. level dictionary
        self.start.clear()
        
        IBMSPrlCompleter.start.append( globals.basecommandname )
        globals.basecommandname += ' '
        
        self.rules.clear()
        i = 0
        for line in rulefilelines:
            i += 1
            utilities.progressbar( i, len(rulefilelines), 'Loading rules: ' )
            # ez mi? assert?
            # assert( '->' in line )
            # Skip the remark and empty lines
            if line.startswith( "#" ) or not line.rstrip():
                continue
            # lower ??? QUIt Query
            # line = line.strip().lower()
            line = line.strip()
            first, second = line.split( '->' )
            first = first.strip()
            second = second.strip()
            if first == '$':
                # Starter
                self.start.append( second )
                # ??? kell ez? bezavar regexp-nél
                # if second not in self.rules:
                #    self.rules[second] = []
            else:
                if first not in self.rules:
                    self.rules[ first ] = []
                if second not in self.rules:
                    self.rules[ second ] = []
                self.rules[ first ].append( second )

        rulefile.close()
        print()

        #utilities.consoleline('#')
        #print(colored(' Imported LEVEL 0 starters', 'green', attrs=['bold']) + ' from this file:\t[' + colored(rulefilename, 'green') + ']')
        # pprint( self.start )
        #print(colored(' Imported LEVEL >1 other rules', 'green', attrs=['bold']) + ' from this file:\t[' + colored(rulefilename, 'green') + ']')
        # pprint( self.rules )
        globals.logger.debug('Rule file imported as starters:\n' + pformat(self.start))
        globals.logger.debug('Rule file imported as other rules:\n' + pformat(self.rules))
        #utilities.consoleline('#')

        # self.results = self.start
        # self.results += [ None ]
        utilities.dictmerger( self.rules, self.dynrules )

        return None

    ###############
    # tokenEngine #
    ###############
    def tokenEngine( self, tokens ):
        globals.logger.debug(' >>> PROCESS TOKENS with token engine, received tokens: ' + pformat(tokens))

        # Reset the results dictionary
        ret           = []
        tokenlength   = len( tokens )
        
        self.retfixed = []

        if tokenlength == 0:
            # Never happens this
            globals.logger.debug(' Stepped into LEVEL 0.')

        elif tokenlength == 1:
            # LEVEL 1 searches in start commands
            globals.logger.debug(' Stepped into LEVEL 1.')

            # Simple check the beginning of the command on start list
            for key in self.start:
                if search('^' + tokens[ -1 ], key, IGNORECASE):
                    globals.logger.debug(str(tokenlength) + ' found this part [' + tokens[ -1] + '] of the command in the 1st LEVEL list items: [' + key + '].')
            
                    # similar commands CASE BUG fix v1.0 part I. test 2 ######################################
            
                    self.retfixed.append( key + ' ' )
            
                    index = len( tokens[ -1 ] )
                    # override the problematic letter
                    # x[index] = tokens[ -1][index]
                    if index > 1:
                        #x = x[:index] + tokens[ -1][index] + x[index+1:]
                        key = tokens[ -1][:index] + key[index:]
                    ##########################################################################################
                    
                    # here it could be improved a bit, if they all start with token[-1], they can be capitalized???
            
                    ret.append( key.lower() + ' ' )

        elif tokenlength >= 2:
            # LEVEL x.
            globals.logger.debug(' Stepped into LEVEL ' + str( tokenlength ) + '.')
            
            if '=' in tokens[-1]:
                tokenlength += 1
                globals.logger.debug(' Stepped into LEVEL overridden to: ' + str( tokenlength ) + '.')

            # reduce rules to tmprules
            tmprules    = {}
            tmprulesmax = 0
            for key in self.rules:
                
                if key.startswith( 'select' ):  # ???????????????????????????????
                    continue
                
                # if search( '^' + ' '.join( tokens[0:( tokenlength - 1 )] ).rstrip(), key, IGNORECASE ):
                # Filter onnly the first two levels!
                # ???????????????? ez lehet már nem is kell
                lenmax2 = ( tokenlength - 1 )
                if lenmax2 > 2:
                    lenmax2 = 2

                # cleanup the rules to reduce its size RUN is an exception we MUST handle!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                if search( '^' + '.* '.join( tokens[0:lenmax2] ).rstrip(), key, IGNORECASE ) or search( '^' + tokens[0], 'run', IGNORECASE ):
                    # print('['+ key + ']')
                    
                    keylength = len( key.split() )                 
                             
                    # if tokenlength > 3 and keylength <= 2:
                    #     continue

                    if keylength != ( tokenlength - 1 ) and not search( '\{1\,\}', key ):
                        continue



                    # if keylength < tokenlength - 1:
                    #     continue                     

                    tmprules[key] = self.rules[key]

                    if keylength > tmprulesmax:
                        tmprulesmax = keylength
 
            globals.logger.debug( '--- tokenlen: ' + str( tokenlength ) + ' and tokens:        ' + pformat( tokens, width=180 ) )
            globals.logger.debug( '--- rulesmax: ' + str( tmprulesmax ) + ' and reduced rules: ' + pformat( tmprules, width=180 ) )

#             # keep only repeatable options if 
#             tmprules2 = []
# 
#             if tokenlength > tmprulesmax:
#                 for key in tmprules:
#                     if search( '\{1\,\}', key ):
#                         tmprules2[key] = tmprules[key]
#                         
#                 tmprules = tmprules2                        
                
            # collect the results
            for key in tmprules:
                
                globals.logger.debug( str( tokenlength ) + ' and searching for regexp pattern [' + key + ']' )
                globals.logger.debug( str( tokenlength ) + ' and searching for regexp pattern [' + '^' + utilities.regexpgenerator( key ) + ']' )
                
                extradelimiter = '' if search( '=', key ) else ' ' 
                if search( '^' + utilities.regexpgenerator( key ) + extradelimiter, ' '.join( tokens ) + extradelimiter, IGNORECASE ):
                    # globals.logger.debug( str( tokenlength ) + ' Found this part [' + tokens   + '] of the command in the 2nd LEVEL dictionary items: [' + key + '].' )
                    globals.logger.debug( str( tokenlength ) + " Let's continue searching with this pattern [" + pformat( tmprules[key], width=180 ) + ']' )
                   
                    ret += self.SPunversaltokenresolver( key, tokens )

            # in level 2 fix to show colors
            if tokenlength == 2:
                self.retfixed = ret
                ret = [x.lower() for x in ret]
            
        else:
            globals.logger.debug(' Stepped into LEVEL Bzzz...')

        #globals.logger.debug( " Here's what we have in ret: [" + pformat( ret, width=180 ) + ']')
        globals.logger.debug(' <<< PROCESS token engine RETURNED.')

        return ret

    # v2 optimization
    rrr = []

    def IBMSPcompleter( self, text, state ):

        globals.logger.debug(utilities.consolefilledline('>>> Step into IBMSPcompleter v2 with this text: ', '-', '[' + text + '] and with this state[' + str(state) + '].'))

        if len( self.rrr ) == 0:
            globals.logger.debug(' The readline buffer has the following: [' + readline.get_line_buffer() + '].')

            # Read CLI and split commands
            # first ;
            # tokens = readline.get_line_buffer().split()
            tokens = readline.get_line_buffer().split(';')[-1].split('|')[-1].split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append('')
            
            # Call the Engine
            self.rrr = self.tokenEngine(tokens) + [None]

            globals.logger.debug(' RETURNED results from the token engine:')
            globals.logger.debug(pformat(self.rrr, width=180))

            tmp = self.rrr.pop( 0 )
            #logging.info(': ' + pformat(self.rrr, width=180))

            if tmp == None:
                globals.logger.debug(utilities.consolefilledline('<<< COMPLETER RESULT PUSH CYCLES ENDED!!!'))
            else:
                globals.logger.debug(utilities.consolefilledline('<<< COMPLETER results push cycle:  [' + tmp + ']', '-', '[' + str(state) + '].'))
            
            return tmp

        else:
            tmp = self.rrr.pop( 0 )
            if tmp == None:
                globals.logger.debug(utilities.consolefilledline('<<< COMPLETER RESULT PUSH CYCLES ENDED2!!!'))
                self.rrr = []
            else:
                globals.logger.debug(utilities.consolefilledline('<<< COMPLETER results push cycle2: [' + tmp + ']', '-', '[' + str(state) + '].'))
            
            return tmp
            
            
    def SPunversaltokenresolver( self, key = '', tokens = [] ):
        
        ret = []
                
        for x in self.rules[ key ]:
        
            # {Mustexist: .+} feature test
            if search( '{Mustexist: .+}', x, IGNORECASE ):
                mustexist = search( '{Mustexist: (.+)}', x )
                
                left, right = mustexist[ 1 ].split( '=' ) 
                leftregexp  = utilities.regexpgenerator( left )
                rightregexp = utilities.regexpgenerator( right )
                
                if not search( ' ' +  leftregexp + '=' + rightregexp, ' '.join( tokens ), IGNORECASE ):
                    continue
                else:                        
                    # it's Ok, we found it, then remove it not to disturb furthermore
                    x = x.replace( mustexist[ 0 ], '' )
                                                                                 
            if x.startswith( 'select' ):
                # First try as an SQL pattern!
                #globals.logger.debug( str( tokenlength) + " it's an SQL select [" + tokens[ -1 ] + ' > ' + x + ']' )
                ret += self.spsqlengine( x.strip(), tokens )
                continue
            else:
                #if explicit option is given, then preparation may needed
                if tokens[ -1 ] != '' and tokens[ -1 ][ -1 ] == '=':
                    match = search( '(\w+=)\w+', x )
                    if match:
                        x = x.replace( match[ 1 ], tokens[ -1 ] )
                                
                if search( '^' + tokens[ -1 ], x, IGNORECASE ):
                    #globals.logger.debug( str( tokenlength) + ' as a regexp starts with [' + tokens[ -1 ] + ' > ' + x + ']' )
                    separator = '' if x[ -1 ] == '=' else ' '
                    
                    ret.append( x + separator )
                    continue
                                  
                if search( r'\w+=\w+', x ):
                    left, right = x.split( '=' ) 
                    leftregexp  = utilities.regexpgenerator( left )
                    rightregexp = utilities.regexpgenerator( right )
                    match = search( '^' + leftregexp + '=' + rightregexp, tokens[ -1 ], IGNORECASE )
                    if match:
                         ret.append( match[ 1 ] + '=' + right )
                         continue

        return ret

    ######################
    # match_display_hook #
    ######################
    def match_display_hook( self, substitution, matches, longest_match_length ):

        #globals.logger.debug( '>>> Step into: match_display_hook with this:' )
        #globals.logger.debug( 'substitution: ' + str( substitution ) )
        #globals.logger.debug( 'matches: ' + str( matches ) )
        #globals.logger.debug( 'longest_match_length: ' + str( longest_match_length ) )

        word       = 1
        maxlength  = 0
        tmpmatches = []
        
        # similar commands CASE BUG fix v1.0 part II. test 2 ######################################
        #print( pformat( self.retfixed ) )
        if self.retfixed != []:
            matches = self.retfixed

        sys.stdout.write( '\n' )
        for match in sorted( matches, key = lambda s: s.casefold() ):

            # cleanup for PARAMETER= values
            if search( '^\w+=(\w+)', match ):
                ppp = search( '^\w+=(\w+)', match )[ 1 ]
            else:
                ppp = match
            
            length = len( ppp )
            if length > maxlength:
                maxlength = length
                            
            tmpmatches.append( ppp )

        maxlength += 3
        separation = ( globals.columns // maxlength ) - 1
        
        for ppp in tmpmatches:
            
            ppp = ppp.ljust( maxlength )
            
            # colorize the result
            match = search( '^[A-Z][A-Z0-9]*', ppp )
            if match:
                ppp = ppp.replace( match[ 0 ], colored( match[ 0 ], globals.color_green, attrs=[ globals.color_attrs_bold ] ) )
                        
            sys.stdout.write( ppp )

            # line separation
            #if word > int( globals.config.getconfiguration()[ 'SPADMIN' ][ 'rlwordseparation' ] ):
            if word > separation:
                word = 0
                sys.stdout.write( '\n' )
            word += 1

        sys.stdout.flush()

        sys.stdout.write( '\n' + self.prompt().replace( "\001", '').replace( "\002", '' ) + '' + readline.get_line_buffer() )
        sys.stdout.flush()

        #globals.logger.debug( '<<< Leave: match_display_hook.' )