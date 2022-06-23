import fsatoolbox
from fsatoolbox import *
from termcolor import colored
import colorama
from basic_CLI.exceptions import ArgsException

colorama.init()


def diag_CLI(args, opts, fsalst, **kwargs):
    
    printOnly = '-printOnly' in opts

    if printOnly:
        args_n=1
    else:
        args_n=2

    if len(args) < args_n: raise ArgsException()

    if not printOnly and args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    try:
        result = diag(fsalst[args[args_n-1]], verbose=('-v' in args))
        if printOnly:
            print(result)
        else:
            fsalst[args[0]]=result
    except Exception as e:
        print(colored("There was an error while computing the diagnoser:", "red"))
        print(e)
        return