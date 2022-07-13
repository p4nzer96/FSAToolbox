import os
import json
import pandas as pd


def loadfile(filename):
    if os.path.isfile(filename):
        extension = os.path.splitext(filename)

        if ".txt" in extension:
            data = load_txt(filename)
        elif ".json" in extension or ".fsa" in extension:
            data = load_json(filename)
        elif ".csv" in extension:
            data = load_csv(filename)
        else:
            raise ValueError("File format not recognized")

        return data


def load_json(filename):
    with open(filename) as file:
        data = json.load(file)

    return data


def load_txt(filename):
    def parse_states(txt_line, fsa_dictionary):

        state_attrs = txt_line.split()

        # Parsing state attributes

        fsa_dictionary['X'][state_attrs[0]] = {'isInitial': bool(eval(state_attrs[1])),
                                               'isFinal': bool(eval(state_attrs[2]))}

    def parse_transitions(curr_state, txt_line, fsa_dictionary):
        ev_trans = txt_line.split()

        # Parsing events and transitions

        if ev_trans[0] not in fsa_dictionary['E']:
            fsa_dictionary['E'][ev_trans[0]] = {}  # Add event to alphabet

            # Is the event controllable?

            if "c" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isControllable'] = True
            elif "uc" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isControllable'] = False
            else:
                pass

            # Is the event observable?

            if "o" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isObservable'] = True
            elif "uo" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isObservable'] = False
            else:
                pass

            # Is the event faulty?

            if "f" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isFaulty'] = True
            elif "uf" in ev_trans:
                fsa_dictionary['E'][ev_trans[0]]['isFaulty'] = False
            else:
                pass

        # Add state to the dict

        fsa_dictionary['delta'][len(fsa_dictionary['delta'])] = {"start": curr_state, "event": ev_trans[0],
                                                                 "end": ev_trans[1]}

    # Open .txt file

    fd = open(filename, "r")

    fsa_dict = {"X": {}, "E": {}, "delta": {}}

    n_states = None

    first_line = True  # I'm reading the first line of the file?
    parse_state = True  # I'm a parsing a state (if false I'm parsing an event)
    current_state = ''  # Represents the last state parsed

    for line in fd:

        if not line.strip():
            parse_state = True
            continue

        # Parsing the first line (get the number of states)

        if first_line:
            assert line.strip().isdigit() is True
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

    fd.close()

    return fsa_dict


def load_csv(filename):
    jsonObject = {"X": {}, "E": {}, "delta": {}}

    data = pd.read_csv(filename).fillna("")

    # States

    for i, row in data.iterrows():
        x = str(row[0]).split("_")

        # Initial States

        if "i" in x:
            is_initial = True
            x.remove("i")
        else:
            is_initial = False

        # Final States

        if "f" in x:
            is_final = True
            x.remove("f")
        else:
            is_final = False

        state = "_".join(x)

        jsonObject['X'][state] = {'isInitial': is_initial,
                                  'isFinal': is_final}
        data.values[i, 0] = state

    events = []

    # Events

    for event in data.columns[1:]:

        e = str(event).split("_")

        # Event is observable?

        if "uo" in e:
            is_observable = False
            e.remove("uo")
        else:
            is_observable = True

        # Event is controllable?

        if "uc" in e:
            is_controllable = False
            e.remove("uc")
        else:
            is_controllable = True

        # Event is fault?

        if "f" in e:
            is_fault = True
            e.remove("f")
        else:
            is_fault = False

        event_str = "_".join(e)

        jsonObject['E'][event_str] = {'isObservable': is_observable,
                                      'isControllable': is_controllable,
                                      'isFault': is_fault}
        events.append(event_str)

    data.columns = ['State'] + events

    # Transitions

    count = 0
    for i in range(data.shape[0]):
        initial_state = data.values[i, 0]
        for j in range(1, data.shape[1]):
            event = data.columns[j]
            if data.values[i, j] != "":
                for end_state in str(data.values[i, j]).split("-"):
                    jsonObject['delta'][count] = {"start": initial_state,
                                                  "event": event,
                                                  "end": end_state}
                    count += 1

    return jsonObject
