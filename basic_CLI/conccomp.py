import fsatoolbox
from fsatoolbox import *
from termcolor import colored


def conccomp(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ncc: ", "yellow", attrs=["bold"]) + "This functions computes the concurrent composition "
                                                            "between two FSAs")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tcc outputname input1 input2")
        print(colored("\nOptional arguments:", attrs=["bold"]) +
              "\n\t-v verbose output, this will print the steps of the algorithm")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tcc G2 G0 G1")
        print("")
        return

    if len(args) < 3:
        print(colored("Not enough arguments provided, type \"cc -h\" to help", "yellow"))
        return

    if args[0] in fsalst:
        inp = input(colored("Error, fsa already exists, do you want to overwrite it? [y/N]: ", "red"))
        if inp == 'N' or inp == 'n' or inp == '':
            return

    if args[1] not in fsalst or args[2] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]] = cc(fsalst[args[1]], fsalst[args[2]], verbose=('-v' in args))
    except Exception as e:
        print(colored("There was an error while computing the concurrent composition:", "red"))
        print(e)
