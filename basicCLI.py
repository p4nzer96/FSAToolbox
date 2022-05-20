import os.path

from fsatoolbox import *

def help(args=None):
    print("This is only a test version: available commands:")
    for key,val in commands.items():
        print("->"+key)
    print("[CTRL+C to exit]")

def loadfsa(args):
    if(len(args)>1):
        if(args[1]=='help'):
                print("This functions loads a fsa from a file")
                print("Usage:\n     load name pathtofile")
        elif(len(args)>2):
            if(args[1] in fsalst):
                print("Name already in use")
                return
            else:
                if(os.path.isfile(args[2])):
                    fsalst[args[1]]=fsa.from_file(args[2])
                elif(os.path.isfile(args[2]+'.fsa')):
                    fsalst[args[1]]=fsa.from_file(args[2]+'.fsa')
                else:
                    print("Error: file does not exists")
                    return
        else:
            print("Not enough arguments provided, type \"load help\" to help")
    else:
        print("Not enough arguments provided, type \"load help\" to help")

def buildfsa(args):
    if(len(args)>1):
        if(args[1]=='help'):
                print("This functions loads a fsa from a file")
                print("Usage:\n     build name")
        else:
            if(args[1] in fsalst):
                print("Name already in use")
                return
            else:
                fsalst[args[1]]=fsabuilder()

    else:
        print("Not enough arguments provided, type \"buildfsa help\" to help")

def showfsa(args):
    if(len(args)>1):
        if(args[1]=='help'):
            print("This functions show a fsa")
            print("Usage:\n     show name")
        else:
            if(args[1] in fsalst):
                print(fsalst[args[1]])
            else:
                print("Error, fsa doesn't exists")
    else:
        print("Not enough arguments provided, type \"show help\" to help")

def listfsa(args): #TODO add some stats?
    for key,value in fsalst.items():
        print(key)

def concComp(args):
    if(len(args)>1):
        if(args[1]=='help'):
            print("This functions computes the concurrent composition between two fsa")
            print("Usage:\n     cc outputname input1 input2")
        elif(len(args)>3):
            if(not args[1] in fsalst):
                if(args[2] in fsalst and args[3] in fsalst):
                    fsalst[args[1]]=cc(fsalst[args[2]],fsalst[args[3]])
                else:
                    print("Error, fsa doesn't exists")
            else:
                print("Error, output name already exists") #TODO ask to overwrite?
        else:
            print("Not enough arguments provided, type \"cc help\" to help")
    else:
        print("Not enough arguments provided, type \"cc help\" to help")

def faultMon(args):
    if(len(args)>1):
        if(args[1]=='help'):
            print("This functions computes the fault monitor of the given fsa")
            print("Usage:\n     fm outputname inputname")
        elif(len(args)>2):
            if(not args[1] in fsalst):
                fsalst[args[1]]=fm(fsalst[args[2]])
            else:
                print("Error, output name already exists") #TODO ask to overwrite?
        else:
            print("Not enough arguments provided, type \"fm help\" to help")
    else:
        print("Not enough arguments provided, type \"fm help\" to help")

def observer(args):
    if(len(args)>1):
        if(args[1]=='help'):
            print("This functions computes the equivalent DFA of the given NFA")
            print("Usage:\n     nfa2dfa outputname inputname")
            print("Alternative:\n     obs outputname inputname")
        elif(len(args)>2):
            if(not args[1] in fsalst):
                fsalst[args[1]]=nfa2dfa(fsalst[args[2]])
            else:
                print("Error, output name already exists") #TODO ask to overwrite?
        else:
            print("Not enough arguments provided, type \"fm help\" to help")
    else:
        print("Not enough arguments provided, type \"fm help\" to help")

commands={
    'load': loadfsa,
    'build': buildfsa,
    'show': showfsa,
    'list': listfsa,
    'cc': concComp,
    'fm': faultMon,
    'nfa2dfa': observer,
    'obs': observer,
    'help': help
}


help()
fsalst=dict()

while(1):
    cmd=input(">>").split(' ')
    
    #remove empty strings or double spaces
    while("" in cmd):
        cmd.remove("")
    
    if(cmd[0] in commands):
        commands[cmd[0]](cmd)
    else:
        print("unrecognized command")



