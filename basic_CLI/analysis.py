import fsatoolbox
from fsatoolbox import *
from fsatoolbox.utils.analysis import get_blockingness_info, get_deadness_info, get_reachability_info, \
    get_reversibility_info, get_trim_info, get_co_reachability_info
from termcolor import colored


def reachability(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nreach: ", "yellow", attrs=["bold"]) + "This functions computes the reachability of a fsa\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\treach fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + "\n\treach G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"reach -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        is_reachable, reachable_states = get_reachability_info(fsalst[args[0]])
        if is_reachable:
            print("The fsa is reachable")
            print("Reachable states:", end=' -> ')
            print(reachable_states)
        else:
            print("The fsa is not reachable")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def coreachability(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ncoreach: ", "yellow", attrs=["bold"]) + "This functions computes the co-reachability of a fsa\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tcoreach fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + "\n\tcoreach G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"coreach -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        is_coreachable, coreachable_states = get_co_reachability_info(fsalst[args[0]])
        if is_coreachable:
            print("The fsa is co-reachable")
            print("Co-reachable states:", end=' -> ')
            print(coreachable_states)
        else:
            print("The fsa is not co-reachable")
            print("Co-reachable states:", end=' -> ')
            print(coreachable_states)

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def blocking(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nblocking: ", "yellow", attrs=["bold"]) + "This functions computes if the fsa is blocking\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tblocking fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + "\n\tblocking G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"blocking -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        is_blocking, blocking_states = get_blockingness_info(fsalst[args[0]])
        if is_blocking:
            print("The fsa is blocking")
            print("Blocking states:", end=' -> ')
            print(blocking_states)
        else:
            print("The fsa is not blocking")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def trim(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ntrim: ", "yellow", attrs=["bold"]) + "This functions computes if the fsa is trim\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\ttrim fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + "\n\ttrim G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"trim -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        is_trim = get_trim_info(fsalst[args[0]])
        if is_trim:
            print("The fsa is trim")
        else:
            print("The fsa is not trim")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def dead(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\ndead: ", "yellow", attrs=["bold"]) + "This functions computes if a fsa has dead states\n")
        print(colored("Usage:", attrs=["bold"]) +"\n\tdead fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + "\n\tdead G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"dead -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        dead = get_deadness_info(fsalst[args[0]])
        if len(dead) == 0:
            print("There are no dead events")
        else:
            print("List of dead events", end=' -> ')
            print(dead)

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def reverse(args, eventslst, fsalst, path):
    if '-h' in args:
        print(colored("\nreverse: ", "yellow", attrs=["bold"]) + "This functions computes if the fsa is reversible\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\treverse fsa_name\n")
        print(colored("Example:", attrs=["bold"]) + " \n\treverse G0")
        print("")
        # print("Optional arguments:")
        # print("-v verbose output, this will print the steps of the algorithm")
        return

    if len(args) < 1:
        print(colored("Not enough arguments provided, type \"reverse -h\" to help", "yellow"))
        return

    if args[0] not in fsalst:
        print(colored("Error, fsa doesn't exists", "red"))
        return

    try:
        is_reversable = get_reversibility_info(fsalst[args[0]])
        if is_reversable:
            print("The fsa is reversible")
        else:
            print("The fsa is not reversible")

    except Exception as e:
        print(colored("There was an error while computing the reachability:\n", "red"))
        print(e)
