class State():

    def __init__(self, label=None, initial=False, final=False) -> None:

        self.label = self.setLabel(label)
        self.isInitial = self.setInitial(initial)
        self.isFinal = self.setFinal(final)

    def getLabel(self):

        if not self.label:

            print ("Label not yet set")

        else:

            return self.label

    def setLabel(self, label):

        if (isinstance(label, str)):

            self.label = label

        else:

            print("Incorrect data type: the label must be a string")

    def getFinal(self):

        return self.isFinal

    def setFinal(self, isFinal):

        self.isFinal = isFinal

    def getInitial(self):

        return self.isInitial

    def setInitial(self, initial):

        self.isInitial = initial

    
