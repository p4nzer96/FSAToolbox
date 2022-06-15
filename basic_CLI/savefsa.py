import os.path

import fsatoolbox
from fsatoolbox import *
from termcolor import colored


def savefsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nsave: ", "yellow", attrs=["bold"]) + "Saves a FSA to file\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tsave fsa_to_save path_to_file")
        print(colored("Example:", attrs=["bold"]) + "\n\tsave G0 G0.fsa")
        print(colored("Notes: ", attrs=["bold"]) + "\n\t * Only .fsa files currently supported")

    if len(args) < 2:
        print("Not enough arguments provided, type \"save -h\" to help")
        return

    if args[0] in fsalst:

        if not os.path.isabs(args[1]):
            filename = os.path.join(path, args[1])
        else:
            filename = args[1]
        if args[1][-4:] != ".fsa":
            filename = filename + ".fsa"

        try:
            fsalst[args[0]].to_file(filename)  # current path
        except Exception as e:
            print("Error while saving the file:")
            print(e)
    else:
        print("Error, fsa doesn't exists")
