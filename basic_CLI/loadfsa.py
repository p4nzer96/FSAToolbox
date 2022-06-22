import os
import ntpath
from termcolor import colored
from basic_CLI.checkevents import checkevents
import fsatoolbox
from fsatoolbox import *
import colorama

colorama.init()


def loadfsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nload:", "yellow", attrs=["bold"]) + " This functions loads a fsa from a file")
        print(colored("\nUsage:\n\t", attrs=["bold"]) + "load fsa_name path_to_file")
        print(colored("\nExample:\n\t", attrs=["bold"]) + "load C:\\\\Automi\\\\Examples\\\\G0.fsa")
        print(colored("\nNotes: ", attrs=["bold"]) + "\n\t * In windows use \\\\ instead of \\ (ex. C:\\\\Automi) or "
                                                     "put the path in brackets (ex. \"C:\\Automi\\\")")
        print("\t * This function will load .fsa and .txt files")
        print("")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"load -h\" to help", "red"))
        return

    if len(args) == 1:  # single argument mode
        name = ntpath.split(args[0])[1]
        name = name.split('.')[0]
        filepath = args[0]
    elif len(args) == 2:  # two arguments mode
        name = args[0]
        filepath = args[1]
    else:
        print(colored("Invalid number of arguments provided, type \"load -h\" to help", "yellow"))
        return

    if name in fsalst:
        inp = input(colored("Warning, fsa already exists, do you want to overwrite it? [y/N]: ", "yellow"))
        if inp.lower() == 'n' or inp == '':
            return

    if not os.path.isabs(filepath):
        filename = os.path.join(path, filepath)

    if os.path.isfile(filename):
        G = fsa.from_file(filename)

    else:
        if filename[-4:] == ".fsa" or filename[-4:] == ".txt":
            print(colored("Error: file does not exists", "red"))
        else:
            print(colored("Error: file does not exists (did you forget the extension?)", "red"))
        return

    checkevents(G, eventslst, fsalst)

    fsalst[name] = G
