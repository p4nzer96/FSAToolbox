from fsatoolbox.analysis import get_blockingness_info, get_deadness_info, get_reachability_info, \
    get_reversibility_info, get_trim_info, get_co_reachability_info
from termcolor import colored
import colorama

colorama.init()

def reachability_cli(p_args):
    is_reachable, reachable_states = get_reachability_info(p_args)
    if is_reachable:
        print(colored("The fsa is reachable", "green"))
        print("Reachable states:", end=' -> ')
        print(reachable_states)
    else:
        print(colored("The fsa is not reachable", "yellow"))
        print("Reachable states:", end=' -> ')
        print(reachable_states)

def coreachability_cli(p_args):
    is_coreachable, coreachable_states = get_co_reachability_info(p_args)
    if is_coreachable:
        print(colored("The fsa is co-reachable", "green"))
        print("Co-reachable states:", end=' -> ')
        print(coreachable_states)
    else:
        print(colored("The fsa is not co-reachable", "yellow"))
        print("Co-reachable states:", end=' -> ')
        print(coreachable_states)

def blocking_cli(p_args):
    is_blocking, blocking_states = get_blockingness_info(p_args)
    if is_blocking:
        print(colored("The fsa is blocking", "yellow"))
        print("Blocking states:", end=' -> ')
        print(blocking_states)
    else:
        print(colored("The fsa is not blocking", "green"))

def trim_cli(p_args):
    is_trim = get_trim_info(p_args)
    if is_trim:
        print(colored("The fsa is trim", "green"))
    else:
        print(colored("The fsa is not trim", "yellow"))

def dead_cli(p_args):
    dead = get_deadness_info(p_args)
    if len(dead) == 0:
        print(colored("There are no dead states", "green"))
    else:
        print(colored("There are dead states", "yellow"))
        print("List of dead states", end=' -> ')
        print(dead)

def reverse_cli(p_args):
    is_reversable = get_reversibility_info(p_args)
    if is_reversable:
        print(colored("The fsa is reversible", "green"))
    else:
        print(colored("The fsa is not reversible", "yellow"))