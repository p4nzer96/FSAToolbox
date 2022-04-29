class Event:

    def __init__(self, label=None, isObservable=True, isControllable=True, isFault=False) -> None:

        self.label = label
        self.isObservable = isObservable
        self.isControllable = isControllable
        self.isFault = isFault

    # TODO: Setter da riscrivere
    
    def __repr__(self):
        
        return self.label

    def getLabel(self):

        if not self.label:

            print("Label not yet set")

        else:

            return self.label

    '''def setLabel(self, label):

        if isinstance(label, str): 
        
            self.label = label'''

    def getObservable(self):

        return self.isObservable

    '''def setObservable(self, observable):

        self.isObservable = observable'''

    def getControllable(self):

        return self.isControllable

    '''def setControllable(self, controllable):

        self.isControllable = controllable'''

    def getFault(self):

        return self.isFault

    '''def setFault(self, fault):

        self.isFault = fault'''
