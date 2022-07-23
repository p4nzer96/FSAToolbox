from fsatoolbox import *
from fsatoolbox.nfa2dfa import nfa2dfa
from fsatoolbox.utils.misc import v_print


def diag(G, verbose=False):

    # Check if there are no or multiple initial states

    if len(G.x0) == 0:
        raise TypeError("Initial state not set")

    if len(G.x0) > 1:
        raise TypeError("Multiple initial states")

    # Fault monitor
    FM = fm(G)
    v_print("\n\nFault monitor:", verbose)
    v_print(FM, verbose)

    # Fault recognizer
    FR = cc(G, FM)
    v_print("\n\nFault recognizer:", verbose)
    v_print(FR, verbose)

    # Diagnoser
    D = nfa2dfa(FR)
    v_print("\n\nDiagnoser:", verbose)
    v_print(D, verbose)

    return D
