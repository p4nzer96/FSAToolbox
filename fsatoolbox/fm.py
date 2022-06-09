from fsatoolbox import fsa, state


def fm(G):
    """
    Given an input automaton G, computes its Fault Monitor

    Args:
        G (fsa): FSA used as input

    Returns:
        fsa: The corresponding Fault Monitor of G

    """
    FM = fsa()

    # the alphabet is the same
    FM.E = G.E

    # states generation
    N = state(label="N", isInitial=True, isFinal=False)
    FM.add_state(N)
    F = state(label="F", isInitial=False, isFinal=False)
    FM.add_state(F)

    for el in FM.E:
        if el.isFault is None:
            raise ValueError("The event " + el.label + " is not initialized properly: Fault state not set")
        elif el.isFault == 1:
            FM.add_transition(N, el, F)
            FM.add_transition(F, el, F)
        elif el.isFault == 2:
            FM.add_transition(N, el, N)
            FM.add_transition(F, el, F)
    return FM
