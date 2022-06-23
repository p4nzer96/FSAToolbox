from ast import arg
import os
import ntpath
from termcolor import colored
import fsatoolbox
from fsatoolbox import *
import colorama

from basic_CLI.exceptions import ArgsException

colorama.init()


def load_CLI(args,fsalst,path,**kwargs):
    
    if len (args) < 1:
        raise ArgsException()

    if len(args) == 1:  # single argument mode
        name = ntpath.split(args[0])[1]
        name = name.split('.')[0]
        filepath = args[0]
    else:  # two arguments mode
        name = args[0]
        filepath = args[0]

    if name in fsalst:
        inp = input(colored("Warning, fsa already exists, do you want to overwrite it? [y/N]: ", "yellow"))
        if inp.lower() == 'n' or inp == '':
            return

    if not os.path.isabs(filepath):
        filename = os.path.join(path.data, filepath)

    if os.path.isfile(filename):
        G = fsa.from_file(filename)

    else:
        if filename[-4:] == ".fsa" or filename[-4:] == ".txt":
            print(colored("Error: file does not exists", "red"))
        else:
            print(colored("Error: file does not exists (did you forget the extension?)", "red"))
        return

    fsalst[name] = G
