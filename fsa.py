import json
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

        X = []
        E = []

        # File opening

        with open(filename) as jsonFile:
            jsonObject = json.load(jsonFile)

        # Reading states and properties

        for key in jsonObject['X']:
            st_label = key  # State name
            isInit = bool(jsonObject['X'][key]['isInit'])  # Is the state initial?
            isFinal = bool(jsonObject['X'][key]['isFinal'])  # Is the state final?

            X.append(State(st_label, isInit, isFinal))

        # Reading events and properties

        for key in jsonObject['E']:
            ev_label = key  # Event name
            observable = bool(jsonObject['E'][key]['isObservable'])  # Is observable?
            controllable = bool(jsonObject['E'][key]['isControllable'])  # Is controllable?
            fault = bool(jsonObject['E'][key]['isFault'])  # Is faulty?

            E.append(Event(ev_label, observable, controllable, fault))

        return cls(X, E)


'''
X=['x0','x1']
E=['a','b']
delta=[['x0','a','x1'],['x1','b','x0']]
x0='x0'
Xm=['x0']

fsa=FSA(X, E, delta, x0, Xm)

fsa.setObs(['a'])
fsa.setFaulty(['b'])
'''
