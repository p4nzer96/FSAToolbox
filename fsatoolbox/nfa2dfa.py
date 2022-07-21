import pandas as pd
from fsatoolbox import fsa
from fsatoolbox.utils.misc import v_print


def nfa2dfa(G, iterationsLimit=100, verbose=False, name_style=0):
    """
    Function to compute the equivalent DFA of a NFA

    Args:
        G(fsa): input NFA
        iterationsLimit (optional, int): Default=100, this avoids an infinite loop when there are unobservable loops
        verbose (optional, bool): Default=False, if true shows the steps followed by the algorithm
        name_style (optional, int): Default=0, available values: 0
        this describes how the names of two or more states are used to build the new state name

    Returns:
        A FSA that represents the equivalent DFA of the input NFA

    """
    DFA = fsa()

    # This dataframe contains D_eps and D_e for every state of the NFA
    # D_eps is the set of reachable states with zero or more unobservable transitions
    # D_e for every event e is the set of states reachable with a single event e
    D = pd.DataFrame({'x': G.X})

    Euo = [e for e in G.E if not e.isObservable]  # unobservable events
    Eo = [e for e in G.E if e.isObservable]  # observable events

    # The alphabet of the output DFA is the set of observable events of the NFA
    DFA.E = Eo

    # Build Deps
    Deps = []

    # Iterating through the states of the NFA
    for current_state in G.X:
        t = []  # Reachable states executing one or more unobservable transitions
        tnew = [current_state]  # States to check
        idx = 0
        while len(tnew) > 0:

            if idx > iterationsLimit:
                raise Exception("Iterations limit reached, there is a unobservable loop in the automaton?")

            state = tnew.pop(0)

            for event in Euo:
                transitions = G.filter_delta(start=state, transition=event)
                for _, trans in transitions.iterrows():
                    tnew.append(trans['end'])

            if state not in t:
                t.append(state)
            idx += 1

        Deps.append(t)
    D['Deps'] = Deps

    # Build De for every event e
    for event in Eo:
        De = []
        for state in G.X:
            e = []
            transitions = G.filter_delta(start=state, transition=event)
            for _, trans in transitions.iterrows():
                e.append(trans['end'])
            e.sort(key=lambda x: x.label)
            De.append(e)
        D['D' + event.label] = De

    v_print(D, verbose)

    # build the "alpha-beta" table
    X = []
    Xnew = [D['Deps'][0]]  # initial state TODO check for multiple initial states
    AB = pd.DataFrame()

    while len(Xnew) > 0:

        x = Xnew.pop(0)  # select a state to analyze
        v_print("\nAnalyzing the state: {}".format(str(x)), verbose)
        X.append(x)

        tempdf = pd.DataFrame({'x': [x]})  # initialize a data frame for this row

        for event in Eo:  # for every observable event
            v_print("\tevent: {}".format(event.label), verbose, end="->")
            alpha = []
            for state in x:  # for each NFA state in this DFA state
                # search where we can go with a single transition of the current event
                trInx = D.index[D.index[D['x'] == state]].tolist()
                transition = D['D' + event.label][trInx[0]]
                # if it's not already in alpha, add it
                if len(transition) > 0:
                    for trans in transition:
                        if trans not in alpha:
                            alpha.append(trans)
            alpha.sort(key=lambda x: x.label)  # sort alphabetically ste states
            tempdf['alpha:' + event.label] = [alpha]  # add entry in the current data frame row
            v_print("alpha: {}".format(str(alpha)), verbose, end=", ")
            # check for eps-transitions from the alpha states
            beta = []
            for el in alpha:
                trInx = D.index[D.index[D['x'] == el]].tolist()
                transition = D['Deps'][trInx[0]]
                if len(transition) > 0:
                    for trans in transition:
                        if trans not in beta:
                            beta.append(trans)
            beta.sort(key=lambda x: x.label)  # sort alphabetically the states
            tempdf['beta:' + event.label] = [beta]  # add entry in the current data frame row
            v_print("beta: {}".format(str(beta)), verbose)
            # check if the new state is already known, otherwise add it to Xnew
            if len(beta) > 0 and beta not in Xnew and beta not in X:
                Xnew.append(beta)
        AB = pd.concat([AB, tempdf], axis=0)

    v_print("", verbose)
    v_print(AB, verbose)

    # Add the found states to the DFA
    # The states are a list of states, this converts them to a single state
    for x in X:
        final = False
        initial = False
        name = ""
        for el in x:
            if name_style == 0:
                name = name + el.label
            if el.isFinal:
                final = True
            if el.isInitial:
                initial = True
        DFA.add_state(name, isInitial=initial, isFinal=final)

    # Add transitions to the DFA
    for i in range(AB.shape[0]):
        initial_st = ""
        if name_style == 0:
            for el in (AB['x'].tolist())[i]:
                initial_st = initial_st + el.label
        for ev in Eo:
            end_st = ""
            if name_style == 0:
                for el in (AB['beta:' + ev.label].tolist())[i]:
                    end_st = end_st + el.label
            if not end_st == "":
                DFA.add_transition(initial_state=initial_st, tr_event=ev, end_state=end_st)

    return DFA
