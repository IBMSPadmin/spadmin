import configparser
from termcolor import colored
from . import setup
import os

class Configuration:
    configparser = None
    configfile = None
    defaults = {
        'cache_age'                : 60,                   # cache entry age (seconds)
        'cache_disable'            : False,                # disable the dynamic SQL queries for readline
        'cache_prefetch'           : True,                 # prefetch cache data when the program starts
        'rulefile'                 : 'lib/spadmin.rules',  # rule file name
        'historyfile'              : '.spadmin_history',   # history file name
        'dsmadmc_path'             : 'dsmadmc',            # the path of dsmadmc
        'dsmadmc_id'               : 'admin',              # username for dsmadmc
        'dsmadmc_password'         : 'admin',              # password for dsmadmc
        'logfile'                  : 'spadmin.log',        # SPadmin main logfile
        'debug'                    : False,                # enable debug info to the main logfile
        'autoexec'                 : '',                   # auto command execution when spadmin starts
        'dynamic_readline'         : True,                 # dynamic SQL queries when TAB + TAB
        'dynamic_readline_toprows' : 25,
        'prompt'                   : '"[' + colored('%%SPSERVERNAME%%', 'white', attrs=['bold']) + '] ' + colored('>', 'red', attrs=['bold']) + ' "',
        'rlwordseparation'         : 8
    }
    aliases = {
        'shrlr' : 'SHow Ruler',
        'shtim' : 'SHow TIME',
        'shtgp' : 'SHow STGp',
        'shcac' : 'SPadmin SHow CAche',
        'ver'   : 'SPadmin SHow VERsion',
        'rul'   : 'SPadmin SHow RULes',
        'deb'   : 'SPadmin SET DEBUG',
        'ses'   : 'SHow SESsions',
        'dsk'   : 'SH stgp | grep DISK'
    }

    def __init__(self, configfile):

        if not configfile:
            os.makedirs(os.path.join(os.path.expanduser('~/.config/spadmin/')), exist_ok=True)
            configfile = os.path.join(os.path.expanduser('~/.config/spadmin/'), 'spadmin.ini')
        self.configfile = configfile
        self.configparser = configparser.ConfigParser()
        self.configparser.optionxform = str
        self.configparser.read(configfile)

        # check existence of DEFAULTS
        if not self.configparser.has_section('SPADMIN'):
            self.configparser.add_section('SPADMIN')
            for key in self.defaults:
                if not self.configparser.has_option('SPADMIN', key):
                    self.configparser['SPADMIN'][key] = str(self.defaults[key])

            parameters = setup.Setup().get_parameters()
            for key in parameters:
                self.configparser['SPADMIN'][key] = str(parameters[key])

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
