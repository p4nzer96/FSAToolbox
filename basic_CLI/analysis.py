from fsatoolbox.analysis import get_blockingness_info, get_deadness_info, get_reachability_info, \
    get_reversibility_info, get_trim_info, get_co_reachability_info
from termcolor import colored
import colorama

colorama.init()


def reachability(args, fsalst):
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
        print("")
        if is_reachable:
            print(colored("The fsa is reachable", "green"))
            print("Reachable states:", end=' -> ')
            print(reachable_states)
        else:
            print(colored("The fsa is not reachable", "yellow"))
            print("Reachable states:", end=' -> ')
            print(reachable_states)
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def coreachability(args, fsalst):
    if '-h' in args:
        print(
            colored("\ncoreach: ", "yellow", attrs=["bold"]) + "This functions computes the co-reachability of a fsa\n")
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
        print("")
        if is_coreachable:
            print(colored("The fsa is co-reachable", "green"))
            print("Co-reachable states:", end=' -> ')
            print(coreachable_states)
        else:
            print(colored("The fsa is not co-reachable", "yellow"))
            print("Co-reachable states:", end=' -> ')
            print(coreachable_states)
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def blocking(args, fsalst):
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
        print("")
        if is_blocking:
            print(colored("The fsa is blocking", "yellow"))
            print("Blocking states:", end=' -> ')
            print(blocking_states)
        else:
            print(colored("The fsa is not blocking", "green"))
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def trim(args, fsalst):
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
        print("")
        if is_trim:
            print(colored("The fsa is trim", "green"))
        else:
            print(colored("The fsa is not trim", "yellow"))
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def dead(args, fsalst):
    if '-h' in args:
        print(colored("\ndead: ", "yellow", attrs=["bold"]) + "This functions computes if a fsa has dead states\n")
        print(colored("Usage:", attrs=["bold"]) + "\n\tdead fsa_name\n")
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
        print("")
        if len(dead) == 0:
            print(colored("There are no dead states", "green"))
        else:
            print(colored("There are dead states", "yellow"))
            print("List of dead states", end=' -> ')
            print(dead)
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:", "red"))
        print(e)


def reverse(args, fsalst):
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
        print("")
        if is_reversable:
            print(colored("The fsa is reversible", "green"))
        else:
            print(colored("The fsa is not reversible", "yellow"))
        print("")

    except Exception as e:
        print(colored("There was an error while computing the reachability:\n", "red"))
        print(e)
