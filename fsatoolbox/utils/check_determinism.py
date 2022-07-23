from fsatoolbox import fsa


class ObsNotSet(Exception):
    def __init__(self, G):
        super().__init__(self)
        self.fsa = G


def check_det(G: fsa):
    ind_events = False
    silent_events = False
    multiple_initial = False

    error_str = ""
    try:

        assert not all(e.isObservable is None for e in G.E)

    except AssertionError:
        raise ObsNotSet(G)

    try:

        assert None not in [e.isObservable for e in G.E]

    except AssertionError:

        print("Warning: Some events do not have the observability property set. "
              "These will be considered by default as observable")

    silent_list = []
    for e in G.E:
        if e.isObservable is False:
            silent_events = True
            silent_list.append(e)

    transition_list = []
    for x in G.X:
        events = G.filter_delta(start=x).transition

        if any(events.duplicated()):
            ind_events = True
            transition_list.append(x)

    if len(G.x0) > 1:
        multiple_initial = True

    if multiple_initial is True or silent_events is True or ind_events is True:

        error_str = "\nThe FSA {} is Not-Deterministic. Causes:\n\n".format(G.name)

        if silent_events is True:
            error_str += "\t * Silent events found: {}\n".format(str(silent_list)[1:-1])
        if ind_events is True:
            error_str += "\t * Indistinguishable events found: check transitions outputting" \
                         " from states {}\n".format(str(transition_list)[1:-1])
        if multiple_initial is True:
            error_str += "\t Multiple initial states: {}\n".format(str(G.x0)[1:-1])

        error_str += "\nThe procedure cannot continue, as a deterministic automaton is required\n"

        return True, error_str
    else:
        return False, error_str
