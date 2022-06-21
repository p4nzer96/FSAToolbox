from termcolor import colored

import fsatoolbox
from fsatoolbox import *


def exth(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("exth: ", "yellow", attrs=["bold"]) + "This functions computes the extended specification "
                                                            "automaton, given the specification automaton H")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\texth outputname inputname (Ex: exth H1 H) ")
        print(colored("\nExample:", attrs=["bold"]) + "\n\texth H1 H")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"exth -h\" to help", "yellow"))
        return

    if args[1] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    try:
        fsalst[args[0]] = hhat(fsalst[args[1]])
    except Exception as e:
        print(colored("There was an error while computing the extended supervisor:", "red"))
        print(e)
