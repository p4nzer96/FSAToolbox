import fsatoolbox
from fsatoolbox import *

def faultmon(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes the fault monitor of the given fsa")
        print("Usage:\n     fm outputname inputname")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"fm -h\" to help")
        return

    if(args[0] in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    try:
        fsalst[args[0]]=fm(fsalst[args[1]])
    except Exception as e:
        print("There was an error while computing the concurrent composition:")
        print(e)