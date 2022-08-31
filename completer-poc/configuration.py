import configparser


class Configuration:
    configparser = None
    defaults = {
        'cache_age': 60,  # cache entry age (seconds)
        'cache_disable': False,  # disable the dynamic SQL queries for readline
        'cache_prefetch': True,  # prefetch cache data when the program starts
        'rulefile': 'spadmin.rules',  # rule file name
        'historyfile': '',  # history file name
        'dsmadmc_path': 'dsmadmc',  # the patch of dsmadmc
        'dsmadmc_id': 'admin',  # username for dsmadmc
        'dsmadmc_password': 'admin',  # password for dsmadmc
        'DSM_DIR': '',
        'DSM_OPT': '',
        'DSM_LOG': '',
        'logfile': 'spadmin.log',  # SPadmin main logfile
        'debug': False,  # enable debug info to the main logfile
        'autoexec'	: '',              # auto command execution when spadmin starts
        'dynamic_readline' : True,            # dynamic SQL queries when TAB + TAB
#        'prompt'           : '[' + colored( '%SPSERVERNAME%', 'white', attrs=[ 'bold' ] ) + '] ' + colored( '>', 'red', attrs=[ 'bold' ] ) + ' ',
        'rlwordseparation' : 8
    }
    def __init__(self, configfile):
        if not configfile:
            configfile = 'ispadmin.ini'
        self.configparser = configparser.ConfigParser()
        self.configparser.read(configfile)

    def writeconfig(self):
        with open('spadmin.ini', 'w') as configfile:
            self.configparser.write(configfile)

    def getconfiguration(self):
        if not self.configparser.has_section('DEFAULT'):
            self.configparser.sections().append('DEFAULT')
        for key in self.defaults:
            if not self.configparser.has_option("DEFAULT", key):
                self.configparser["DEFAULT"][key] = str(self.defaults[key])

        return self.configparser

if __name__ == "__main__":
    c = Configuration("spadmin.ini")
    print ("Print: ", c.getconfiguration()['DEFAULT'])
    print ("Print: ", c.getconfiguration()['DEFAULT']['cache_age'])
    c.writeconfig()