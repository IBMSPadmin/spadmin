import configparser
from termcolor import colored


class Configuration:
    configparser = None
    configfile   = None
    defaults     = {
        'cache_age'        : 60,  # cache entry age (seconds)
        'cache_disable'    : False,  # disable the dynamic SQL queries for readline
        'cache_prefetch'   : True,  # prefetch cache data when the program starts
        'rulefile'         : 'spadmin.rules',  # rule file name
        'historyfile'      : '.spadmin_history',  # history file name
        'dsmadmc_path'     : 'dsmadmc',  # the patch of dsmadmc
        'dsmadmc_id'       : 'admin',  # username for dsmadmc
        'dsmadmc_password' : 'admin',  # password for dsmadmc
        'DSM_DIR'          : '',
        'DSM_OPT'          : '',
        'DSM_LOG'          : '',
        'logfile'          : 'spadmin.log',  # SPadmin main logfile
        'debug'            : False,  # enable debug info to the main logfile
        'autoexec'	       : '',  # auto command execution when spadmin starts
        'dynamic_readline' : True,   # dynamic SQL queries when TAB + TAB
        'prompt'           : '"[' + colored( '%%SPSERVERNAME%%', 'white', attrs=[ 'bold' ] ) + '] ' + colored( '>', 'red', attrs=[ 'bold' ] ) + ' "',
        'rlwordseparation' : 8
    }
    aliases = {
        'shrlr': 'SHow Ruler',
        'shtim': 'SHow TIME',
        'shtgp': 'SHow STGp',
        'shcac': 'SPadmin SHow CAche',
        'ver': 'SPadmin SHow VERsion',
        'rul': 'SPadmin SHow RULes',
        'deb': 'SPadmin SET DEBUG',
    }
    def __init__(self, configfile):
        if not configfile:
            configfile   = 'spadmin.ini'
        self.configfile  = configfile
        self.configparser = configparser.ConfigParser()
        self.configparser.read(configfile)

        # check existence of DEFAULTS
        if not self.configparser.has_section('SPADMIN'):
            self.configparser.add_section('SPADMIN')
        for key in self.defaults:
            if not self.configparser.has_option('SPADMIN', key):
                self.configparser['SPADMIN'][key] = str(self.defaults[key])
        # check default aliases
        if not self.configparser.has_section('ALIAS'):
            self.configparser.add_section('ALIAS')
        for key in self.aliases:
            if not self.configparser.has_option('ALIAS', key):
                self.configparser['ALIAS'][key] = str(self.aliases[key])
        self.writeconfig()

    def writeconfig(self):
        with open(self.configfile, 'w') as configfile:
            self.configparser.write(configfile)

    def getconfiguration(self):
        return self.configparser