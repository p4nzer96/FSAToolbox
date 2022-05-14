from dataclasses import dataclass


@dataclass
class event:
    label: str = None
    isObservable: bool = True
    isControllable: bool = True
    isFault: bool = False

    def __repr__(self):
        return self.label

    def __eq__(self, other):
        return self.label == other.label
