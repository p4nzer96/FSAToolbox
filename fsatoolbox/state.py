from dataclasses import dataclass


@dataclass
class state:
    label: str = None
    isInitial: bool = None
    isFinal: bool = None
    isForbidden: bool = None

    # added by me ******************************************************************************************************
    is_Reachable: bool = None     # (1)yes/(0)no
    is_co_Reachable: bool = None     # (1)yes/(0)no
    is_Blocking: bool = None     # (1)yes/(0)no
    is_Dead: bool = None     # (1)yes/(0)no
    is_co_Reachable_to_x0: bool = None     # (1)yes/(0)no

    def __repr__(self):
        return self.label

    # added by me ******************************************************************************************************
    def __eq__(self, other):
        return self.label == other.label
