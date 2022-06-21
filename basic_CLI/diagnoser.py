import fsatoolbox
from fsatoolbox import *
from termcolor import colored


def diagnoser(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ndiag: ", "yellow", attrs=["bold"]) + "This function computes the diagnoser of a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tdiag outputname inputname")
        print(colored("\nOptional arguments:", attrs=["bold"]) + "\n\t-v verbose output, this will print the steps of "
                                                                 "the algorithm")
        print("\nExample:" + "\n\tdiag G1 G0")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"diag -h\" to help", "yellow"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    try:
        fsalst[args[0]] = diag(fsalst[args[1]], verbose=('-v' in args))
    except Exception as e:
        print(colored("There was an error while computing the diagnoser:", "red"))
        print(e)
