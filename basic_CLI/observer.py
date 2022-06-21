from termcolor import colored

import fsatoolbox
from fsatoolbox import *


def observer(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nobs: ", "yellow", attrs=["bold"]) + "This functions computes the equivalent DFA of the "
                                                             "given NFA")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tobs outputname inputname")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tobs G0 N0")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"nfa2dfa -h\" to help", "yellow"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    try:
        fsalst[args[0]] = nfa2dfa(fsalst[args[1]])
    except Exception as e:
        print(colored("There was an error while computing the fault monitor:", "red"))
        print(e)
