import json

class FSA():

    def __init__(self, X=None, E=None, delta=None, x0=None, Xm=None) -> None:

        self.X = X  # States
        self.E = E  # Alphabet
        self.delta = delta  # Delta relation
        self.x0 = x0  # Initial states
        self.Xm = Xm  # Final states

    @classmethod
    def fromfile(self, filename):

        # Load from file

    def _loaddata(self, X, E, delta, x0, Xm):

        # load data

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