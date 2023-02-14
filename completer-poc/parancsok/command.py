import subprocess
import re
import csv
file = open("parancsoksorszama.txt", "r")
data = file.readlines()
file.close()

for l in data:
    get_output = False
    print ("Next: Help for:", l)
    proc = subprocess.Popen(['dsmadmc', '-id=support', '-pa=userkft1q2', 'help', l], stdout=subprocess.PIPE)
    while True:
        line = proc.stdout.readline()
        if not line:
            break
        if re.search('^Syntax', line.rstrip().decode('utf-8')):
            get_output = True
        if re.search('^Parameters', line.rstrip().decode('utf-8')):
            get_output = False
        if get_output:
            print("OUTPUT:", line.rstrip().decode('utf-8'), "-")
