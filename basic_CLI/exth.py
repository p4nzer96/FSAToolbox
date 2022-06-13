import fsatoolbox
from fsatoolbox import *

def exth(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes the extended specification automaton, given the specification automaton H")
        print("Usage:\n     exth outputname inputname (Ex: exth H1 H) ")
        #print("Optional arguments:")
        #print("-v verbose output, this will print the steps of the algorithm")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"exth -h\" to help")
        return

    if(args[1] not in fsalst):
        print("Error, fsa doesn't exists")
        return

    if(args[0] in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    try:
        fsalst[args[0]]=hhat(fsalst[args[1]])
    except Exception as e:
        print("There was an error while computing the extended supervisor:")
        print(e)

