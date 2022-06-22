from termcolor import colored

import fsatoolbox
from fsatoolbox import *
import colorama

colorama.init()


def supervisor(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nsupervisor: ", "yellow", attrs=["bold"]) + "This functions computes the supervisor of an "
                                                                    "automaton G, given the specification automaton H")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tsupervisor outputname automaton_name specif_automaton_name")
        print(colored("\nOptional arguments:", attrs=["bold"]) + "\n\t-v verbose output, this will print the steps of "
                                                                 "the algorithm")
        print(colored("\nExample:" + "\n\tsupervisor G0 H"))
        print("")
        return

    if len(args) < 3:
        print(colored("Not enough arguments provided, type \"supervisor -h\" to help", "yellow"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    if args[1] not in fsalst or args[2] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        fsalst[args[0]] = compute_supervisor(fsalst[args[1]], fsalst[args[2]])
    except Exception as e:
        print(colored("There was an error while computing the supervisor:", "red"))
        print(e)
