class State():

    def __init__(self, label=None, initial=False, final=False) -> None:
        self.label = label
        self.isInitial = initial
        self.isFinal = final

    # TODO: Setter da riscrivere
    
    def __repr__(self):
        
        return self.label
    
    def getLabel(self):

        if not self.label:

            print("Label not yet set")

        else:

            return self.label

    '''
    def setLabel(self, label):

        if isinstance(label, str):

            self.label = label

        else:

            print("Incorrect data type: the label must be a string")
            
    '''

    def getFinal(self):

        return self.isFinal

    '''

    def setFinal(self, state, isFinal):

        self.isFinal = isFinal
        
    '''

    def getInitial(self):

        return self.isInitial

    '''

    def setInitial(self, state, initial):

        self.isInitial = initial

    '''

    def __eq__(self, other):
        return self.label == other.label