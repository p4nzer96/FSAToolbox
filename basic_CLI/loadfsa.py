import os
import ntpath
from basic_CLI.checkevents import checkevents
import fsatoolbox
from fsatoolbox import *

def loadfsa(args,eventslst, fsalst, path):
    if('-h' in args):
        print("This functions loads a fsa from a file")
        print("Usage:\n->load name pathToFile or load name nameOfTheFile if the fsa is in the path")
        print("Alternative:\n->load pathtofile (the name will be the same as the file)")
        print("Note: In windows, use \\\\ instead of \\ (C:\\\\Automi\\\\G0.fsa) or put the path in brakets: \"C:\Automi\G0.fsa\"") #TODO
        print("Note2: This function will load .fsa and .txt files")
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
        G=fsa.from_file(filepath)
    elif(os.path.isfile(filepath+'.fsa')):
        G=fsa.from_file(filepath+'.fsa')
    elif(os.path.isfile(filepath+'.txt')):
        G=fsa.from_file(filepath+'.txt')
    elif(os.path.isfile(path+'\\'+filepath)):
        G=fsa.from_file(path+'\\'+filepath)
    elif(os.path.isfile(path+'\\'+filepath+'.fsa')):
        G=fsa.from_file(path+'\\'+filepath+'.fsa')
    elif(os.path.isfile(path+'\\'+filepath+'.txt')):
        G=fsa.from_file(path+'\\'+filepath+'.txt')
    else:
        print("Error: file does not exists")
        return
    
    checkevents(G,eventslst, fsalst)

    fsalst[name]=G