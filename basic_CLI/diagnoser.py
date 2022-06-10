import fsatoolbox
from fsatoolbox import *

def diagnoser(args, fsalst, path):
    if('-h' in args):
        print("This function computes the diagnoser of a fsa")
        print("Usage\n->diag outputname inputname (Ex: diag G1 G0")
        print("Optional arguments:")
        print("-v verbose output, this will print the steps of the algorithm")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"diag -h\" to help")
        return
    
    if(args[0] in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    try:
        fsalst[args[0]]=diag(fsalst[args[1]], verbose=('-v' in args))
    except Exception as e:
        print("There was an error while computing the diagnoser:")
        print(e)