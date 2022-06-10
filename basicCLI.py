import shlex
import os
from fsatoolbox import *

from basic_CLI.loadfsa import loadfsa
from basic_CLI.savefsa import savefsa
from basic_CLI.fsabuilder import fsabuilder
from basic_CLI.editfsa import addstate, rmstate, addevent, rmevent, addtrans, rmtrans
from basic_CLI.conccomp import conccomp
from basic_CLI.faultmon import faultmon
from basic_CLI.observer import observer

#commands

def help(args=None):
    print("This is only a test version: available commands:")
    for key,val in commands.items():
        print("->"+key)
    print("[CTRL+C to exit]")

def changepath(args, path):
    if('-h' in args):
        print("This functions changes the default path")
        print("Usage:\n     changepath newpath (Ex: changepath C:\\Automi")
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"changepath help\" to help")

    if(os.path.isdir(args[0])):
        return args[0]
    else:
        print("Invalid path")
        return path

def currpath(args, fsalst, path):
    if('-h' in args):
        print("Print the current path")

    print(path)

def showfsa(args, fsalst, path):
    #TODO
    if(len(args)<1):
        print("Not enough arguments provided, type \"showfsa -h\" to help")
        return

    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    print(fsalst[args[0]])

def listfsa(args, fsalst, path): #TODO add some stats?
    for key,value in fsalst.items():
        print(key)

#list of loaded FSA
fsalst=dict()

commands={
    'changepath' : changepath,
    'path' : currpath,
    'load': loadfsa,
    'save': savefsa,
    'build': fsabuilder,
    'addstate': addstate,
    'rmstate': rmstate,
    'addevent' : addevent,
    'rmevent' : rmevent,
    'addtrans' : addtrans,
    'rmtrans' : rmtrans,
    'show': showfsa,
    'list': listfsa,
    'cc': conccomp,
    'fm': faultmon,
    'nfa2dfa': observer,
    'obs': observer,
    'help': help
}


home=os.path.expanduser("~")
path=home+'\\Documents\\FsaToolbox\\'

if not os.path.exists(path):
    os.makedirs(path)

help()
print("\n\nNote: the default path is:")
print(path)
print("")


while(1):
    cmd=shlex.split(input(">>"))
    if cmd==[]:
        continue
    args = cmd[1:] #extract arguments

    if(cmd[0]=='changepath'):
        path=changepath(args, path)
        continue
    if(cmd[0] in commands):

        commands[cmd[0]](args,fsalst,path)
    else:
        print("unrecognized command")



