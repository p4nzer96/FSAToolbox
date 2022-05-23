from dataclasses import dataclass


@dataclass
class state:
    label: str = None
    isInitial: bool = None
    isFinal: bool = None
    isForbidden: bool = None

    def __repr__(self):
        return self.label

    def __eq__(self, other):
        return self.label == other.label
