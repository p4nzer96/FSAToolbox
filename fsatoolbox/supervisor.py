from fsatoolbox.fsa import fsa
from fsatoolbox.state import state
from fsatoolbox.cc import cc
from fsatoolbox.trim import trim
import copy


def hhat(H, verbose=False):
    """
    Function that, given H (where H represents a specification automaton), returns the corresponding extended
    specification automaton

    Args:
        H (fsa): specification automaton

    Returns:
        fsa
    """
    yf = state("yf", isInitial=False, isFinal=False, isForbidden=True)

    Hh = copy.deepcopy(H)
    Hh.add_state(yf)

    for x in H.X:
        for e in H.E:
            filt_df = H.filter_delta(start=x, transition=e)
            if filt_df.empty and not e.isControllable:
                Hh.add_transition(x, e, yf)

    return Hh


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


def compute_supervisor(G, H, verbose=False):
    # Computing the extended specification automaton
    h_hat = hhat(H)

    # Computing the composition automaton
    A = cc(G, h_hat)

    # Getting the set of forbidden states
    forbidden = get_forbidden(A)

    if len(forbidden) == 0:
        return A

    weakly_forbidden = get_weakly_forbidden(A, forbidden)

    for x in A.x0:

        if x in weakly_forbidden:

            return None

    wf_f_states = forbidden + weakly_forbidden

    for x in wf_f_states:

        if x in A.X:

            A.remove_state(x)

    A = trim(A)

    return A
