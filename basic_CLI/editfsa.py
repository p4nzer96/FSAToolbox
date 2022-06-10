from shutil import ExecError
from numpy import array2string
import fsatoolbox
from fsatoolbox import *

def addstate(args, fsalst, path):
    if('-h' in args):
        print("This functions adds a state to a fsa")
        print("Usage:\n     addstate fsa_name state_name (ex: addstate G0 x0)")
        print("Optional arguments:")
        print("-i set state as initial")
        print("-f set state as final")
        print("-fr set state as forbidden")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"addstate -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].add_state(args[1],isInitial=('-i' in args),isFinal=('-f' in args),isForbidden=('-f' in args),)
    except Exception as e:
        print("There was an error while adding the state:")
        print(e)

def rmstate(args, fsalst, path):
    if('-h' in args):
        print("This functions removes a state to a fsa")
        print("Usage:\n     rmstate fsa_name state_name (ex: rmstate G0 x0)")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"rmstate -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].remove_state(args[1])
    except Exception as e:
        print("There was an error while removing the state:")
        print(e)

def addevent(args, fsalst, path):
    if('-h' in args):
        print("This functions adds an event to a fsa")
        print("Usage:\n     addevent fsa_name event_name (ex: addevent G0 a)")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"addevent -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].add_event(args[1])
    except Exception as e:
        print("There was an error while adding the event:")
        print(e)

def rmevent(args, fsalst, path):
    if('-h' in args):
        print("This functions removes an event to a fsa")
        print("Usage:\n     rmevent fsa_name event_name (ex: rmevent G0 x0)")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"rmevent -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].remove_event(args[1])
    except ExecError as e:
        print("There was an error while removing the event:")
        print(e)

def addtrans(args, fsalst, path):
    if('-h' in args):
        print("This functions adds a transition to a fsa")
        print("Usage:\n     addtrans fsa_name initial_state event final_state (ex: addtrans G0 x0 a x1)")
        return

    if(len(args)<3):
        print("Not enough arguments provided, type \"addtrans -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].add_transition(args[1],args[2],args[3])
    except Exception as e:
        print("There was an error while adding the transition:")
        print(e)

def rmtrans(args, fsalst, path):
    if('-h' in args):
        print("This functions removes a transition to a fsa")
        print("Usage:\n     rmtrans fsa_name initial_state event final_state (ex: rmtrans G0 x0 a x1)")
        return

    if(len(args)<2):
        print("Not enough arguments provided, type \"rmevent -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    try:
        fsalst[args[0]].remove_transition(args[1],args[2],args[3])
    except Exception as e:
        print("There was an error while removing the event:")
        print(e)