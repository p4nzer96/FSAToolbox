from fsatoolbox.fsa import fsa
from fsatoolbox.state import state
from fsatoolbox import cc
import copy


def hhat(H):
    """
    Function that, given H (where H represents a specification automaton), returns the corresponding extended
    specification automaton

    Args:
        H (fsa): specification automaton

    Returns:
        fsa
    """
    yf = state("yf", isForbidden=True)

    Hh = copy.deepcopy(H)
    Hh.add_state(yf)

    for x in H.X:
        for e in H.E:
            filt_df = H.filter_delta(start=x, transition=e)
            if filt_df.empty and not e.isControllable:
                Hh.add_transition(x, e, yf)

    return Hh


def comp_automaton(G, Hh):
    return cc(G, Hh)


def get_forbidden(A):
    forbidden_states = []

    for x in A.X:

        if x.isForbidden:
            forbidden_states.append(x)

    return forbidden_states


def get_weakly_forbidden(A: fsa, forbidden: list):
    wb_states = []  # Set of weakly forbidden states
    X_new = copy.deepcopy(forbidden)  # Set of forbidden states

    # Run until X_new is empty
    while len(X_new) != 0:

        # For each state in X_new
        for x in X_new:

            # For each event which is not controllable
            for e in [x for x in A.E if x.isControllable is False]:

                # Filter all transition based on non-controllable event and given final state
                filt_trans = A.filter_delta(transition=e, end=x)

                # For each transition in filt_trans
                for _, trans in filt_trans.iterrows():

                    start_state = trans["start"]

                    if start_state not in X_new:
                        if start_state not in wb_states:
                            wb_states.append(start_state)  # Add the state in the set of weakly forbidden states
                        X_new.append(start_state)  # Add the state in X_new if not present

            X_new.remove(x)  # Remove the current state from X_new

    return list(wb_states)
