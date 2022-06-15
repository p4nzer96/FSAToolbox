from fsatoolbox import *
from fsatoolbox.nfa2dfa import nfa2dfa
from fsatoolbox.utils.misc import v_print


def diag(G, verbose=False):
    # Fault monitor
    v_print("Compute the fault monitor:", verbose)
    FM = fm(G, verbose)
    v_print("\n\nFault monitor:", verbose)
    v_print(FM, verbose)

    # Fault recognizer
    v_print("Compute the fault recognizer:", verbose)
    FR = cc(G, FM, verbose)
    v_print("\n\nFault recognizer:", verbose)
    v_print(FR, verbose)

    # Diagnoser
    v_print("Compute the diagnoser:", verbose)
    D = nfa2dfa(FR, verbose=verbose)
    v_print("\n\nDiagnoser:", verbose)
    v_print(FM, verbose)

    return D
