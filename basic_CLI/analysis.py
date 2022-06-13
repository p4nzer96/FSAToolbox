import fsatoolbox
from fsatoolbox import *
from fsatoolbox.utils.analysis import get_blockingness_info, get_deadness_info, get_reachability_info, get_reversibility_info, get_trim_info

def reachability(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes the reachability of a fsa")
        print("Usage:\n     reach fsa_name (Ex: reach G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"reach -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        is_reachable, reachable_states = get_reachability_info(fsalst[args[0]])
        if(is_reachable):
            print("The fsa is reachable")
            print("Reachable states:",end=' -> ')
            print(reachable_states)
        else:
            print("The fsa is not reachable")
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)

def coreachability(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes the co-reachability of a fsa")
        print("Usage:\n     coreach fsa_name (Ex: coreach G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"coreach -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        is_coreachable, coreachable_states = get_reachability_info(fsalst[args[0]])
        if(is_coreachable):
            print("The fsa is co-reachable")
            print("Co-reachable states:",end=' -> ')
            print(coreachable_states)
        else:
            print("The fsa is not reachable")
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)

def blocking(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes if the fsa is blocking")
        print("Usage:\n     blocking fsa_name (Ex: blocking G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"blocking -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        is_blocking, blocking_states = get_blockingness_info(fsalst[args[0]])
        if(is_blocking):
            print("The fsa is blocking")
            print("Blocking states:",end=' -> ')
            print(blocking_states)
        else:
            print("The fsa is not blocking")
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)

def trim(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes if the fsa is trim")
        print("Usage:\n     trim fsa_name (Ex: trim G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"trim -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        is_trim = get_trim_info(fsalst[args[0]])
        if(is_trim):
            print("The fsa is trim")
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)

def dead(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes if the fsa is dead")
        print("Usage:\n     dead fsa_name (Ex: dead G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"dead -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        dead = get_deadness_info(fsalst[args[0]])
        if len(dead)==0:
            print("There are no dead events")
        else:
            print("List of dead events", end=' -> ')
            print(dead)
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)

def reverse(args,eventslst,fsalst,path):
    if('-h' in args):
        print("This functions computes if the fsa is reversible")
        print("Usage:\n     reverse fsa_name (Ex: reverse G0)")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return
    
    if(len(args)<1):
        print("Not enough arguments provided, type \"reverse -h\" to help")
        return
    
    if(args[0] not in fsalst):
        print("Error, fsa doesn't exists")
        return
    
    try:   
        is_reversable = get_reversibility_info(fsalst[args[0]])
        if(is_reversable):
            print("The fsa is reversible")
        else:
            print("The fsa is not reversible")
        
    except Exception as e:
        print("There was an error while computing the reachability:")
        print(e)