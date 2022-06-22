from shutil import ExecError
from numpy import array2string
from termcolor import colored

import fsatoolbox
from fsatoolbox import *
import colorama

colorama.init()


def addstate(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\naddstate: ", "yellow", attrs=["bold"]) + "This functions adds a state to a fsa")
        print(colored("\nUsage:") + "\n\taddstate fsa_name state_name")
        print(colored("\nOptional arguments:")
              + "\n\t-i set state as initial"
              + "\n\t-f set state as final"
              + "\n\t-fb set state as forbidden")
        print(colored("\nExample:") + "\n\taddstate G0 x0")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"addstate -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].add_state(args[1], isInitial=('-i' in args), isFinal=('-f' in args),
                                  isForbidden=('-fb' in args), )
    except Exception as e:
        print(colored("There was an error while adding the state:", "red"))
        print(e)


def rmstate(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nrmstate: ", "yellow", attrs=["bold"]) + "This functions removes a state to a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\trmstate fsa_name state_name")
        print(colored("\nExample:", attrs=["bold"]) + "\n\trmstate G0 x0")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"rmstate -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].remove_state(args[1])
    except Exception as e:
        print(colored("There was an error while removing the state:", "red"))
        print(e)


def addevent(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\naddevent: ", "yellow", attrs=["bold"]) + "This functions adds an event to a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\taddevent fsa_name event_name")
        print(colored("\nExample:", attrs=["bold"]) + "\n\taddevent G0 a")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"addevent -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].add_event(args[1])
    except Exception as e:
        print(colored("There was an error while adding the event:", "red"))
        print(e)


def rmevent(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nrmevent: ", "yellow", attrs=["bold"]) + "This functions removes an event from a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\trmevent fsa_name event_name")
        print(colored("\nExample:", attrs=["bold"]) + "\n\trmevent G0 a")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"rmevent -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].remove_event(args[1])
    except ExecError as e:
        print(colored("There was an error while removing the event:", "red"))
        print(e)


def addtrans(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\naddtrans: ", "yellow", attrs=["bold"]) + "This functions adds a transition to a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\taddtrans fsa_name initial_state event final_state")
        print(colored("\nExample:", attrs=["bold"]) + "\n\taddtrans G0 x0 a x1")
        print("")
        return

    if len(args) < 3:
        print(colored("Not enough arguments provided, type \"addtrans -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].add_transition(args[1], args[2], args[3])
    except Exception as e:
        print(colored("There was an error while adding the transition:", "red"))
        print(e)


def rmtrans(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nrmtrans: ", "yellow", attrs=["bold"]) + "This functions removes a transition to a fsa")
        print(colored("\nUsage:", attrs=["bold"]) + "\n\trmtrans fsa_name initial_state event final_state")
        print(colored("\nExample:", attrs=["bold"]) + "\n\trmtrans G0 x0 a x1")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"rmtrans -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        fsalst[args[0]].remove_transition(args[1], args[2], args[3])
    except Exception as e:
        print(colored("There was an error while removing the event:", "red"))
        print(e)


def editstate(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\neditstate:", "yellow", attrs=["bold"]) + "This functions is used to modify a state inside a "
                                                                  "fsa")
        print(colored("\nUsage:") + "\n\teditstate fsa_name state_name -options")
        print(colored("\nOptions:") +
              "\n\t-i set the state as initial" +
              "-\n\t-f set the state as final" +
              "\n\t-fb set the state as forbidden")
        print("")
        return

    if len(args) < 2:
        print(colored("Not enough arguments provided, type \"editstate -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return
    try:
        props = {
            'isInitial': ('-i' in args),
            'isFinal': ('-f' in args),
            'isForbidden': ('-fb' in args)
        }
        fsalst[args[0]].change_state_props(args[1], **props)
    except Exception as e:
        print(colored("There was an error while adding the event:", "red"))
        print(e)
