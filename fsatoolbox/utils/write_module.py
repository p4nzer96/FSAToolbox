import json

from fsatoolbox.utils.filter_delta import filter_delta


def save_json(filename, X, E, delta, name):
    # Base dict structure
    fsa_dict = dict.fromkeys(["X", "E", "delta"])

    # Populating the states
    fsa_dict["X"] = dict.fromkeys([x.label for x in X])

    for x in X:

        state_properties = ["isInitial", "isFinal"]
        dict_x = {}

        for prop in state_properties:

            if getattr(x, prop) is not None:
                dict_x[str(prop)] = getattr(x, prop)

        fsa_dict["X"][x.label] = dict_x

    # Events
    fsa_dict["E"] = dict.fromkeys([e.label for e in E])

    for e in E:

        event_properties = ["isObservable", "isControllable", "isFault"]
        dict_e = {}

        for prop in event_properties:

            if getattr(e, prop) is not None:
                dict_e[str(prop)] = getattr(e, prop)

        fsa_dict["E"][e.label] = dict_e

    # Delta
    fsa_dict["delta"] = dict.fromkeys(list(delta.index))

    for index, row in delta.iterrows():
        fsa_dict["delta"][index] = dict.fromkeys(["start", "event", "end"])

        fsa_dict["delta"][index]["start"] = row[0].label
        fsa_dict["delta"][index]["event"] = row[1].label
        fsa_dict["delta"][index]["end"] = row[2].label

    fsa_dict["name"] = name

    with open(filename, "w") as outfile:
        json.dump(fsa_dict, outfile, indent=4)


def save_txt(filename, X, E, delta):
    n_states = str(len(X))
    padding = max([len(x.label) for x in X]) + 4

    with open(filename, "w") as f:

        f.write(n_states)
        f.write("\n\n")

        event_dict = {}

        for event in E:

            if event.isControllable is True:
                controllable = "c"
            elif event.isControllable is False:
                controllable = "uc"
            else:
                controllable = "c"  # default fallback

            if event.isObservable is True:
                observable = "o"
            elif event.isObservable is False:
                observable = "uo"
            else:
                observable = "o"  # default fallback

            if event.isFault is True:
                fault = "f"
            elif event.isFault is False:
                fault = "uf"
            else:
                fault = "uf"  # default fallback

            event_dict[event] = {"isControllable": controllable, "isObservable": observable, "isFault": fault}

        for state in X:

            label = state.label
            initial_str = str(int(state.isInitial))
            final_str = str(int(state.isFinal))

            f.write("{label:<{width}}{initial_str:<{width}}{final_str:<{width}}\n"
                    .format(label=label, initial_str=initial_str, final_str=final_str, width=padding))
            # f.write(f'{label:<10}{initial_str:<10}{final_str:<10}\n')

            f_delta = filter_delta(delta, start=state)

            for _, trans in f_delta.iterrows():
                event = trans["transition"]

                e_label = event.label

                e_dict = event_dict[event]

                c_value = e_dict["isControllable"]
                o_value = e_dict["isObservable"]
                f_value = e_dict["isFault"]

                state = trans["end"]
                s_label = state.label

                for value in [e_label, s_label, c_value, o_value, f_value]:
                    if value:
                        f.write("{value:<{width}}".format(value=value, width=padding))
                        # f.write(f'{value:<10}')

                f.write("\n")
            f.write("\n")
