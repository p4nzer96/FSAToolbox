import json
import pandas as pd
from event import Event
from state import State


class FSA:

    def __init__(self, X=None, E=None, delta=None, x0=None, Xm=None) -> None:

        self.X = X  # States
        self.E = E  # Alphabet
        self.delta = delta  # Delta relation
        self.x0 = x0  # Initial states
        self.Xm = Xm  # Final states

    @classmethod
    def fromfile(cls, filename):

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
            
            if('isInit' in jsonObject['X'][key]):
                isInit = bool(jsonObject['X'][key]['isInit'])  # Is the state initial?
            else:
                isInit = None
            if('isFinal' in jsonObject['X'][key]):
                isFinal = bool(jsonObject['X'][key]['isFinal'])  # Is the state final?
            else:
                isFinal = None

            state = State(st_label, isInit, isFinal)

            if isInit:  # If the state is initial, add it to initial states
                x0.append(state)

            if isFinal:  # If the state is final, add it to final states
                Xm.append(state)
            X.append(state)

        # Reading events and properties

        for key in jsonObject['E']:
            ev_label = key  # Event name

            if('isObservable' in jsonObject['E'][key]):
                observable = bool(jsonObject['E'][key]['isObservable'])  # Is observable?
            else:
                observable = None
            if('isControllable' in jsonObject['E'][key]):
                controllable = bool(jsonObject['E'][key]['isControllable'])  # Is controllable?
            else:
                controllable = None
            if('isFaulty' in jsonObject['E'][key]):
                fault = bool(jsonObject['E'][key]['isFault'])  # Is faulty?
            else:
                fault = None

            E.append(Event(ev_label, observable, controllable, fault))

        data = []

        # Reading delta

        for key in jsonObject['delta']:

            start_state = jsonObject['delta'][key]['start']  # Start state

            if start_state not in [s.label for s in X]:  # Check if start state is in X
                raise ValueError("Invalid start state")

            transition = jsonObject['delta'][key]['name']  # Transition

            if transition not in [e.label for e in E]:  # Check if transition is in E
                raise ValueError("Invalid event")

            end_state = jsonObject['delta'][key]['ends']

            if end_state not in [s.label for s in X]:  # Check if end state is in X
                raise ValueError("Invalid end state")

            data.append([start_state, transition, end_state])

        delta = pd.DataFrame(data, columns=list(jsonObject['delta'].keys()))

        return cls(X, E, delta, x0, Xm)
