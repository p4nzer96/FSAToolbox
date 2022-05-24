import json
import numpy as np
import pandas as pd
from tabulate import tabulate
from fsatoolbox import event, state


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

        with open(filename) as jsonFile:
            jsonObject = json.load(jsonFile)

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
            return cls(X, E, delta, x0, Xm, name=fsa_name)

        return cls(X, E, delta, x0, Xm)

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

    def showfsa(self, ui_mode=False, **kwargs):

        """
        Shows a graphical representation of the FSA

        Args:
            ui_mode (bool): If True, plot the FSA in UI

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

        for i, state in enumerate(self.X):

            if state.isFinal and state.isInitial:
                state_table[:, i] = "I, F"

            elif state.isFinal and not state.isInitial:
                state_table[:, i] = "F"

            elif not state.isFinal and state.isInitial:
                state_table[:, i] = "I"

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
               "\nLegend: I: Initial, F: Final\n "

        return text

    def __repr__(self):

        rep = self.name + "\n" + self.showfsa()
        return rep

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

                new_state = state(new_state, isInitial, isFinal)
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
        self.delta = pd.concat([self.delta, temp_df], axis=0, ignore_index=True)
