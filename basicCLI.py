import shlex
import os
from fsatoolbox import *

from basic_CLI.checkevents import checkevents, updateevents
from basic_CLI.loadfsa import loadfsa
from basic_CLI.savefsa import savefsa
from basic_CLI.fsabuilder import fsabuilder
from basic_CLI.editfsa import addstate, rmstate, addevent, rmevent, addtrans, rmtrans
from basic_CLI.conccomp import conccomp
from basic_CLI.faultmon import faultmon
from basic_CLI.diagnoser import diagnoser
from basic_CLI.observer import observer
from basic_CLI.super import supervisor
from basic_CLI.exth import exth

#commands

def help(args=None):
    print("This is only a test version: available commands:")
    for key,val in commands.items():
        print("-> "+key)
    print("[CTRL+C to exit]")

def changepath(args, path):
    if('-h' in args):
        print("This functions changes the default path")
        print("Usage:\n     changepath newpath (Ex: changepath C:\\Automi")
        return path
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"changepath help\" to help")
        return path

    if(os.path.isdir(args[0])):
        return args[0]
    else:
        print("Invalid path")
        return path

def removefsa(args, fsalst, path):
    if('-h' in args):
        print("Removes a fsa from the list")
        print("Usage:\n->rm fsa_name (Ex:rm G0)")
        return

    if(len(args)<1):
        print("Not enough arguments provided, type \"rm -h\" to help")
        return

    if(args[0] not in fsalst):
        print("fsa not found")
        return

    del fsalst[args[0]]

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

def listevents(args, eventslst, fsalst, path):
    for e in eventslst:
        print("- "+e.label+":  Observable: "+str(e.isObservable)+", Controllable: "+str(e.isControllable)+", Fault: "+str(e.isFault))

#list of loaded FSA
fsalst=dict()
eventslst=[]

commands={
    'changepath' : changepath,
    'path' : currpath,
    'load': loadfsa,
    'rm': removefsa,
    'save': savefsa,
    'build': fsabuilder,
    'addstate': addstate,
    'rmstate': rmstate,
    'addevent' : addevent,
    'rmevent' : rmevent,
    'addtrans' : addtrans,
    'rmtrans' : rmtrans,
    'show': showfsa,
    'xlist': listfsa,
    'elist': listevents,
    'cc': conccomp,
    'fm': faultmon,
    'diag' : diagnoser,
    'nfa2dfa': observer,
    'obs': observer,
    'supervisor': supervisor,
    'exth': exth,
    'help': help
}


home=os.path.expanduser("~")
path=home+'\\Documents\\FsaToolbox'

if not os.path.exists(path):
    os.makedirs(path)

help()
print("->exit")
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
    if(cmd[0]=='exit'):
        break
    if(cmd[0] in commands):
        commands[cmd[0]](args,eventslst,fsalst,path)
    else:
        print("unrecognized command")



