import os.path

import fsatoolbox
from fsatoolbox import *
from termcolor import colored
import colorama

colorama.init()


def savefsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nsave: ", "yellow", attrs=["bold"]) + "Saves a FSA to file")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\tsave fsa_to_save path_to_file")
        print(colored("\nExample:", attrs=["bold"]) + "\n\tsave G0 G0.fsa")
        print(colored("\nNotes: ", attrs=["bold"]) + "\n\t * Only .fsa files currently supported")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"save -h\" to help", "yellow"))
        return

    if args[0] in fsalst:

        if not os.path.isabs(args[1]):
            filename = os.path.join(path, args[1])
        else:
            filename = args[1]

        try:
            fsalst[args[0]].to_file(filename)  # current path
        except Exception as e:
            print(colored("Error while saving the file:", "red"))
            print(e)
    else:
        print(colored("Error, fsa doesn't exists", "red"))
