from dataclasses import dataclass


@dataclass
class event:
    label: str = None
    isObservable: bool = None
    isControllable: bool = None
    isFault: bool = None

    def __repr__(self):
        return self.label

    def __eq__(self, other):
        return self.label == other.label
