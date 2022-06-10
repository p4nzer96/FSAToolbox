import fsatoolbox
from fsatoolbox import *

def conccomp(args, fsalst, path):
    if('-h' in args):
        print("This functions computes the concurrent composition between two FSAs")
        print("Usage:\n     cc outputname input1 input2 (Ex: cc G2 G0 G1")
        print("Optional arguments:")
        print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<3):
        print("Not enough arguments provided, type \"cc -h\" to help")
        return

    if(args[0] in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    if(args[1] not in fsalst or args[2] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:   
        fsalst[args[0]]=cc(fsalst[args[1]],fsalst[args[2]], verbose=('-v' in args))
    except Exception as e:
        print("There was an error while computing the concurrent composition:")
        print(e)
