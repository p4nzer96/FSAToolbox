import os
import ntpath
import fsatoolbox
from fsatoolbox import *

def loadfsa(args, fsalst, path):
    if('-h' in args):
        print("This functions loads a fsa from a file")
        print("Usage:\n->load name pathtofile")
        print("Alternative:\n->load pathtofile (the name will be the same as the file)")
        print("PS: In windows, use \\\\ instead of a single \\ in the paths") #TODO
        return

    if(len(args)<1):
        print("Not enough arguments provided, type \"load -h\" to help")
        return

    if(len(args)==1): #single argument mode
        name=ntpath.split(args[0])[1]
        name=name.split('.')[0]
        filepath=args[0]
    if(len(args)==2): #two arguments mode
        name=args[0]
        filepath=args[1]
    
    if(name in fsalst):
        inp = input("Error, fsa already exists, do you want to overwrite it? [y/N]: ")
        if(inp=='N' or inp=='n' or inp==''):
            return

    if(os.path.isfile(filepath)):
        fsalst[name]=fsa.from_file(filepath)
    elif(os.path.isfile(filepath+'.fsa')):
        fsalst[name]=fsa.from_file(filepath+'.fsa')
    elif(os.path.isfile(path+filepath)):
        fsalst[name]=fsa.from_file(path+filepath)
    elif(os.path.isfile(path+filepath+'.fsa')):
        fsalst[name]=fsa.from_file(path+filepath+'.fsa')
    else:
        print("Error: file does not exists")
        return