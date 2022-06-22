import fsatoolbox
from fsatoolbox import *
from termcolor import colored
import colorama

from fsatoolbox.trim import trim

colorama.init()


def trimfsa(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ntrimfsa: ", "yellow", attrs=["bold"]) + "This functions computes a trim of a FSA ")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\ttrimfsa output input")
        print(colored("\nExample:", attrs=["bold"]) + "\n\ttrimfsa G2 G1")
        print("")
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
        fsalst[args[0]] = trim(fsalst[args[1]])
    except Exception as e:
        print(colored("There was an error while computing the extended supervisor:", "red"))
        print(e)
