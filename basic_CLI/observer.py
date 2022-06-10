import fsatoolbox
from fsatoolbox import *

def observer(args, fsalst, path):
    if('-h' in args):
        print("This functions computes the equivalent DFA of the given NFA")
        print("Usage:\n     nfa2dfa outputname inputname")
        print("Alternative:\n     obs outputname inputname")

    if(args[0] in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    try:
        fsalst[args[0]]=nfa2dfa(fsalst[args[1]])
    except Exception as e:
        print("There was an error while computing the fault monitor:")
        print(e)

