import utilities

def initialize():
    global rows, columns, config, last_error
    global myIBMSPrlCompleter, tsm

    last_error = { 'rc': 0, 'message': "" }
    columns = 80
    rows    = 25
    utilities.refreshrowscolumns()