import fsatoolbox
from fsatoolbox import *


def supervisor(args, eventslst, fsalst, path):
    if '-h' in args:
        print("This functions computes the supervisor of an automaton G, given the specification automaton H")
        print("Usage:\n     supervisor outputname automaton_name specif_automaton_name (Ex: supervisor G1 G H) ")
        print("Optional arguments:")
        print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 3:
        print("Not enough arguments provided, type \"supervisor -h\" to help")
        return

    if args[0] in fsalst:
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if inp == 'N' or inp == 'n' or inp == '':
            return

    if args[1] not in fsalst or args[2] not in fsalst:
        print("Error, fsa doesn't exists")
        return

    try:
        fsalst[args[0]] = compute_supervisor(fsalst[args[1]], fsalst[args[2]])
    except Exception as e:
        print("There was an error while computing the supervisor:")
        print(e)
