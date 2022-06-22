from termcolor import colored

import fsatoolbox
from fsatoolbox import *
import colorama

colorama.init()


def faultmon(args, eventslst, fsalst, path):
    if '-h' in args:
        print(
            colored("\nfm: ", "yellow", attrs=["bold"]) + "This functions computes the fault monitor of the given fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tfm outputname inputname")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tfm F G0")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"fm -h\" to help", "yellow"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    try:
        fsalst[args[0]] = fm(fsalst[args[1]])
    except Exception as e:
        print(colored("There was an error while computing the concurrent composition:", "red"))
        print(e)
