import json

import numpy as np
import pandas as pd
from tabulate import tabulate

from event import Event
from state import State


class FSA:
    """
    Class used to represent a Finite State Automaton (FSA)

    Parameters
    ----------
    X : list of State objects
        the set of states of which the automaton is composed
    E : list of Event objects
        the alphabet of the automaton
    delta : DataFrame
        the transition relation / function of the automaton
    x0 : list of State objects
        the initial states of the automaton (all elements of x0 must be contained in X)
    Xm : list of State objects
        the final states of the automaton (all elements of Xm must be contained in X)

    """

    def __init__(self, X=None, E=None, delta=None, x0=None, Xm=None, **kwargs) -> None:

        self.X = X if X else []  # States
        self.E = E if E else []  # Alphabet
        self.delta = delta  # Delta relation
        self.x0 = x0 if x0 else []  # Initial states
        self.Xm = Xm if Xm else []  # Final states

        # Optional: Name of the FSA
        self.name = kwargs.get('name') if kwargs.get('name') else object.__repr__(self)

    @classmethod
    def fromfile(cls, filename):
        """
        Generates a FSA from file

        Args:
            filename (str): the path of the .json file containing the definition of the FSA


        Returns:
            FSA: An instance of FSA
            
        """

        # Load from file

        X = []  # States
        E = []  # Alphabet
        x0 = []  # Initial states
        Xm = []  # Final states

        # File opening

        with open(filename) as jsonFile:
            jsonObject = json.load(jsonFile)

        # Reading states and properties

        for key in jsonObject['X']:
            st_label = key  # State name

            if 'isInit' in jsonObject['X'][key]:
                isInit = eval(jsonObject['X'][key]['isInit'])  # Is the state initial?
            else:
                isInit = None
            if 'isFinal' in jsonObject['X'][key]:
                isFinal = eval(jsonObject['X'][key]['isFinal'])  # Is the state final?
            else:
                isFinal = None

            # Create the state
            state = State(st_label, bool(isInit), bool(isFinal))

            if isInit:  # If the state is initial, add it to initial states
                x0.append(state)

            if isFinal:  # If the state is final, add it to final states
                Xm.append(state)

            # Add the state to X
            X.append(state)

        # Reading events and properties

        for key in jsonObject['E']:
            ev_label = key  # Event name

            if 'isObservable' in jsonObject['E'][key]:
                observable = eval(jsonObject['E'][key]['isObservable'])  # Is observable?
            else:
                observable = None
            if 'isControllable' in jsonObject['E'][key]:
                controllable = eval(jsonObject['E'][key]['isControllable'])  # Is controllable?
            else:
                controllable = None
            if 'isFault' in jsonObject['E'][key]:
                fault = eval(jsonObject['E'][key]['isFault'])  # Is faulty?
            else:
                fault = None

            E.append(Event(ev_label, bool(observable), controllable, fault))

        data = []

        # Reading delta

        for key in jsonObject['delta']:

            start_state = jsonObject['delta'][key]['start']  # Start state

            if start_state not in [s.label for s in X]:  # Check if start state is in X
                raise ValueError("Invalid start state")

            else:

                idx = [x.label for x in X].index(start_state)
                i_state = X[idx]

            transition = jsonObject['delta'][key]['name']  # Transition

            if transition not in [e.label for e in E]:  # Check if transition is in E
                raise ValueError("Invalid event")

            else:

                idx = [x.label for x in E].index(transition)
                trans = E[idx]

            end_state = jsonObject['delta'][key]['ends']

            if end_state not in [s.label for s in X]:  # Check if end state is in X
                raise ValueError("Invalid end state")

            else:

                idx = [x.label for x in X].index(end_state)
                f_state = X[idx]

            data.append([i_state, trans, f_state])

        delta = pd.DataFrame(data, columns=["start", "transition", "end"])

        return cls(X, E, delta, x0, Xm)

    #TODO: Add UI Mode

    def showfsa(self, ui_mode=False):
        """
        Args:
            mode (bool): If True, plot the FSA in UI

        Returns: str or None

        """

        data = np.empty((len(self.X), len(self.E) + 2), dtype='U100')
        column_labels = ["X", "flag"] + [x.label for x in self.E]
        data[:, 0] = [x.label for x in self.X]

        for i, state in enumerate(self.X):
            for j, event in enumerate(self.E):

                filtered_events = self.filter_delta(state, event)['end'].values
                end_labels = [x.label for x in filtered_events]
                string = ""

                if not end_labels:
                    data[i, j + 2] = "-"
                    continue

                for end in end_labels:

                    if not string:

                        string += end

                    else:

                        string += ", " + end

                data[i, j + 2] = string

        for i, state in enumerate(self.X):

            if state.isFinal and state.isInitial:

                data[i, 1] = "I, F"

            elif state.isFinal and not state.isInitial:

                data[i, 1] = "F"

            elif not state.isFinal and state.isInitial:

                data[i, 1] = "I"

            else:

                data[i, 1] = "-"

        table = tabulate(data, headers=column_labels, stralign="center")

        return table

    def __repr__(self):

        rep = self.name + "\n" + self.showfsa()

        return rep

    def filter_delta(self, start=None, transition=None, end=None):
        """
        Filters the delta by starting state, transition or ending state

        Args:
            start (State, optional): starting state. Defaults to None.
            transition (Event, optional): transition event. Defaults to None.
            end (Event, optional): ending state. Defaults to None.

        Returns:
            DataFrame: Filtered delta according to filter passed as argument of the function
        """

        filt_delta = self.delta

        if start:  # Starting state

            start = start.label if isinstance(start, State) else start  # If start is a State object, parse it
            condition = filt_delta["start"].apply(lambda x: x.label) == start
            filt_delta = filt_delta.loc[condition]

        if transition:  # Transition event

            transition = transition.label if isinstance(transition, Event) else transition  # If transition is an Event
            # object, parse it
            condition = filt_delta["transition"].apply(lambda x: x.label) == transition
            filt_delta = filt_delta.loc[condition]

        if end:  # Ending state

            end = end.label if isinstance(end, State) else end  # If event is a State object, parse it
            condition = filt_delta["end"].apply(lambda x: x.label) == end
            filt_delta = filt_delta.loc[condition]

        return filt_delta

    # TODO: Remove all the print functions  

    def print_x0(self):

        """
        Prints the list of initial states
        """

        in_states = [x.label for x in self.x0]
        print(in_states)

    def print_Xm(self):

        """
        Prints the list of final states
        """

        fin_states = [x.label for x in self.Xm]
        print(fin_states)

    def add_state(self, state, isInitial=None, isFinal=None):

        if isinstance(state, State):  # if state is an instance of State

            if state not in self.X:

                self.X.append(state)

                if state.isFinal:
                    self.Xm.append(state)

                if state.isInitial:
                    self.x0.append(state)

            else:

                print("Error: We cannot have two states with the same label")
                return

        elif isinstance(state, str):  # if state is a string

            if state not in [x.label for x in self.X]:

                new_state = State(state, isInitial, isFinal)
                self.X.append(new_state)

                if new_state.isFinal:
                    self.Xm.append(new_state)

                if new_state.isInitial:
                    self.x0.append(new_state)

            else:

                print("Error: We cannot have two states with the same label")
                return

        else:

            raise ValueError

    def add_event(self, event, isObservable=None, isControllable=None, isFault=None):
        """
        Args:
            event (Event): Event to be added to the FSA
            isObservable (bool, optional): Specifies if the event is observable. Defaults to None
            isControllable (bool, optional): Specifies if the event is controllable. Defaults to None
            isFault (bool, optional): Specifies if the event is aa fault event. Defaults to None
        """

        if isinstance(event, Event):  # if event is an instance of Event

            if event not in self.E:
                self.E.append(event)

            else:

                print("Error: We cannot have two states with the same label")
                return

        elif isinstance(event, str):  # if event is a string

            if event not in [x.label for x in self.E]:

                new_event = Event(event, isObservable, isControllable, isFault)
                self.E.append(new_event)

            else:

                print("Error: We cannot have two states with the same label")
                return

        else:

            raise ValueError

    def add_transition(self, initial_state, event, end_state):

        # Initial State

        try:

            if isinstance(initial_state, State):
                initial_state = initial_state.label

            idx = [x.label for x in self.X].index(initial_state)
            i_state = self.X[idx]

        except (ValueError, TypeError):

            print("Error: initial state not in X")
            return

        # Transition

        try:

            if isinstance(event, Event):
                event = event.label

            idx = [e.label for e in self.E].index(event)
            transition = self.E[idx]

        except (ValueError, TypeError):

            print("Error: event not in E")
            return

        # Final State

        try:

            if isinstance(end_state, State):
                end_state = end_state.label

            idx = [x.label for x in self.X].index(end_state)
            e_state = self.X[idx]

        except (ValueError, TypeError):

            print("Error: end state not in X")
            return

        temp_df = pd.DataFrame([[i_state, transition, e_state]], columns=["start", "transition", "end"])
        self.delta = pd.concat([self.delta, temp_df], axis=0, ignore_index=True)
