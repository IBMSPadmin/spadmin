import sys
import utilities
import globals
import logging

from termcolor import colored
from pprint import pprint, pformat
from re import search, IGNORECASE
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
    rows = None
    columns = None
    logging = None
    config = None
    tsm = None
    spversion = None
    sprelease = None
    splevel = None
    spsublevel = None
    spprompt = None

    # cache store
    cache           = {} # global cache data store
    cache_timestamp = {} # global cache timestamp store
    cache_hitratio  = { 'new' : 0, 'request' : 0, 'hit' : 0, 'hitupdate' : 0 }

    def __init__(self, tsm):
        
        sys.stdout.write(" Let's try to get the name of the server...")
        sys.stdout.flush()
        spprompt = tsm.send_command_array_tabdel('select SERVER_NAME from STATUS')[0]
        sys.stdout.write( '\r' )
        
        sys.stdout.write(" and get the version of the IBM SP server...")
        sys.stdout.flush()
        spversion, sprelease, splevel, spsublevel = tsm.send_command_array_array_tabdel('select VERSION, RELEASE, LEVEL, SUBLEVEL from STATUS')[0]
        sys.stdout.write( '\r' )

        self.rows       = globals.rows
        self.columns    = globals.columns
        self.config     = globals.config
        self.tsm        = tsm
        self.spversion  = spversion
        self.sprelease  = sprelease
        self.splevel    = splevel
        self.spsublevel = spsublevel
        self.spprompt   = spprompt

        print(' and loading rules...                                          ')        
        self.loadrules(self.config.getconfiguration()['DEFAULT']['rulefile'])

    def prompt(self):
        prompt = self.config.getconfiguration()['DEFAULT']['prompt'].strip( '"' )

        # versions
        prompt = prompt.replace('%SPVERSION%', self.spversion)
        prompt = prompt.replace('%SPRELEASE%', self.sprelease)
        prompt = prompt.replace('%SPLEVEL%', self.splevel)
        prompt = prompt.replace('%SPSUBLEVEL%', self.spsublevel)

        # prompt
        return prompt.replace('%SPSERVERNAME%', self.spprompt)

    def spsqlengine(self, select, tokens=[]):
        # Handle SQL requests

        logging.info(' SP SQL Engine reached with this select: [' + select + '] command and')
        logging.info(' SP SQL Engine reached with these tokens: [' + pformat(tokens) + '].')

        ret = []

        # select preparation
        if search('\'(-\d)\'', select):
            # extra index
            index = search('\'(-\d)\'', select)[1]
            select = select.replace(str(index), tokens[int(index)])
            logging.info(' SP SQL Engine select index preparation result: [' + select + '].')

        if search('\{Prefix:\s+(\w+=)}', select):
            # extra prefix
            prefix = search('\{Prefix: (\w+=)}', select)[1]
            select = select.replace('{Prefix: ' + prefix + '}', '')  # remove the logic description
            select = select.replace('%PREFIX%', prefix)

            logging.info(' SP SQL Engine select prefix preparation result: [' + select + '].')

        # logging.info( ' CACHE: [' + pformat( cache ) + '].' )

        # cache engine
        if select in self.cache.keys():
            self.cache_hitratio['hit'] += 1
            if time() - self.cache_timestamp[select] > int(self.config.getconfiguration()['DEFAULT']['cache_age']):
                # refresh needed
                logging.info(' SP SQL Engine hit the cache but the stored one is too old.')
                logging.info(' CACHE TIMEDIFF in second(s): [' + str(time() - self.cache_timestamp[select]) + '].')
                self.cache[select] = self.tsm.send_command_array_tabdel(select)
                self.cache_timestamp[select] = time()
                self.cache_hitratio['hitupdate'] += 1
        else:
            # new, init
            logging.info(" SP SQL Engine still no cached data store a new one.")
            self.cache[select] = self.tsm.send_command_array_tabdel(select)
            self.cache_timestamp[select] = time()
            self.cache_hitratio['new'] += 1

        # logging.info( ' CACHE2: [' + pformat( cache ) + '].' )

        sqlresults = self.cache[select]
        self.cache_hitratio['request'] += 1

        # Filter the sqlresults with the last word if possible
        for x in sqlresults:
            if search('^' + tokens[-1], x, IGNORECASE):
                ret.append(x + ' ')

        return ret

    start    = []  # 1. level list
    rules    = {}  # >2. level dictionary
    dynrules = {}  # >2. level dynamic dictionary

    def loadrules(self, rulefilename):
        rulefile = open(rulefilename, 'r')
        rulefilelines = rulefile.readlines()
        #self.start = []  # 1. level list
        #self.rules = {}  # >2. level dictionary
        i = 0
        for line in rulefilelines:
            i += 1
            utilities.progressbar(i, len(rulefilelines))
            # ez mi? assert?
            # assert( '->' in line )
            # Skip the remark and empty lines
            if line.startswith("#") or not line.rstrip():
                continue
            # lower ??? QUIt Query
            # line = line.strip().lower()
            line = line.strip()
            first, second = line.split('->')
            first = first.strip()
            second = second.strip()
            if first == '$':
                # Starter
                self.start.append(second)
                # ??? kell ez? bezavar regexp-nél
                # if second not in self.rules:
                #    self.rules[second] = []
            else:
                if first not in self.rules:
                    self.rules[first] = []
                if second not in self.rules:
                    self.rules[second] = []
                self.rules[first].append(second)

        rulefile.close()
        print()

        #utilities.consoleline('#')
        #print(colored(' Imported LEVEL 0 starters', 'green', attrs=['bold']) + ' from this file:\t[' + colored(rulefilename, 'green') + ']')
        # pprint( self.start )
        #print(colored(' Imported LEVEL >1 other rules', 'green', attrs=['bold']) + ' from this file:\t[' + colored(rulefilename, 'green') + ']')
        # pprint( self.rules )
        logging.info('Rule file imported as starters:\n' + pformat(self.start))
        logging.info('Rule file imported as other rules:\n' + pformat(self.rules))
        #utilities.consoleline('#')

        # self.results = self.start
        # self.results += [ None ]
        utilities.dictmerger( self.rules, self.dynrules )

        return None

    ###############
    # tokenEngine #
    ###############
    def tokenEngine(self, tokens):
        logging.info(' PROCESS TOKENS, received tokens: ' + pformat(tokens))

        # Reset the results dictionary
        ret = []

        if len(tokens) == 0:
            # Never happen this
            logging.info('Stepped into LEVEL 0.')

        elif len(tokens) == 1:
            # LEVEL 1 searches in start commands
            logging.info(' Stepped into LEVEL 1.')

            # Simple check the beginning of the command on start list
            for x in self.start:
                if search('^' + tokens[-1], x, IGNORECASE):
                    logging.info(' found this part [' + tokens[
                        -1] + '] of the command in the 1st LEVEL list items: [' + x + '].')
                    ret.append(x + ' ')

        elif len(tokens) == 2:
            # LEVEL 2
            logging.info(' Stepped into LEVEL 2.')

            for key in self.rules:
                # skip the previous level entries
                if len(key.split()) + 1 < 2:
                    continue
                # logging.info( ' and searching for regexp pattern [' + key + ']' )
                # logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + '(?!.*\w)' + ']' )
                if search('^' + utilities.regexpgenerator(key), tokens[-2], IGNORECASE):
                    logging.info(' Found this part [' + tokens[
                        -2] + '] of the command in the 2nd LEVEL dictionary items: [' + key + '].')

                    logging.info(
                        ' Let\'s continue searching with this pattern [' + pformat(self.rules[key], width=180) + ']')
                    for x in self.rules[key]:
                        if search('^' + tokens[-1], x, IGNORECASE):
                            logging.info(' as (regexp) starts with [' + tokens[-1] + ' > ' + x + ']')
                            ret.append(x + ' ')
                            continue

        elif len(tokens) == 3:
            # LEVEL 3
            logging.info(' Stepped into LEVEL 3.')

            for key in self.rules:
                # skip the previous level entries
                if len(key.split()) + 1 < 3:
                    continue
                elif key.startswith('select'):  # ???????????????????????????????
                    continue
                # logging.info( ' and searching for regexp pattern [' + key + ']' )
                # logging.info( ' and searching for regexp pattern [' + '^' + regexpgenerator( key ) + ']' )
                # logging.info( ' and searching in text [' + tokens[ -3 ] + ' ' + tokens[ -2 ] + ']' )
                if search('^' + utilities.regexpgenerator(key), tokens[-3] + ' ' + tokens[-2] + ' ' + tokens[-1], IGNORECASE):
                    logging.info(' and found [' + tokens[-3] + ' ' + tokens[
                        -2] + '] command in the 3rd LEVEL dictionary item: [' + key + '].')

                    logging.info(
                        ' let\'s continue searching with this item(s) [' + pformat(self.rules[key], width=180) + ']')
                    for x in self.rules[key]:
                        if x.startswith('select'):
                            # First try as an SQL pattern!
                            logging.info(' it\'s an SQL select [' + tokens[-1] + ' > ' + x + ']')
                            ret += self.spsqlengine(x.strip(), tokens)
                            continue
                        elif search('^' + tokens[-1], x, IGNORECASE):
                            logging.info(' as a regexp starts with [' + tokens[-1] + ' > ' + x + ']')
                            separator = '' if x[-1] == '=' else ' '
                            ret.append(x + separator)
                            continue
        elif len(tokens) == 4:
            # LEVEL 4
            logging.info(' Stepped into LEVEL 4.')

            for key in self.rules:
                # skip the previous level entries
                if len(key.split()) + 1 < 4:
                    continue
                elif key.startswith('select'):  # ???????????????????????????????
                    continue
                if search('^' + utilities.regexpgenerator(key),
                          tokens[-4] + ' ' + tokens[-3] + ' ' + tokens[-2] + ' ' + tokens[-1], IGNORECASE):
                    logging.info(' and found [' + tokens[-4] + ' ' + tokens[-3] + ' ' + tokens[
                        -2] + '] command in the 4th LEVEL dictionary item: [' + key + '].')

                    logging.info(
                        ' let\'s continue searching with this item(s) [' + pformat(self.rules[key], width=180) + ']')
                    for x in self.rules[key]:
                        if x.startswith('select'):
                            # First try as an SQL pattern!
                            logging.info(' it\'s an SQL select [' + tokens[-1] + ' > ' + x + ']')
                            ret += self.spsqlengine(x.strip(), tokens)
                            continue
                        elif search('^' + tokens[-1], x, IGNORECASE):
                            logging.info(' as a regexp starts with [' + tokens[-1] + ' > ' + x + ']')
                            separator = '' if x[-1] == '=' else ' '
                            ret.append(x + separator)
                            continue

        elif len(tokens) == 5:
            # LEVEL 5
            logging.info(' Stepped into LEVEL 5.')

            for key in self.rules:
                # skip the previous level entries
                if len(key.split()) + 1 < 5:
                    continue
                elif key.startswith('select'):  # ???????????????????????????????
                    continue
                if search('^' + utilities.regexpgenerator(key),
                          tokens[-5] + ' ' + tokens[-4] + ' ' + tokens[-3] + ' ' + tokens[-2] + ' ' + tokens[-1],
                          IGNORECASE):
                    logging.info(' and found [' + tokens[-5] + ' ' + tokens[-4] + ' ' + tokens[-3] + ' ' + tokens[
                        -2] + '] command in the 5th LEVEL dictionary item: [' + key + '].')

                    logging.info(
                        ' let\'s continue searching with this item(s) [' + pformat(self.rules[key], width=180) + ']')
                    for x in self.rules[key]:
                        if x.startswith('select'):
                            # First try as an SQL pattern!
                            logging.info(' it\'s an SQL select [' + tokens[-1] + ' > ' + x + ']')
                            ret += self.spsqlengine(x.strip(), tokens)
                            continue
                        elif search('^' + tokens[-1], x, IGNORECASE):
                            logging.info(' as a regexp starts with [' + tokens[-1] + ' > ' + x + ']')
                            separator = '' if x[-1] == '=' else ' '
                            ret.append(x + separator)
                            continue

        else:
            logging.info(' Stepped into LEVEL Bzzz...')

        logging.info(' Here\'s what we have in ret: [' + pformat(ret, width=180) + ']')
        logging.info(' PROCESS RETURNED.')

        return ret

    # v2 optimization
    rrr = []

    def IBMSPcompleter(self, text, state):

        logging.info('')
        logging.info(utilities.consolefilledline('COMPLETER Text: ', '-', '[' + text + '] and state[' + str(state) + '].', 120))

        if len(self.rrr) == 0:
            logging.info('Readline buffer: [' + readline.get_line_buffer() + '].')

            # Read CLI and split commands
            # first ;
            # tokens = readline.get_line_buffer().split()
            tokens = readline.get_line_buffer().split(';')[-1].split('|')[-1].split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens.append('')

            # Call the Engine
            self.rrr = self.tokenEngine(tokens) + [None]

            logging.info('RETURNED results from the engine: ' + pformat(self.rrr, width=180))

            tmp = self.rrr.pop(0)
            logging.info(': ' + pformat(self.rrr, width=180))

            if tmp == None:
                logging.info(
                    'COMPLETER RESULT PUSH CYCLES ENDED! --------------------------------------------------------------------------')
                logging.info('')
            else:
                logging.info(utilities.consolefilledline('COMPLETER results push cycle: [' + tmp + ']', '-',
                                               '[' + str(state) + '] [' + '].', 120))

            return tmp

        else:
                tmp = self.rrr.pop(0)
                if tmp == None:
                    self.rrr = []
                return tmp


    ######################
    # match_display_hook #
    ######################
    def match_display_hook(self, substitution, matches, longest_match_length):

        word = 1

        print()
        for match in matches:

            # cleanup for PARAMETER= values
            if search('^\w+=(\w+)', match):
                ppp = search('^\w+=(\w+)', match)[1]
            else:
                ppp = match
            
            # colorize the result
            match = search( '^[A-Z]+', ppp )
            if match:
                ppp = ppp.replace( match[0], colored( match[0], 'green', attrs=[ 'bold' ] ) )

            sys.stdout.write( ppp + '   ' )

            # line separation
            if word > int(self.config.getconfiguration()['DEFAULT']['rlwordseparation']):
                word = 1
                print()
            word += 1

        sys.stdout.write('\n' + self.prompt() + '' + readline.get_line_buffer())
        # sys.stdout.flush()
