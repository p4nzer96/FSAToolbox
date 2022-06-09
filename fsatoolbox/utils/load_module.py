import os
import json


def loadfile(filename):
    if os.path.isfile(filename):
        extension = os.path.splitext(filename)

        if ".txt" in extension:
            data = load_txt(filename)
        elif ".json" in extension or ".fsa" in extension:
            data = load_json(filename)
        else:
            raise ValueError("File format not recognized")

        return data


def load_json(filename):
    with open(filename) as file:
        data = json.load(file)

    return data


def load_txt(filename):
    def parse_states(line, fsa_dict):

        state_attrs = line.split()

        # Parsing state attributes

        fsa_dict['X'][state_attrs[0]] = {'isInitial': bool(eval(state_attrs[1])),
                                         'isFinal': bool(eval(state_attrs[2])),
                                         'isForbidden': bool(eval(state_attrs[3]))}

    def parse_transitions(current_state, line, fsa_dict):
        ev_trans = line.split()

        # Parsing events and transitions

        if ev_trans[0] not in fsa_dict['E']:
            fsa_dict['E'][ev_trans[0]] = {}  # Add event to alphabet

            # Is the event controllable?

            if ev_trans[2] == "c":
                fsa_dict['E'][ev_trans[0]]['isControllable'] = True
            elif ev_trans[2] == "uc":
                fsa_dict['E'][ev_trans[0]]['isControllable'] = False
            else:
                raise ValueError

            # Is the event observable?

            if ev_trans[3] == "o":
                fsa_dict['E'][ev_trans[0]]['isObservable'] = True
            elif ev_trans[3] == "uo":
                fsa_dict['E'][ev_trans[0]]['isObservable'] = False
            else:
                raise ValueError

            # Is the event faulty?

            if ev_trans[4] == "f":
                fsa_dict['E'][ev_trans[0]]['isFaulty'] = True
            elif ev_trans[4] == "uf":
                fsa_dict['E'][ev_trans[0]]['isFaulty'] = False
            else:
                raise ValueError

        # Add state to the dict

        fsa_dict['delta'][len(fsa_dict['delta'])] = {"start": current_state, "event": ev_trans[0], "end": ev_trans[1]}

    # Open .txt file

    fd = open(filename, "r")

    fsa_dict = {"X": {}, "E": {}, "delta": {}}

    first_line = True  # I'm reading the first line of the file?
    parse_state = True  # I'm a parsing a state (if false I'm parsing an event)
    current_state = ''  # Represents the last state parsed

    for line in fd:

        if not line.strip():
            parse_state = True
            continue

        # Parsing the first line (get the number of states)

        if first_line:
            assert line.strip().isdigit() == True
            n_states = int(line.strip())
            first_line = False
            continue

        # Parsing a state / event

        if parse_state:
            parse_states(line, fsa_dict)
            current_state = line.split()[0]
            parse_state = False
        else:
            parse_transitions(current_state, line, fsa_dict)

    assert n_states == len(fsa_dict['X'])
    # json_object = json.dumps(fsa_dict, indent=4)

    fd.close()

    return fsa_dict
