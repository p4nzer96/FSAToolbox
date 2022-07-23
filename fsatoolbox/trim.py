import copy

from fsatoolbox import fsa, analysis


def trim(fsa_obj: fsa, **kwargs):

    # Check if there are no or multiple initial states

    if len(fsa_obj.x0) == 0:
        raise TypeError("Initial state not set")

    if len(fsa_obj.x0) > 1:
        raise TypeError("Multiple initial states")

    G = copy.deepcopy(fsa_obj)

    if G.is_Trim is None:
        analysis.get_trim_info(G)

    if G.is_Trim:
        return G

    fsa_states = G.X.copy()

    for x in fsa_states:
        if not (x.is_Reachable and x.is_co_Reachable):
            G.remove_state(x)

    return G
