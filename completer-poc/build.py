from cx_Freeze import sys, Executable, setup
from lib import dsmadmc_pexpect
from lib.configuration import Configuration
from lib.IBMSPrlCompleter import IBMSPrlCompleter
import lib.utilities as utilities
import lib.columnar
import lib.globals as globals


import datetime
import os
import platform
import logging
import atexit
import argparse

from time import time
from termcolor import colored
from pprint import pformat
from re import search, IGNORECASE

buildOptions = dict(include_files = ['lib/', 'commands/']) #folder,relative path. Use tuple like in the single file to set a absolute path.

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("spadmin.py", base=base)]

setup(
    name="spadmin",
    version="0.1",
    author="Gyorgy Fleischmann, Marcell Szabo",
    options=dict(build_exe=buildOptions),
    description="SPADMIN - toolset for IBM Spectrum Protect ",
    executables=executables,
)
