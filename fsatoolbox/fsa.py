import json
import numpy as np
import pandas as pd
from tabulate import tabulate
from fsatoolbox import event, state
from fsatoolbox.utils import load_module


class StateNotFoundExc(Exception):
    pass


class EventNotFoundExc(Exception):
    pass


class TransitionNotFoundExc(Exception):
    pass


class fsa:
    """
    Class used to represent a Finite State Automaton (FSA)

    Parameters
    ----------
    X : list of State objects
        the set of states of which the automaton is composed
    E : list of event objects
        the alphabet of the automaton
    delta : DataFrame
        the transition relation / function of the automaton
    """

    def __init__(self, X=None, E=None, delta=pd.DataFrame(columns=["start", "transition", "end"]),
                 **kwargs) -> None:

        self._X = X if X else []  # States
        self._E = E if E else []  # Alphabet
        self._delta = delta  # Delta relation
        self._x0 = []  # Initial states
        self._Xm = []  # Final states

        self._update_fsa()  # Init fsa (set final and initial states)

        # Optional: Name of the FSA

        self._name = kwargs.get('name') if kwargs.get('name') else object.__repr__(self)

        # FSA properties

        self.is_Reachable = None
        self.is_co_Reachable = None
        self.is_Blocking = None
        self.is_Trim = None
        self.is_Reversible = None

    def __repr__(self):

        rep = "\nFSA: " + self._name + "\n" + self.showfsa()
        return rep

    @property
    def X(self):
        return self._X

    @X.setter
    def X(self, value):
        for x in value:
            if x in self._X:
                self.add_state(x)
            else:
                self.remove_state(x)

    @property
    def E(self):
        return self._E

    @E.setter
    def E(self, value):
        for e in value:
            if e not in self._E:
                self.add_event(e)
            else:
                self.remove_event(e)

    @property
    def delta(self):
        return self._delta

    @delta.setter
    def delta(self, value):
        self._delta = value

    @property
    def x0(self):
        return self._x0

    @property
    def Xm(self):
        return self._Xm

    @classmethod
    def from_file(cls, filename, **kwargs):

        """
        Generates a FSA from file

        Args:
            filename (str): the path of the .json file containing the definition of the FSA


        Returns:
            fsa: An instance of FSA

        """

        # Load from file

        X = []  # States
        E = []  # Alphabet
        x0 = []  # Initial states
        Xm = []  # Final states

        # File opening

        jsonObject = load_module.loadfile(filename)

        if jsonObject is None:
            raise TypeError

        # Reading states and properties

        state_properties = {"isInitial": None, "isFinal": None, "isForbidden": None}

        for state_name in jsonObject['X']:
            for prop in state_properties.keys():

                if prop in jsonObject['X'][state_name]:
                    state_properties[prop] = jsonObject['X'][state_name][prop]

            # Creating the state
            State = state(state_name,
                          state_properties["isInitial"],
                          state_properties["isFinal"],
                          state_properties["isForbidden"])

            if state_properties["isInitial"]:  # If the state is initial, add it to initial states
                x0.append(State)

            if state_properties["isFinal"]:  # If the state is final, add it to final states
                Xm.append(State)

            # Add the state to X
            X.append(State)

        event_properties = {"isObservable": None, "isControllable": None, "isFault": None}

        # Reading events and properties

        for event_name in jsonObject['E']:
            for prop in event_properties.keys():
                if prop in jsonObject['E'][event_name]:
                    event_properties[prop] = jsonObject['E'][event_name][prop]  # Is observable?

            # Creating the event
            Event = event(event_name,
                          event_properties["isObservable"],
                          event_properties["isControllable"],
                          event_properties["isFault"])

            E.append(Event)

        data = []

        # Reading delta

        for key in jsonObject['delta']:

            start_state = jsonObject['delta'][key]['start']  # Start state

            if start_state not in [s.label for s in X]:  # Check if start state is in X
                raise ValueError("Invalid start state")

            else:

                idx = [x.label for x in X].index(start_state)
                i_state = X[idx]

            transition = jsonObject['delta'][key]['event']  # Transition

            if transition not in [e.label for e in E]:  # Check if transition is in E
                raise ValueError("Invalid event")

            else:

                idx = [x.label for x in E].index(transition)
                trans = E[idx]

            end_state = jsonObject['delta'][key]['end']

            if end_state not in [s.label for s in X]:  # Check if end state is in X
                raise ValueError("Invalid end state")

            else:

                idx = [x.label for x in X].index(end_state)
                f_state = X[idx]

            data.append([i_state, trans, f_state])

        delta = pd.DataFrame(data, columns=["start", "transition", "end"])

        if kwargs.get("name"):
            fsa_name = kwargs.get("name")
            return cls(X, E, delta, name=fsa_name)

        return cls(X, E, delta)

    def to_file(self, filename):

        # Base dict structure
        fsa_dict = dict.fromkeys(["X", "E", "delta"])

        # Populating the states
        fsa_dict["X"] = dict.fromkeys([x.label for x in self.X])

        for x in self.X:

            state_properties = vars(x)
            dict_x = {}

            for prop in state_properties.keys():

                if state_properties[prop] is not None:
                    dict_x[str(prop)] = state_properties[prop]

            fsa_dict["X"][x.label] = dict_x

        fsa_dict["E"] = dict.fromkeys([e.label for e in self.E])

        # Events
        for e in self.E:

            event_properties = vars(e)
            dict_e = {}

            for prop in event_properties.keys():

                if event_properties[prop] is not None:
                    dict_e[str(prop)] = event_properties[prop]

            fsa_dict["E"][e.label] = dict_e

        # Delta
        fsa_dict["delta"] = dict.fromkeys(list(self.delta.index))

        for index, row in self.delta.iterrows():
            fsa_dict["delta"][index] = dict.fromkeys(["start", "event", "end"])

            fsa_dict["delta"][index]["start"] = row[0].label
            fsa_dict["delta"][index]["event"] = row[1].label
            fsa_dict["delta"][index]["end"] = row[2].label

        with open(filename, "w") as outfile:
            json.dump(fsa_dict, outfile, indent=4)

    def showfsa(self):

        """
        Shows a graphical representation of the FSA

        Returns:
            str: String that show the fsa structure

        """

        column_labels = ["X"] + [x.label for x in self.E]

        data = np.empty((len(self.X), len(self.E) + 1), dtype='U100')
        data[:, 0] = [x.label for x in self.X]

        event_table = np.empty((1, len(self.E)), dtype='U100')
        state_table = np.empty((1, len(self.X)), dtype='U100')

        for i, state in enumerate(self.X):
            for j, event in enumerate(self.E):

                filtered_events = self.filter_delta(state, event)['end'].values
                end_labels = [x.label for x in filtered_events]
                string = ""

                if not end_labels:
                    data[i, j + 1] = "-"
                    continue

                for end in end_labels:

                    if not string:

                        string += end

                    else:

                        string += ", " + end

                data[i, j + 1] = string

        # Populating the column representing the properties of the states

        # TODO: Trovare una soluzione più elegante

        for i, state in enumerate(self.X):

            props = ["isInitial", "isFinal", "isForbidden"]
            props_label = ["I", "F", "FR"]
            true_props_label = []

            state_attr = vars(state)

            for idx, prop in enumerate(props):
                if state_attr[prop]:
                    true_props_label.append(props_label[idx])

            if len(true_props_label) != 0:
                state_table[:, i] = ", ".join(true_props_label)

            else:
                state_table[:, i] = "-"

        # Populating the table representing the properties of the events

        for i, event in enumerate(self.E):

            string = ""

            if event.isObservable:
                string += "0"

            if event.isControllable:

                if string:
                    string += ", "

                string += "C"

            if event.isFault:

                if string:
                    string += ", "

                string += "F"

            if not string:

                event_table[:, i] = "-"

            else:

                event_table[:, i] = string

        table = tabulate(data, headers=column_labels, stralign="center", tablefmt='grid')
        event_properties = tabulate(event_table, headers=self.E, stralign="center", tablefmt='grid')
        state_properties = tabulate(state_table, headers=self.X, stralign="center", tablefmt='grid')

        text = "\nTable:\n" + \
               table + \
               "\n\nEvent Properties:\n" + \
               event_properties + \
               "\nLegend: O: Observable, C: Controllable, F: Fault\n\n" + \
               "State Properties:\n" + \
               state_properties + \
               "\nLegend: I: Initial, F: Final, FR: Forbidden\n "

        return text

    def filter_delta(self, start=None, transition=None, end=None):
        """
        Filters the delta by starting state, transition or ending state

        Args:
            start (state, optional): starting state. Defaults to None.
            transition (Event, optional): transition event. Defaults to None.
            end (Event, optional): ending state. Defaults to None.

        Returns:
            DataFrame: Filtered delta according to filter passed as argument of the function
        """

        filt_delta = self.delta

        if start:  # Starting state
            start = start.label if isinstance(start, state) else start  # If start is a State object, parse it
            condition = filt_delta["start"].apply(lambda x: x.label) == start
            filt_delta = filt_delta.loc[condition]

        if transition:  # Transition event
            transition = transition.label if isinstance(transition, event) else transition  # If transition is an Event
            # object, parse it
            condition = filt_delta["transition"].apply(lambda x: x.label) == transition
            filt_delta = filt_delta.loc[condition]

        if end:  # Ending state
            end = end.label if isinstance(end, state) else end  # If event is a state object, parse it
            condition = filt_delta["end"].apply(lambda x: x.label) == end
            filt_delta = filt_delta.loc[condition]

        return filt_delta

    def add_state(self, new_state, isInitial=None, isFinal=None, isForbidden=None):

        """
        Adds a state to the FSA

        Args:
            new_state (state): The new state to be added
            isInitial (bool, optional): determines if the state is initial
            isFinal (bool, optional): determines if the state is final
            isForbidden(bool, optional): determines if the state is forbidden
        """

        self._update_fsa()

        if isinstance(new_state, state):  # if state is an instance of state

            if new_state not in self.X:

                self.X.append(new_state)

                if new_state.isFinal:
                    self.Xm.append(new_state)

                if new_state.isInitial:
                    self.x0.append(new_state)

            else:

                print("Error: We cannot have two states with the same label")
                return

        elif isinstance(new_state, str):  # if state is a string

            if new_state not in [x.label for x in self.X]:

                new_state = state(new_state, isInitial, isFinal, isForbidden)
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

    def remove_state(self, state):

        state = self._state_parser(state)

        if state is None or state not in self.X:
            raise StateNotFoundExc("Error: state not in X")

        self._update_fsa()

        for x in self._X:
            if x == state:
                self._X.remove(x)

        if not self._delta.empty:
            self._delta.drop(self.delta[((self._delta.start == state) |
                                         (self._delta.end == state))].index, inplace=True)

    def change_state_props(self, state, **kwargs):

        state = self._state_parser(state)

        if state not in self._X:
            raise StateNotFoundExc(Exception)

        for prop in kwargs.keys():
            setattr(state, prop, kwargs[prop])

    def add_event(self, new_event, isObservable=None, isControllable=None, isFault=None):
        """
        Adds an event to the FSA

        Args:
            new_event (event): Event to be added to the FSA
            isObservable (bool, optional): Specifies if the event is observable. Defaults to None
            isControllable (bool, optional): Specifies if the event is controllable. Defaults to None
            isFault (bool, optional): Specifies if the event is aa fault event. Defaults to None
        """

        if isinstance(new_event, event):  # if event is an instance of Event

            if new_event not in self.E:
                self.E.append(new_event)

            else:

                print("Error: We cannot have two events with the same label")
                return

        elif isinstance(new_event, str):  # if event is a string

            if new_event not in [x.label for x in self.E]:

                new_event = event(new_event, isObservable, isControllable, isFault)
                self.E.append(new_event)

            else:

                print("Error: We cannot have two events with the same label")
                return

        else:

            raise ValueError

    def remove_event(self, event):
        """
        Removes an event or a list of events from the FSA
        Args:
            event (state):
        """

        event = self._event_parser(event)

        if event is None or event not in self.E:
            raise EventNotFoundExc("Error: event not in alphabet")

        self._update_fsa()

        for e in self._E:
            if e == event:
                self._E.remove(e)

        if not self._delta.empty:
            self._delta.drop(self.delta[(self._delta.transition == event)], inplace=True)

    def change_event_props(self, event, **kwargs):

        event = self._event_parser(event)

        if event not in self._E:
            raise EventNotFoundExc(Exception)

        for prop in kwargs.keys():
            setattr(event, prop, kwargs[prop])

    def add_transition(self, initial_state, tr_event, end_state):

        """
        Adds a transition to the delta relation/function

        Args:
            initial_state (state, optional): initial state
            tr_event (event, optional): transition
            end_state (state, optional): ending state

        Returns: DataFrame that contains the filtered data according to parameters

        """

        # Initial State

        try:

            if isinstance(initial_state, state):
                initial_state = initial_state.label

            idx = [x.label for x in self.X].index(initial_state)
            i_state = self.X[idx]

        except (ValueError, TypeError):

            print("Error: starting state not in X")
            return

        # Transition

        try:

            if isinstance(tr_event, event):
                tr_event = tr_event.label

            idx = [e.label for e in self.E].index(tr_event)
            transition = self.E[idx]

        except (ValueError, TypeError):

            print("Error: event not in E")
            return

        # Final State

        try:

            if isinstance(end_state, state):
                end_state = end_state.label

            idx = [x.label for x in self.X].index(end_state)
            e_state = self.X[idx]

        except (ValueError, TypeError):

            print("Error: end state not in X")
            return

        temp_df = pd.DataFrame([[i_state, transition, e_state]], columns=["start", "transition", "end"])
        self.delta = pd.concat([self.delta, temp_df], axis=0, ignore_index=True) \
            .drop_duplicates().reset_index(drop=True)

        self._update_fsa()

    def remove_transition(self, start, event, end):

        start = self._state_parser(start)
        event = self._event_parser(event)
        end = self._state_parser(end)

        transition = self.delta[((self._delta.start == start) &
                                 (self._delta.transition == event) &
                                 (self._delta.end == end))]

        if transition.empty():
            raise TransitionNotFoundExc("Error: transition not in delta")

        self._delta.drop(transition.index, inplace=True)

        self._update_fsa()

    # Internal Methods -------------------------------------------------------------

    def _state_parser(self, states):

        if isinstance(states, list):
            parsed_states = []
            for x in states:
                if isinstance(x, state):
                    parsed_states.append(x)
                elif isinstance(x, str):
                    for fsa_x in self.X:
                        if x == fsa_x.label:
                            parsed_states.append(fsa_x)
                else:
                    raise TypeError
            return parsed_states
        elif isinstance(states, str):
            for fsa_x in self.X:
                if states == fsa_x.label:
                    return fsa_x
        elif isinstance(states, state):
            return states
        else:
            raise TypeError

    def _event_parser(self, events):

        if isinstance(events, list):
            parsed_events = []
            for e in events:
                if isinstance(e, event):
                    parsed_events.append(e)
                elif isinstance(e, str):
                    for fsa_x in self.X:
                        if e == fsa_x.label:
                            parsed_events.append(fsa_x)
                else:
                    raise TypeError
            return parsed_events
        elif isinstance(events, str):
            for fsa_e in self.E:
                if events == fsa_e.label:
                    return fsa_e
        elif isinstance(events, event):
            return event
        else:
            raise TypeError

    def _update_fsa(self):

        for x in self._X:
            if x.isInitial is True and x not in self._x0:
                self._x0.append(x)
            elif x.isInitial is False and x in self._x0:
                self._x0.remove(x)

        for x in self._X:
            if x.isFinal is True and x not in self._Xm:
                self._Xm.append(x)
            elif x.isFinal is False and x in self._Xm:
                self._Xm.remove(x)

        self.is_Reachable = None
        self.is_co_Reachable = None
        self.is_Trim = None
        self.is_Blocking = None
        self.is_Reversible = None
