from dataclasses import dataclass


@dataclass
class event:
    label: str = None
    isObservable: bool = None
    isControllable: bool = None
    isFault: bool = None

    def __hash__(self):
        return hash(self.label)

    def __repr__(self):
        return self.label

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
