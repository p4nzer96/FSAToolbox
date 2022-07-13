from fsatoolbox.fsa import fsa

from fsatoolbox.fm import fm
from fsatoolbox.diag import diag

from termcolor import colored
import colorama

colorama.init()

def fm_cli(p_args: fsa, verbose):
    #check if the events have the faulty propriety set
    faultyset=True
    for e in p_args.E:
        if e.isFault == None:
            faultyset=False

    #if not, ask the user to input faulty events
    if not faultyset:
        print(colored("Fault propriety not set in some events","yellow"))
        while(1):
            print("Events in this fsa:",end=" ")
            print(p_args.E)
            inp=input(colored("Please input the list of faulty events, separated by a space:\n", "yellow")).split(' ')
            while "" in inp:  # remove empty strings or double spaces, better way?
                inp.remove("")

            #set faulty propriety
            for e in p_args.E:
                try:
                    if e.label in inp:
                        isFault=True
                    else:
                        isFault=False
                    p_args.change_event_props(e, **{'isFault':isFault})
                except Exception as e:
                    print(colored(e,"red"))
                    continue
            break
    
    #function call
    return fm(p_args)

def diag_cli(p_args: fsa, verbose):
    #check if the events have the faulty propriety set
    faultyset=True
    for e in p_args.E:
        if e.isFault == None:
            faultyset=False

    #if not, ask the user to input faulty events
    if not faultyset:
        print(colored("Fault propriety not set in some events","yellow"))
        while(1):
            print("Events in this fsa:",end=" ")
            print(p_args.E)
            inp=input(colored("Please input the list of faulty events, separated by a space:\n", "yellow")).split(' ')
            while "" in inp:  # remove empty strings or double spaces, better way?
                inp.remove("")

            #set faulty propriety
            for e in p_args.E:
                try:
                    if e.label in inp:
                        isFault=True
                    else:
                        isFault=False
                    p_args.change_event_props(e, **{'isFault':isFault})
                except Exception as e:
                    print(colored(e,"red"))
                    continue
            break
    
    #function call
    return diag(p_args, verbose)