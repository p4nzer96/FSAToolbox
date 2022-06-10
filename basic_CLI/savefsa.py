import fsatoolbox
from fsatoolbox import *

def savefsa(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions saves a fsa to a file")
        print("Usage:\n     load name nameOfTheFile (without the extension)")
        print("Optional arguments:\n -a Use absolute path")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"save -h\" to help")
        return
    
    if(args[0] in fsalst):
        try:
            #check if path is valid?
            if("-a" in args):
                fsalst[args[0]].to_file(args[1]+".fsa")
            else:
                fsalst[args[0]].to_file(path+args[1]+".fsa") #current path
        except Exception as e:
            print("Error while saving the file:")
            print(e)
    else:
        print("Error, fsa doesn't exists")