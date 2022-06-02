import re


def load_txt_or_fsa(filename=None):
    """Parse the .txt file describing the fsa and it returns a json dictionary of the fsa"""

    jsonObject = {"X": {}, "E": {}, "delta": {}}

    fd = open(filename, mode='rt')
    # bytes_file_content = fd.read()

    lines = fd.readlines()

    clean_lines = []

    #print("lines: ", lines)
    for iter_list in range(len(lines)):
        clean_lines.append(lines[iter_list])

        clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")

        clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])

        #print("clean_lines[" + str(iter_list) + "]: " + str(clean_lines[iter_list]))
        clean_lines[iter_list] = clean_lines[iter_list].split(" ")

    fd.close()

    dict_start_states = {}  # to populate column 0 with keys (states), and for every key a dictionary of info on isInitial, isFinal, isFault
    list_start_states = []  # the indexes of the list represent the row of the related the start_state value
    num_states = 1
    list_events = []  # to populate columnlabels with keys (events), and for every key a dictionary of info on isObservable, isControllable

    # print("clean_lines: ", clean_lines)
    num_states = int(clean_lines[0][0])
    #print("num_states: ", num_states)

    dict_events = {}
    dict_deltas = {}

    index_row_start_states = 0
    index_column_events = 1  # the index '0' is for the column "States", so the events start from column '1'
    index_delta_events = 0
    current_start_state = ""
    current_event = ""
    flag_the_next_line_is_a_state = 0
    iter_lines = 1
    # for iter_lines in range(1, len(clean_lines)-2):
    while iter_lines < len(clean_lines):
        #print("clean_lines[" + str(iter_lines) + "][0] = '" + clean_lines[iter_lines][0] + "'")
        if clean_lines[iter_lines][0] == '' and flag_the_next_line_is_a_state == 0:
            if len(dict_start_states) < num_states:
                #print("''")
                flag_the_next_line_is_a_state = 1
                iter_lines += 1
                #print("iter_lines: ", iter_lines)
            else:
                break  # all the states and their deltas have been parsed, but there are other blak lines after
        elif flag_the_next_line_is_a_state == 1:
            #print("state")
            current_start_state = str(clean_lines[iter_lines][0])
            dict_start_states.update({current_start_state: {"isInitial": int(clean_lines[iter_lines][1]),
                                                            "isFinal": int(clean_lines[iter_lines][2]),
                                                            "isForbidden": int(clean_lines[iter_lines][3])}})
            list_start_states.append(current_start_state)
            index_row_start_states += 1
            flag_the_next_line_is_a_state = 0
            iter_lines += 1
            #print("dict_start_states: ", dict_start_states)
            #print("iter_lines: ", iter_lines)
        elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0:
            #print("name")
            flag_end_current_start_state = 0
            current_event = clean_lines[iter_lines][0]
            while flag_end_current_start_state == 0:
                #print("current_event: ", clean_lines[iter_lines][0])
                if clean_lines[iter_lines][0] not in dict_events:
                    #print("first time event")
                    bool_Controllable = 0
                    bool_Observable = 0
                    bool_Fault = 0
                    if clean_lines[iter_lines][2] == "c":
                        bool_Controllable = 1
                    elif clean_lines[iter_lines][2] == "uc":
                        bool_Controllable = 0

                    if clean_lines[iter_lines][3] == "o":
                        bool_Observable = 1
                    elif clean_lines[iter_lines][3] == "uo":
                        bool_Observable = 0

                    if clean_lines[iter_lines][4] == "f":
                        bool_Fault = 1
                    elif clean_lines[iter_lines][4] == "uf":
                        bool_Fault = 0

                    dict_events.update({clean_lines[iter_lines][0]: {"isControllable": bool_Controllable,
                                                                     "isObservable": bool_Observable,
                                                                     "isFault": bool_Fault}})
                    list_events.append(clean_lines[iter_lines][0])
                    dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                  "name": clean_lines[iter_lines][0],
                                                                  "ends": clean_lines[iter_lines][1]}})
                    index_column_events += 1
                    index_delta_events += 1
                    #print("index_delta_events: ", index_delta_events)
                    #print("dict_events: ", dict_events)
                else:

                    dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                  "name": clean_lines[iter_lines][0],
                                                                  "ends": clean_lines[iter_lines][1]}})
                    index_delta_events += 1
                    #print("index_delta_events: ", index_delta_events)

                if (iter_lines + 1) < len(clean_lines) and clean_lines[iter_lines + 1][0] != '':
                    #print("again")
                    iter_lines += 1  # reiteration of while flag_end_current_start_state == 0:
                    #print("iter_lines: ", iter_lines)
                    flag_the_next_line_is_a_state = 0
                else:
                    #print("exit while loop")
                    iter_lines += 1  # reiteration of while iter_lines < len(clean_lines):
                    flag_end_current_start_state = 1  # exit from the while loop
                    flag_the_next_line_is_a_state = 0

    jsonObject["X"].update(dict_start_states)
    jsonObject["E"].update(dict_events)
    jsonObject["delta"].update(dict_deltas)

    #print("from txt to jsonobject:", jsonObject)
    return jsonObject


def load_csv(filename=None):
    """Parse the .csv file describing the fsa and it returns a json dictionary of the fsa"""

    with open(filename, encoding='utf-8') as csvf:
        fd = open(filename, mode='rt')
        lines = fd.readlines()

    # print(lines)

    clean_lines = []

    #print("lines: ", lines)
    for iter_list in range(len(lines)):
        clean_lines.append(lines[iter_list])

        clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")

        clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])

        #print("clean_lines[" + str(iter_list) + "]: " + str(clean_lines[iter_list]))
        clean_lines[iter_list] = clean_lines[iter_list].split(",")

    # list_states = clean_lines[0][1:len(clean_lines[0])]
    fd.close()

    # print clean_lines
    for row in range(1, len(clean_lines)):
        for col in range(0, len(clean_lines[0])):
            #print("(row, col): ("+str(row)+","+str(col)+")"+": "+str(clean_lines[row][col]))
            pass

    jsonObject = {"X": {}, "E": {}, "delta": {}}
    dict_X = {}
    dict_E = {}
    dict_delta = {}
    # events properties, row 0
    list_columns = []

    i = 1
    for i in range(1, len(clean_lines[0])):
        current_event = clean_lines[0][i]
        if clean_lines[0][i] and clean_lines[0][i] != '_':
            if current_event.endswith("_uc_f_uo") or current_event.endswith("_uc_uo_f") or current_event.endswith(
                    "_f_uc_uo") or current_event.endswith("_f_uo_uc") or current_event.endswith(
                "_uo_f_uc") or current_event.endswith("_uo_uc_f"):
                string_lenght = len(current_event)
                substring_to_remove = current_event[-6:]
                current_event = current_event.replace(str(substring_to_remove), "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_f"):
                current_event = current_event.replace("_uc_f", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_f_uc"):
                current_event = current_event.replace("_f_uc", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_uo"):
                current_event = current_event.replace("_uc_uo", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_uc"):
                current_event = current_event.replace("_uo_uc", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_f"):
                current_event = current_event.replace("_uo_f", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_f_uo"):
                current_event = current_event.replace("_f_uo", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uc"):
                current_event = current_event.replace("_uc", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_f"):
                current_event = current_event.replace("_f", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uo"):
                current_event = current_event.replace("_uo", "")
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 0}})
            else:
                current_event.replace(" ", "")
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 0}})
            #print("current_event: ", current_event)
            list_columns.append(current_event)

    current_state = ""
    iter_ascii_delta = 65  # decimal value of the ASCII character 'A'
    num_rows = len(clean_lines)
    num_cols = len(clean_lines[0])
    for iter_row in range(1, num_rows):
        for iter_col in range(num_cols):
            # print("iter_row,iter_col:" + str(iter_row) + "," + str(iter_col))
            if clean_lines[iter_row][iter_col] != None:
                current_cell = clean_lines[iter_row][iter_col]
                # print("current_cell: ", current_cell)
                if iter_col == 0:
                    if current_cell[0] and current_cell[0] != '_':
                        if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                            "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                            string_lenght = len(current_cell)
                            substring_to_remove = current_cell[-6:]
                            current_state = current_cell.replace(str(substring_to_remove), "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_i_f"):
                            current_state = current_cell.replace("_i_f", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_f_i"):
                            current_state = current_cell.replace("_f_i", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_i_p"):
                            current_state = current_cell.replace("_i_p", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                        elif current_cell.endswith("_p_i"):
                            current_state = current_cell.replace("_p_i", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                        elif current_cell.endswith("_p_f"):
                            current_state = current_cell.replace("_p_f", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_f_p"):
                            current_state = current_cell.replace("_f_p", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_i"):
                            current_state = current_cell.replace("_i", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 0}})
                        elif current_cell.endswith("_f"):
                            current_state = current_cell.replace("_f", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_p"):
                            current_state = current_cell.replace("_p", "")
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 1}})
                        else:
                            current_state = current_cell
                            current_state.replace(" ", "")
                            dict_X.update(
                                {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 0}})
                    else:
                         # TODO: make a try except in this if-else
                         print("cell(" + str(iter_row) + "," + str(iter_col) + " is not a valid name for a state.\nPlease insert a valid one.")
                else:
                    current_delta_ends = current_cell.split("-")
                    flag_end_while = 0
                    while (flag_end_while == 0):
                        if '' in current_delta_ends:
                            current_delta_ends.remove('')
                        else:
                            flag_end_while = 1

                    for i in range(len(current_delta_ends)):
                        dict_delta.update({str(chr(iter_ascii_delta)): {"start": str(current_state), "name": list_columns[iter_col-1], "ends": str(current_delta_ends[i])}})
                        # print("dict_delta", dict_delta)
                        current_key_event = clean_lines[iter_row][iter_col]
                        iter_ascii_delta += 1

                    # print(current_delta_ends)
            else:
                pass

    jsonObject["X"] = dict_X
    jsonObject["delta"] = dict_delta
    jsonObject["E"] = dict_E
    # print(jsonObject)

    return jsonObject

