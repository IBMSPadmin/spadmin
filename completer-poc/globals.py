import utilities

def initialize():
    global rows, columns, config, last_error

    last_error = { 'rc': 0, 'message': "" }
    columns = 80
    rows    = 25
    utilities.refreshrowscolumns()


def set_last_error(rc, message):
    print("RC: ", rc)
    print("Message: ", message)
