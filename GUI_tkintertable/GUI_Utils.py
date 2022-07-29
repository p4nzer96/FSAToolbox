import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, ttk, Tk, Label, Toplevel, Button, Text, BOTH, \
    StringVar
from tkinter.ttk import Frame
<<<<<<< HEAD
from loadfsa_GUI import *
import re
from tkinter.ttk import Combobox

=======

import re
from tkinter.ttk import Combobox


>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
dictcolObservableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolControllableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolFaultyEvents = {'event1': 0, 'event2': 0, 'event3': 0, 'event4': 0}

last_sheet = "Sheet1"
<<<<<<< HEAD
last_extension = ""
num_rows_to_add = 0

def setEventAsUnobservable(MyTable, column_name=None):
    """Set the event as Unobservable - can be used in a table header"""
    #print("setEventAsUnobservable")
=======

def setEventAsUnobservable(MyTable, column_name=None):
    """Set the event as Unobservable - can be used in a table header"""
    # print("setEventAsUnobservable")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolObservableEvents
    if column_name is None:
        n = messagebox.askyesno("Setting",
                                "Unobservable Event?")
        if n:
<<<<<<< HEAD
=======

>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolObservableEvents[str(current_col_name)] = 0
    else:
        dictcolObservableEvents[str(column_name)] = 0

<<<<<<< HEAD

def setEventAsObservable(MyTable, column_name=None):
    """Set the event as Observable - can be used in a table header"""
    #print("setEventAsObservable")
=======
def setEventAsObservable(MyTable, column_name=None):
    """Set the event as Observable - can be used in a table header"""
    # print("setEventAsObservable")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolObservableEvents
    if column_name is None:

        n = messagebox.askyesno("Setting",
                                "Observable Event?")
        if n:
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolObservableEvents[str(current_col_name)] = 1
    else:
        dictcolObservableEvents[str(column_name)] = 1

<<<<<<< HEAD

def setEventAsUncontrollable(MyTable, column_name=None):
    """Set the event as Uncontrollable - can be used in a table header"""
    #print("setEventAsUncontrollable")
=======
def setEventAsUncontrollable(MyTable, column_name=None):
    """Set the event as Uncontrollable - can be used in a table header"""
    # print("setEventAsUncontrollable")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolControllableEvents

    if column_name is None:

        n = messagebox.askyesno("Setting",
                                "Uncontrollable Event?")
        if n:
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolControllableEvents[str(current_col_name)] = 0
    else:
        dictcolControllableEvents[str(column_name)] = 0

<<<<<<< HEAD

def setEventAsControllable(MyTable, column_name=None):
    """Set the event as Controllable - can be used in a table header"""
    #print("setEventAsControllable")
=======
def setEventAsControllable(MyTable, column_name=None):
    """Set the event as Controllable - can be used in a table header"""
    # print("setEventAsControllable")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolControllableEvents

    if column_name is None:

        n = messagebox.askyesno("Setting",
                                "Controllable Event?")
        if n:
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolControllableEvents[str(current_col_name)] = 1
    else:
        dictcolControllableEvents[str(column_name)] = 1

<<<<<<< HEAD

def setEventAsFaulty(MyTable, column_name=None):
    """Set the event as Faulty - can be used in a table header"""
    #print("setEventAsFaulty")
=======
def setEventAsFaulty(MyTable, column_name=None):
    """Set the event as Faulty - can be used in a table header"""
    # print("setEventAsFaulty")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolFaultyEvents

    if column_name is None:
        n = messagebox.askyesno("Setting",
                                "Faulty Event?")
        if n:
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolFaultyEvents[str(current_col_name)] = 1
    else:
        dictcolFaultyEvents[str(column_name)] = 1

<<<<<<< HEAD

def setEventAsUnfaulty(MyTable, column_name=None):
    """Set the event as Unfaulty - can be used in a table header"""
    #print("setEventAsUnfaulty")
=======
def setEventAsUnfaulty(MyTable, column_name=None):
    """Set the event as Unfaulty - can be used in a table header"""
    # print("setEventAsUnfaulty")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolFaultyEvents

    if column_name is None:

        n = messagebox.askyesno("Setting",
                                "Observable Event?")
        if n:
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolFaultyEvents[str(current_col_name)] = 0
    else:
        dictcolFaultyEvents[str(column_name)] = 0

<<<<<<< HEAD

def fromTableToJson(MyTable):
    """Convert the current table content into a Json file"""
    #print("fromTableToJson")
=======
def fromTableToJson(MyTable):
    """Convert the current table content into a Json file"""
    # print("fromTableToJson")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
    global dictcolControllableEvents
    global dictcolObservableEvents
    global dictcolFaultyEvents

<<<<<<< HEAD
    # n = messagebox.askyesno("Convert", "Convert table to json file?", parent=MyTable.parentframe)
    # if n:

    print("Converting the table to the file '.\json_table\description_table.json' ...")


    flag_more_than_one_same_state = 0  # when has been specified the same state more times
    flag_more_than_one_same_event = 0  # when has been specified the same event more times

    #print("MyTable.currenttable.model.columnlabels: ", MyTable.currenttable.model.columnlabels)
    list_columnlabels = list(MyTable.currenttable.model.columnlabels.values())
    for i in range(len(list_columnlabels)):
        # print("list_columnlabels[{}]: " .format(i) + list_columnlabels[i])
        if list_columnlabels.count(list_columnlabels[i]) > 1:
            flag_more_than_one_same_event = 1


    # print("columnlabels:", MyTable.currenttable.model.columnlabels.values())

    list_events = []
    for i in range(1, len(list_columnlabels)):
        #print("i: ", i)
        curr_event = list_columnlabels[i]
        if curr_event.endswith("_uc_f_uo") or curr_event.endswith("_uc_uo_f") or curr_event.endswith(
                "_f_uc_uo") or curr_event.endswith("_f_uo_uc") or curr_event.endswith(
            "_uo_f_uc") or curr_event.endswith("_uo_uc_f"):
            substring_to_remove = curr_event[-8:]
            curr_event = curr_event.replace(str(substring_to_remove), "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uc_f"):
            curr_event = curr_event.replace("_uc_f", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_f_uc"):
            curr_event = curr_event.replace("_f_uc", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uc_uo"):
            curr_event = curr_event.replace("_uc_uo", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uo_uc"):
            curr_event = curr_event.replace("_uo_uc", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uo_f"):
            curr_event = curr_event.replace("_uo_f", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_f_uo"):
            curr_event = curr_event.replace("_f_uo", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uc"):
            curr_event = curr_event.replace("_uc", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_f"):
            curr_event = curr_event.replace("_f", "")
            re.sub(" +", "", curr_event)
        elif curr_event.endswith("_uo"):
            curr_event = curr_event.replace("_uo", "")
            re.sub(" +", "", curr_event)
        else:
            re.sub(" +", "", curr_event)

        if curr_event in list_events:
            flag_more_than_one_same_event = 1
            print(
                "Syntax error:\t\t\t\t\t\t\tThe event '{}' must be defined only once (only one column per event), instead more have been found.".format(
                    curr_event))
        list_events.append(curr_event)

    flag_empty_state = 0
    list_rows_empty_states = []

    json_dict = {"X": {}, "E": {}, "delta": {}}
    dict_X = {}
    dict_E = {}
    dict_delta = {}
    current_state = ""
    iter_delta_key = 0
    num_rows = MyTable.currenttable.model.getRowCount()
    num_cols = len(MyTable.currenttable.model.columnlabels)
    for iter_row in range(num_rows):
        for iter_col in range(num_cols):
            # print("iter_row,iter_col:" + str(iter_row) + "," + str(iter_col))
            if MyTable.currenttable.model.getCellRecord(iter_row, iter_col) is not None:
                current_cell = MyTable.currenttable.model.getCellRecord(iter_row, iter_col)
                # print("current_cell: ", current_cell)
                if iter_col == 0:
                    temp_current_cell = re.sub(" +", "", current_cell)
                    # print("iter_row={} --> temp_current_cell={}" .format(iter_row+1, temp_current_cell))
                    if temp_current_cell and temp_current_cell != '_' and temp_current_cell != '':
                        if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                            "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                            substring_to_remove = current_cell[-6:]
                            current_state = current_cell.replace(str(substring_to_remove), "")
                            re.sub(" +", "", current_state)
                            # print("current_state: ", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_i_f"):
                            current_state = current_cell.replace("_i_f", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_f_i"):
                            current_state = current_cell.replace("_f_i", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_i_p"):
                            current_state = current_cell.replace("_i_p", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                        elif current_cell.endswith("_p_i"):
                            current_state = current_cell.replace("_p_i", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                        elif current_cell.endswith("_p_f"):
                            current_state = current_cell.replace("_p_f", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_f_p"):
                            current_state = current_cell.replace("_f_p", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                        elif current_cell.endswith("_i"):
                            current_state = current_cell.replace("_i", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 1, "isFinal": 0, "isForbidden": 0}})
                        elif current_cell.endswith("_f"):
                            current_state = current_cell.replace("_f", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 0, "isFinal": 1, "isForbidden": 0}})
                        elif current_cell.endswith("_p"):
                            current_state = current_cell.replace("_p", "")
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 0, "isFinal": 0, "isForbidden": 1}})
                        else:
                            current_state = current_cell
                            re.sub(" +", "", current_state)
                            if current_state in dict_X:
                                flag_more_than_one_same_state = 1
                            dict_X.update(
                                {str(current_state): {"row": iter_row+1, "isInitial": 0, "isFinal": 0, "isForbidden": 0}})
                    else:
                        if(temp_current_cell == ''):
                            print(
                            "Syntax error in row='{}', col='State':\t\t\t\t\t\t\tThe name of the state has not been properly specified. Please define it.".format(iter_row+1))

                        flag_empty_state = 1

                else:
                    current_delta_ends = current_cell.split("-")
                    iter_current_delta_ends = 0
                    # to cancel any equal states entered in a cell when more states are specified in it
                    while iter_current_delta_ends < len(current_delta_ends):
                        # print(current_delta_ends)
                        current_delta_end_value = current_delta_ends[iter_current_delta_ends]
                        occurrences_current_delta_end = current_delta_ends.count(current_delta_end_value)
                        if occurrences_current_delta_end > 1:
                            j = iter_current_delta_ends
                            j += 1
                            while j < len(current_delta_ends):
                                if current_delta_end_value == current_delta_ends[j]:
                                    del current_delta_ends[j]
                                    j -= 1
                                else:
                                    j += 1
                        iter_current_delta_ends += 1

                    flag_end_while = 0
                    while flag_end_while == 0:
                        if '' in current_delta_ends:
                            current_delta_ends.remove('')
                        else:
                            flag_end_while = 1

                    for i in range(len(current_delta_ends)):
                        dict_delta.update({str(iter_delta_key): {"start": str(current_state),
                                                                 "name": list_events[iter_col - 1],
                                                                 "ends": str(current_delta_ends[i])}})
                        current_key_event = list_events[iter_col - 1]
                        # print("(iter_row, iter_col) = (" + str(iter_row) + ", " + str(iter_col) + ")")
                        # print("dict_E: ", dict_E)
                        # print("list_events: ", list_events)

                        # print("current_key_event: ", current_key_event)
                        # print("dictcolObservableEvents={}".format(current_key_event, dictcolObservableEvents))
                        # print("dictcolObservableEvents[{}]={}" .format(current_key_event, dictcolObservableEvents[current_key_event]))
                        dict_E.update(
                            {current_key_event: {"isObservable": dictcolObservableEvents[current_key_event],
                                                 "isControllable":
                                                     dictcolControllableEvents[current_key_event],
                                                 "isFault":
                                                     dictcolFaultyEvents[current_key_event]}})

                        iter_delta_key += 1

                    # print(current_delta_ends)
            else:
                pass

    if flag_empty_state == 1:
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        text_cntnt = ""
        text_cntnt += "Some problems occurred converting the table to the file '.\json_table\description_table.json':\r\n"

        text_cntnt += "- One or more of the State names are not specified (empty), please insert it/them.\r\n"
        text_cntnt += "\nPlease look at the terminal for more accurate info, and correct the content of the table.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the table (like a .csv file)."
        win.geometry()
        win['background'] = '#fc5a27'
        win.title("Error parsing the file")
        Label(win, text=text_cntnt, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
        win.mainloop()
        return

    initial_state = {}
    flag_zero_initial_states = 0
    flag_more_than_one_initial_state = 0
    counter_initial_states = 0
    for keyX in dict_X:
        if dict_X[keyX]["isInitial"] == 1 or dict_X[keyX]["isInitial"] == "1":
            counter_initial_states += 1
            if counter_initial_states == 1:
                initial_state = keyX
            elif counter_initial_states > 1:
                flag_more_than_one_initial_state = 1
                print(
                    "Syntax error in row {}:\t\t\t\t\tThe state '{}' has been specified as Initial, while the real initial one is the first defined '{}' in row {}.".format(
                        dict_X[keyX]["row"], keyX, initial_state, dict_X[initial_state]["row"]))

    if counter_initial_states == 0:
        flag_zero_initial_states = 1
        print("Syntax error:\t\t\t\t\t\t\t\tThe initial state has not been specified, please insert it in the 'State' column.")

    flag_event_state = 0
    list_E = list(dict_E.keys())
    for keyX in dict_X:
        if keyX in list_E:
            flag_event_state = 1

    flag_end_state_not_a_state = 0
    list_X = list(dict_X.keys())
    # print("dict_delta: ", dict_delta)
    for keydelta in dict_delta:
        if dict_delta[keydelta]["ends"] not in list_X:
            flag_end_state_not_a_state = 1
            # print("keydelta", keydelta)
            print("Syntax error in row={}, event='{}':\t\t\t\t\tThe end-state '{}' specified in this cell is not defined in the column 'State'." .format(dict_X[dict_delta[keydelta]["start"]]["row"], dict_delta[keydelta]["name"], dict_delta[keydelta]["ends"]))



    flag_error = flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1
    # print("assigning to flag_error: ", flag_error)
    if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
            or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
        title_content = "Conversion problems"
        text_content = "Some problems occurred:\r\n"
        statements_counter = 0
        width_list = []
        if flag_zero_initial_states == 1:
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                width_list.append(950)
            else:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified.\n"
                width_list.append(500)
        if flag_more_than_one_initial_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state' (_i).\n"
            width_list.append(600)
        if flag_end_state_not_a_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: only 'states' specified in the column 'State' are allowed as 'end states' of a transition.\n"
            width_list.append(800)
        if flag_event_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state' like those in the first column (ignore this warning if it is the desired behaviour).\n"
            width_list.append(1000)
        if flag_more_than_one_same_event == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: an 'event' can be defined only once (only one column per 'event').\n"
            width_list.append(600)
        if flag_more_than_one_same_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
            width_list.append(600)
        if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
            text_content += "\nPlease look at the terminal for more accurate info, and correct the content of the table.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the table (like a .csv file)."

        # auto-adapative height of the popup
        win_geometry_height = 100 + 52 * statements_counter
        width_popup = str(max(width_list)) + "x"
        win_geometry = width_popup + str(win_geometry_height)
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title(title_content)
        win['background'] = '#fc5a27'
        Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(
            pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
        win.mainloop()

        if flag_error:
            # print(flag_error)
            return


    for keyX in dict_X:
        del dict_X[keyX]["row"]

    json_dict["X"] = dict_X
    json_dict["delta"] = dict_delta
    json_dict["E"] = dict_E

    with open(".\json_table\description_table.json", "w") as outfile:
        json.dump(json_dict, outfile, indent=4)
    print("... 'description_table.json' generated into the folder 'json_table'.")

    outfile.close()

    return


def from_table_to_json():
    #print("from_table_to_json")
    img = PhotoImage(format='png', file='./images/logo_convert_to_json.png', height=32, width=32)
    return img


def analyze_fsa():
    #print("analyze_fsa")
    # img = PhotoImage(format='png', file='./images/logo_analyze_fsa.png', height=32, width=32)
    img = PhotoImage(format='png', file='./images/logo_analyze_fsa.png', height=57, width=61)

    return img


import os
from tkintertable.Prefs import Preferences


=======
    n = messagebox.askyesno("Convert",
                            "Convert table to json file?",
                            parent=MyTable.parentframe)
    if n:

        flag_more_than_one_same_state = 0  # when has been specified the same state more times
        flag_more_than_one_same_event = 0  # when has been specified the same event more times

        list_columnlabels = list(MyTable.model.columnlabels.values())
        for i in range(len(list_columnlabels)):
            if list_columnlabels.count(list_columnlabels[i]) > 1:
                flag_more_than_one_same_event = 1

        # # print("columnlabels:", MyTable.model.columnlabels.values())

        list_events = []
        for i in range(1, len(list_columnlabels)):
            curr_event = list_columnlabels[i]
            if curr_event.endswith("_uc_f_uo") or curr_event.endswith("_uc_uo_f") or curr_event.endswith(
                    "_f_uc_uo") or curr_event.endswith("_f_uo_uc") or curr_event.endswith(
                "_uo_f_uc") or curr_event.endswith("_uo_uc_f"):
                substring_to_remove = curr_event[-8:]
                curr_event = curr_event.replace(str(substring_to_remove), "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uc_f"):
                curr_event = curr_event.replace("_uc_f", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_f_uc"):
                curr_event = curr_event.replace("_f_uc", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uc_uo"):
                curr_event = curr_event.replace("_uc_uo", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uo_uc"):
                curr_event = curr_event.replace("_uo_uc", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uo_f"):
                curr_event = curr_event.replace("_uo_f", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_f_uo"):
                curr_event = curr_event.replace("_f_uo", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uc"):
                curr_event = curr_event.replace("_uc", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_f"):
                curr_event = curr_event.replace("_f", "")
                re.sub(" +", "", curr_event)
            elif curr_event.endswith("_uo"):
                curr_event = curr_event.replace("_uo", "")
                re.sub(" +", "", curr_event)
            else:
                re.sub(" +", "", curr_event)

            if curr_event in list_events:
                flag_more_than_one_same_event = 1
            list_events.append(curr_event)

        json_dict = {"X": {}, "E": {}, "delta": {}}
        dict_X = {}
        dict_E = {}
        dict_delta = {}
        current_state = ""
        iter_delta_key = 0
        num_rows = MyTable.model.getRowCount()
        num_cols = len(MyTable.model.columnlabels)
        for iter_row in range(num_rows):
            for iter_col in range(num_cols):
                # # print("iter_row,iter_col:" + str(iter_row) + "," + str(iter_col))
                if MyTable.model.getCellRecord(iter_row, iter_col) is not None:
                    current_cell = MyTable.model.getCellRecord(iter_row, iter_col)
                    # # print("current_cell: ", current_cell)
                    if iter_col == 0:
                        if current_cell[0] and current_cell[0] != '_':
                            if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                    "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                                "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                                substring_to_remove = current_cell[-8:]
                                current_state = current_cell.replace(str(substring_to_remove), "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_i_f"):
                                current_state = current_cell.replace("_i_f", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_f_i"):
                                current_state = current_cell.replace("_f_i", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_i_p"):
                                current_state = current_cell.replace("_i_p", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            elif current_cell.endswith("_p_i"):
                                current_state = current_cell.replace("_p_i", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            elif current_cell.endswith("_p_f"):
                                current_state = current_cell.replace("_p_f", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_f_p"):
                                current_state = current_cell.replace("_f_p", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_i"):
                                current_state = current_cell.replace("_i", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 0}})
                            elif current_cell.endswith("_f"):
                                current_state = current_cell.replace("_f", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_p"):
                                current_state = current_cell.replace("_p", "")
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 1}})
                            else:
                                current_state = current_cell
                                re.sub(" +", "", current_state)
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 0}})
                        else:
                             print("cell(" + str(iter_row) + "," + str(iter_col) + " is not a valid name for a state.\nPlease insert a valid one.")
                    else:
                        current_delta_ends = current_cell.split("-")
                        iter_current_delta_ends = 0
                        # to cancel any equal states entered in a cell when more states are specified in it
                        while iter_current_delta_ends < len(current_delta_ends):
                            # print(current_delta_ends)
                            current_delta_end_value = current_delta_ends[iter_current_delta_ends]
                            occurrences_current_delta_end = current_delta_ends.count(current_delta_end_value)
                            if occurrences_current_delta_end > 1:
                                j = iter_current_delta_ends
                                j += 1
                                while j < len(current_delta_ends):
                                    if current_delta_end_value == current_delta_ends[j]:
                                        del current_delta_ends[j]
                                        j -= 1
                                    else:
                                        j += 1
                            iter_current_delta_ends += 1

                        flag_end_while = 0
                        while flag_end_while == 0:
                            if '' in current_delta_ends:
                                current_delta_ends.remove('')
                            else:
                                flag_end_while = 1

                        for i in range(len(current_delta_ends)):
                            dict_delta.update({str(iter_delta_key): {"start": str(current_state), "name": list_events[iter_col-1], "ends": str(current_delta_ends[i])}})
                            current_key_event = list_events[iter_col-1]
                            dict_E.update({current_key_event: {"isObservable": dictcolObservableEvents[current_key_event],
                                                               "isControllable":
                                                                   dictcolControllableEvents[current_key_event],
                                                               "isFault":
                                                                   dictcolFaultyEvents[current_key_event]}})
                            iter_delta_key += 1

                        # print(current_delta_ends)
                else:
                    pass

        flag_zero_initial_states = 0
        flag_more_than_one_initial_state = 0
        counter_initial_states = 0
        for keyX in dict_X:
            if dict_X[keyX]["isInitial"] == 1 or dict_X[keyX]["isInitial"] == "1":
                counter_initial_states += 1
        if counter_initial_states > 1:
            flag_more_than_one_initial_state = 1
        elif counter_initial_states == 0:
            flag_zero_initial_states = 1

        flag_event_state = 0
        list_E = list(dict_E.keys())
        for keyX in dict_X:
            if keyX in list_E:
                flag_event_state = 1

        flag_end_state_not_a_state = 0
        list_X = list(dict_X.keys())
        for keydelta in dict_delta:
            if dict_delta[keydelta]["ends"] not in list_X:
                flag_end_state_not_a_state = 1

        if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
            title_content = "Conversion problems"
            text_content = "Some problems occurred:\r\n"
            statements_counter = 0
            width_list = []
            if flag_zero_initial_states == 1:
                if flag_more_than_one_same_state == 1:
                    statements_counter += 1
                    text_content += str(statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                    width_list.append(950)
                else:
                    statements_counter += 1
                    text_content += str(statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified.\n"
                    width_list.append(500)
            if flag_more_than_one_initial_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state' (_i).\n"
                width_list.append(600)
            if flag_end_state_not_a_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: only 'states' specified in the column 'State' are allowed as 'end states' of a transition.\n"
                width_list.append(800)
            if flag_event_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state' like those in the first column (ignore this warning if it is the desired behaviour).\n"
                width_list.append(1000)
            if flag_more_than_one_same_event == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: an 'event' can be defined only once (only one column per 'event').\n"
                width_list.append(600)
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
                width_list.append(600)
            if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                    or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
                text_content += "Please correct the content of the table.\n"


            # auto-adapative height of the popup
            win_geometry_height = 70 + 52 * statements_counter
            width_popup = str(max(width_list))+"x"
            win_geometry = width_popup + str(win_geometry_height)

            win = Tk()
            # Set the geometry of Tkinter frame
            win.geometry(win_geometry)
            win.title(title_content)
            Label(win, text=text_content, font=('Helvetica 10 bold')).pack(pady=20)
            # Create a button in the main Window to open the popup
            win.mainloop()


        json_dict["X"] = dict_X
        json_dict["delta"] = dict_delta
        json_dict["E"] = dict_E
        print(json_dict)

        with open(".\json_table\description_table.json", "w") as outfile:
            json.dump(json_dict, outfile, indent=4)

        outfile.close()
        # print("Tabella convertita in un json file")

    return

def from_table_to_json():
    # print("from_table_to_json")
    img = PhotoImage(format='png', file='./images/logo_convert_to_json.png', height=32, width=32)
    return img

def analyze_fsa():
    # print("analyze_fsa")
    img = PhotoImage(format='png', file='./images/logo_analyze_fsa.png', height=32, width=32)
    return img

import os
from tkintertable.Prefs import Preferences
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
class TablesApp(Frame):
    """
    Tables app
    """

    def __init__(self, parent=None, data=None, datafile=None):
        "Initialize the application."
<<<<<<< HEAD
        #print("TablesApp__init__")
        super().__init__()
        self.parent = parent

        # If there is data to be loaded, show the dialog first
=======
        ## print("TablesApp__init__")
        super().__init__()
        self.parent = parent

        #If there is data to be loaded, show the dialog first
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
        if not self.parent:
            Frame.__init__(self)
            self.tablesapp_win = self.master
        else:
            self.tablesapp_win = Toplevel()

        # Get platform into a variable
        import platform
        self.currplatform = platform.system()
        if not hasattr(self, 'defaultsavedir'):
            self.defaultsavedir = os.getcwd()

<<<<<<< HEAD
        # self.preferences=Preferences('TablesApp',{'check_for_update':1})
=======
        #self.preferences=Preferences('TablesApp',{'check_for_update':1})
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
        # self.loadprefs()
        self.tablesapp_win.title('Save')
        self.tablesapp_win.geometry('+40+40')
        self.x_size = 800
        self.y_size = 600

        # self.createMenuBar()
<<<<<<< HEAD
        # self.apptoolBar = ToolBar(self.tablesapp_win, self)
        # self.apptoolBar.pack(fill=BOTH, expand=NO)
        # self.createSearchBar()
        # self.tablesapp_win.protocol('WM_DELETE_WINDOW',self.quit)
        return


def analyzeFsa(MyTable):
    #print("analyzeFsa")
    n = messagebox.askyesno("Analyze",
                            "Table converted to the file '.\json_table\description_table.json'.\nDo you want to analyze the FSA?",
                            parent=MyTable.parentframe)
    if n:

        # from fsatoolbox.fsa import fsa

        import analysis
        f = fsa_GUI()
        f.from_file_GUI(filename=".\json_table\description_table.json", bool_table=1)
=======
        #self.apptoolBar = ToolBar(self.tablesapp_win, self)
        #self.apptoolBar.pack(fill=BOTH, expand=NO)
        # self.createSearchBar()
        #self.tablesapp_win.protocol('WM_DELETE_WINDOW',self.quit)
        return

def analyzeFsa(MyTable):
    # print("analyzeFsa")
    n = messagebox.askyesno("Analyze",
                            "Analyze the FSA?",
                            parent=MyTable.parentframe)
    if n:

        from fsatoolbox.fsa import fsa
        import analysis

        f = fsa.from_file('.\json_table\description_table.json')
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta

<<<<<<< HEAD
        num_elements_per_row = 5
        text_content = "FSA name: " + last_sheet + "\n"
        text_content += "___________________________\n"

        dict_max_chars_per_row_found = {}

        if x0:
            # states
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            num_rows = 0
            text_states = ""
            text_states += "States: ["
            num_chars_per_line += len(text_states)
            max_chars_per_row_found = len(text_states)
            for i in range(len(X) - 1):
                current_text = str(X[i].label) + ", "
                text_states += current_text
                num_states_per_row += 1
                num_chars_per_line += len(current_text)
                if num_states_per_row >= num_elements_per_row:
                    text_states += "\n            "
                    num_states_per_row = 0
                    if num_rows == 0:
                        max_chars_per_row_found = num_chars_per_line
                    else:
                        if num_chars_per_line > max_chars_per_row_found:
                            max_chars_per_row_found = num_chars_per_line
                    num_rows += 1
                    num_chars_per_line = 0

            text_states += str(X[len(X) - 1].label) + "]\n"
            text_content += text_states
            num_chars_per_line += len(str(X[len(X) - 1].label) + "]\n")

            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"states": max_chars_per_row_found})


            # initial states
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            num_chars_per_line += len(text_initial_states)
            max_chars_per_row_found = len(text_initial_states)
            for i in range(len(x0) - 1):
                current_text = str(x0[i].label) + ", "
                text_initial_states += current_text
                num_states_per_row += 1
                num_chars_per_line += len(current_text)
                if num_states_per_row >= num_elements_per_row:
                    text_initial_states += "\n                    "
                    num_states_per_row = 0
                    if num_rows == 0:
                        max_chars_per_row_found = num_chars_per_line
                    else:
                        if num_chars_per_line > max_chars_per_row_found:
                            max_chars_per_row_found = num_chars_per_line
                    num_rows += 1
                    num_chars_per_line = 0
            text_initial_states += str(x0[len(x0) - 1].label) + "]\n"
            text_content += text_initial_states
            num_chars_per_line +=  len(str(x0[len(x0) - 1].label) + "]\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"init_states": max_chars_per_row_found})


            # final states
            text_final_states = ""
            if Xm:
                num_rows = 0
                max_chars_per_row_found = 0
                num_chars_per_line = 0
                num_states_per_row = 0
                text_final_states += "Final states: ["
                num_chars_per_line += len(text_final_states)
                max_chars_per_row_found = len(text_final_states)
                for i in range(len(Xm) - 1):
                    current_text = str(Xm[i].label) + ", "
                    text_final_states += current_text
                    num_states_per_row += 1
                    num_chars_per_line += len(current_text)
                    if num_states_per_row >= num_elements_per_row:
                        text_final_states += "\n                   "
                        num_states_per_row = 0
                        if num_rows == 0:
                            max_chars_per_row_found = num_chars_per_line
                        else:
                            if num_chars_per_line > max_chars_per_row_found:
                                max_chars_per_row_found = num_chars_per_line
                        num_rows += 1
                        num_chars_per_line = 0
                text_final_states += str(Xm[len(Xm) - 1].label) + "]\n"
                num_chars_per_line += len(str(Xm[len(Xm) - 1].label) + "]\n")
                text_content += text_final_states
            else:
                text_content += "Final states: []\n"
                num_chars_per_line += len("Final states: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"final_states": max_chars_per_row_found})


            # forbidden states
            text_forbidden_states = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
=======
        num_chars_per_line = 50
        text_content = "FSA name: " + last_sheet + "\n"
        text_content += "______________________________________\n"

        if x0:
            # states
            text_states = ""
            text_states += "States: ["
            chars_count = len(text_states)
            for i in range(len(X) - 1):
                current_text = str(X[i].label) + ", "
                text_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_states += "\n            "
                    chars_count = 0
            text_states += str(X[len(X) - 1].label) + "]\n"
            text_content += text_states

            # initial states
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            chars_count = len(text_initial_states)
            for i in range(len(x0) - 1):
                current_text = str(x0[i].label) + ", "
                text_initial_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_initial_states += "\n                    "
                    chars_count = 0
            text_initial_states += str(x0[len(x0) - 1].label) + "]\n"
            text_content += text_initial_states

            # final states
            if Xm:
                text_final_states = ""
                text_final_states += "Final states: ["
                chars_count = len(text_final_states)
                for i in range(len(Xm) - 1):
                    current_text = str(Xm[i].label) + ", "
                    text_final_states += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_final_states += "\n                   "
                        chars_count = 0
                text_final_states += str(Xm[len(Xm) - 1].label) + "]\n"
                text_content += text_final_states
            else:
                text_content += "Final states: []\n"

            # forbidden states
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            num_forbidden_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].isForbidden == 1:
                    num_forbidden_states += 1
            if num_forbidden_states != 0:
                counter_forbidden_states = 0
                text_forbidden_states = ""
                text_forbidden_states += "Forbidden states: ["
<<<<<<< HEAD
                num_chars_per_line += len(text_forbidden_states)
                max_chars_per_row_found = len(text_forbidden_states)
=======
                chars_count = len(text_forbidden_states)
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                for i in range(len(X)):
                    if X[i].isForbidden == 1:
                        if counter_forbidden_states < num_forbidden_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_forbidden_states += 1
                        text_forbidden_states += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_forbidden_states += "\n                        "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                text_content += text_forbidden_states + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Forbidden states: []\n"
                num_chars_per_line += len("Forbidden states: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"forb_states": max_chars_per_row_found})



            text_content += "___________________________\n"




            # alphabet
            text_alphabet = ""
            if E:
                num_rows = 0
                max_chars_per_row_found = 0
                num_chars_per_line = 0
                num_events_per_row = 0
                text_alphabet = ""
                text_alphabet += "Alphabet: ["
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
                for i in range(len(E) - 1):
                    current_text = str(E[i].label) + ", "
                    text_alphabet += current_text
                    num_events_per_row += 1
                    num_chars_per_line += len(current_text)
                    if num_events_per_row >= num_elements_per_row:
                        text_alphabet += "\n                "
                        num_events_per_row = 0
                        if num_rows == 0:
                            max_chars_per_row_found = num_chars_per_line
                        else:
                            if num_chars_per_line > max_chars_per_row_found:
                                max_chars_per_row_found = num_chars_per_line
                        num_rows += 1
                        num_chars_per_line = 0
                text_alphabet += str(E[len(E) - 1].label) + "]\n"
                num_chars_per_line += len(str(E[len(E) - 1].label) + "]\n")
                text_content += text_alphabet
            else:
                text_content += "Alphabet: []\n"
                num_chars_per_line += len("Alphabet: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"alphabet": max_chars_per_row_found})

            # unobservable events
            text_alphabet = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_events_per_row = 0
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_forbidden_states += "\n                        "
                            chars_count = 0
                text_content += text_forbidden_states + "\n"
            else:
                text_content += "Forbidden states: []\n"


            text_content += "______________________________________\n"


            # alphabet
            if E:
                text_alphabet = ""
                text_alphabet += "Alphabet: ["
                chars_count = len(text_alphabet)
                for i in range(len(E) - 1):
                    current_text = str(E[i].label) + ", "
                    text_alphabet += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_alphabet += "\n                "
                        chars_count = 0
                text_alphabet += str(E[len(E) - 1].label) + "]\n"
                text_content += text_alphabet
            else:
                text_content += "Alphabet: []\n"

            # unobservable events
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            num_unobservable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isObservable == 0:
                    num_unobservable_events += 1
            if num_unobservable_events != 0:
                counter_unobservable_events = 0
                text_alphabet = ""
                text_alphabet += "Unobservable events: ["
<<<<<<< HEAD
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
=======
                chars_count = len(text_alphabet)
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                for i in range(len(E)):
                    if E[i].isObservable == 0:
                        if counter_unobservable_events < num_unobservable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_unobservable_events += 1
                        text_alphabet += current_text
<<<<<<< HEAD
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Unobservable events: []\n"
                num_chars_per_line += len("Unobservable events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"uo_events": max_chars_per_row_found})


            # uncontrollable events
            text_alphabet = ""
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_events_per_row = 0
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Unobservable events: []\n"

            # uncontrollable events
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            num_uncontrollable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isControllable == 0:
                    num_uncontrollable_events += 1
            if num_uncontrollable_events != 0:
                counter_uncontrollable_events = 0
                text_alphabet = ""
                text_alphabet += "Uncontrollable events: ["
<<<<<<< HEAD
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
=======
                chars_count = len(text_alphabet)
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                for i in range(len(E)):
                    if E[i].isControllable == 0:
                        if counter_uncontrollable_events < num_uncontrollable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_uncontrollable_events += 1
                        text_alphabet += current_text
<<<<<<< HEAD
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                                   "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Uncontrollable events: []\n"
                num_chars_per_line += len("Uncontrollable events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"uc_events": max_chars_per_row_found})


            # fault events
            text_alphabet = ""
            num_rows = 0
            num_events_per_row = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                                   "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Uncontrollable events: []\n"

            # fault events
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            num_fault_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isFault == 1:
                    num_fault_events += 1
            if num_fault_events != 0:
                counter_fault_events = 0
                text_alphabet = ""
                text_alphabet += "Fault events: ["
<<<<<<< HEAD
                num_chars_per_line += len(text_alphabet)
                max_chars_per_row_found = len(text_alphabet)
=======
                chars_count = len(text_alphabet)
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                for i in range(len(E)):
                    if E[i].isFault == 1:
                        if counter_fault_events < num_fault_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_fault_events += 1
                        text_alphabet += current_text
<<<<<<< HEAD
                        num_events_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_events_per_row >= num_elements_per_row:
                            text_alphabet += "\n                            "
                            num_events_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
                text_content += text_alphabet + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += "Fault events: []\n"
                num_chars_per_line += len("Fault events: []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"f_events": max_chars_per_row_found})

            text_content += "___________________________\n"

            # delta relations
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_deltas_per_row = 0
            text_content += "Delta relations:\n"
            max_chars_per_row_found = len("Delta relations:\n")
            text_delta = ""
            if len(delta) != 0:
                for iter_X in range(len(X)):
                    current_start_filtered_deltas = f.filter_delta(start=str(X[iter_X].label), transition=None,
                                                                   end=None)
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                            "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Fault events: []\n"

            text_content += "______________________________________\n"


            # delta transitions
            num_chars_per_line = 50
            text_content += "Delta transitions:\n"
            text_delta = ""
            if len(delta) != 0:
                for iter_X in range(len(X)):
                    current_start_filtered_deltas = f.filter_delta(start=str(X[iter_X].label), transition=None, end=None)
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                    if len(current_start_filtered_deltas) == 0:
                        pass
                    else:
                        for iter_delta_row in range(len(current_start_filtered_deltas)):
                            if current_start_filtered_deltas.index[iter_delta_row] is not None:
<<<<<<< HEAD
                                current_text = "(" + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["start"]) + ", " + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["transition"]) + ", " + str(
                                    current_start_filtered_deltas.iloc[iter_delta_row]["end"]) + ")  "
                                text_delta += current_text
                                num_deltas_per_row += 1
                                num_chars_per_line += len(current_text)
                                if num_deltas_per_row >= num_elements_per_row:
                                    text_delta += "\n"
                                    num_deltas_per_row = 0
                                    if num_rows == 0:
                                        max_chars_per_row_found = num_chars_per_line
                                    else:
                                        if num_chars_per_line > max_chars_per_row_found:
                                            max_chars_per_row_found = num_chars_per_line
                                    num_rows += 1
                                    num_chars_per_line = 0
                            else:
                                pass
                text_content += text_delta + "\n"
                num_chars_per_line += len("\n")
            else:
                text_content += " []\n"
                num_chars_per_line += len(" []\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"deltas": max_chars_per_row_found})
                

            # Reachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_reachable = analysis.get_reachability_info(f)
            text_content += "___________________________\n"
            text_content += "\nREACHABLE STATES\n"
            max_chars_per_row_found = len("\nREACHABLE STATES\n")
            text_content += "Reachable: ["
            num_chars_per_line += len("Reachable: [")
=======
                                current_text = "(" + str(current_start_filtered_deltas.iloc[iter_delta_row]["start"]) + ", " + str(current_start_filtered_deltas.iloc[iter_delta_row]["transition"]) + ", " + str(current_start_filtered_deltas.iloc[iter_delta_row]["end"]) + ")  "
                                text_delta += current_text
                                chars_count += len(current_text)
                                if chars_count >= num_chars_per_line:
                                    text_delta += "\n"
                                    chars_count = 0
                            else:
                                pass
                text_content += text_delta + "\n"
            else:
                text_content += " []\n"


            # Reachability
            is_reachable = analysis.get_reachability_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nREACHABLE STATES\n"
            text_content += "Reachable: ["
            chars_count = len("Reachable: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_reachability = ""
            num_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 1:
                    num_reachable_states += 1
            if num_reachable_states != 0:
                counter_reachable_states = 0
                for i in range(len(X)):
                    if X[i].is_Reachable:
<<<<<<< HEAD
                        if counter_reachable_states < num_reachable_states - 1:
=======
                        if counter_reachable_states < num_reachable_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_reachable_states += 1
                        text_reachability += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_reachability += "\n                   "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_reachability += "]"
            text_content += text_reachability + "\n"
            num_chars_per_line += len("]"+"\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"reach_states": max_chars_per_row_found})


            # Unreachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not reachable: ["
            num_chars_per_line += len("Not reachable: [")
            max_chars_per_row_found = len("Not reachable: [")
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_reachability += "\n                   "
                            chars_count = 0
            else:
                text_reachability += "]"
            text_content += text_reachability + "\n"


            # Unreachability
            text_content += "Not reachable: ["
            chars_count = len("Not reachable: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_unreachability = ""
            num_unreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 0:
                    num_unreachable_states += 1
            counter_unreachable_states = 0
            if num_unreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_Reachable == 0:
<<<<<<< HEAD
                        if counter_unreachable_states < num_unreachable_states - 1:
=======
                        if counter_unreachable_states < num_unreachable_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unreachable_states += 1
                        text_unreachability += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_unreachability += "\n                           "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_unreachability += "]"
                num_chars_per_line += len("]" + "\n")
            text_content += text_unreachability + "\n"
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_reach_states": max_chars_per_row_found})
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unreachability += "\n                           "
                            chars_count = 0
            else:
                text_unreachability += "]"
            text_content += text_unreachability + "\n"
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366

            text_content += "FSA is reachable? "
            if is_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Co-Reachability
<<<<<<< HEAD
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_co_reachable = analysis.get_co_reachability_info(f)
            text_content += "___________________________\n"
            text_content += "\nCO-REACHABLE STATES\n"
            text_content += "Co-reachable: ["
            num_chars_per_line += len("Co-reachable: [")
            max_chars_per_row_found = len("\nCO-REACHABLE STATES\n")
=======
            is_co_reachable = analysis.get_co_reachability_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nCO-REACHABLE STATES\n"
            text_content += "Co-reachable: ["
            chars_count = len("Co-reachable: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_co_reachability = ""
            num_co_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 1:
                    num_co_reachable_states += 1
            counter_co_reachable_states = 0
            if num_co_reachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable:
<<<<<<< HEAD
                        if counter_co_reachable_states < num_co_reachable_states - 1:
=======
                        if counter_co_reachable_states < num_co_reachable_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_co_reachable_states += 1
                        text_co_reachability += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_co_reachability += "\n                        "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_co_reachability += "]"
            text_content += text_co_reachability + "\n"
            num_chars_per_line += len("]"+ "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"co-reach_states": max_chars_per_row_found})


            # Not Co-Reachability
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not co-reachable: ["
            num_chars_per_line += len("Not co-reachable: [")
            max_chars_per_row_found = len("Not co-reachable: [")
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_co_reachability += "\n                        "
                            chars_count = 0
            else:
                text_co_reachability += "]"
            text_content += text_co_reachability + "\n"


            # Not Co-Reachability
            text_content += "Not co-reachable: ["
            chars_count = len("Not co-reachable: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_uncoreachability = ""
            num_uncoreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 0:
                    num_uncoreachable_states += 1
            counter_uncoreachable_states = 0
            if num_uncoreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable == 0:
<<<<<<< HEAD
                        if counter_uncoreachable_states < num_uncoreachable_states - 1:
=======
                        if counter_uncoreachable_states < num_uncoreachable_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_uncoreachable_states += 1
                        text_uncoreachability += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_uncoreachability += "\n                                "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_uncoreachability += "]"
            text_content += text_uncoreachability + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_co-reach_states": max_chars_per_row_found})
            
            
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_uncoreachability += "\n                                "
                            chars_count = 0
            else:
                text_uncoreachability += "]"
            text_content += text_uncoreachability + "\n"

>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_content += "FSA is co-reachable? "
            if is_co_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Blocking
<<<<<<< HEAD
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            is_blocking = analysis.get_blockingness_info(f)
            text_content += "___________________________\n"
            text_content += "\nBLOCKING STATES\n"
            max_chars_per_row_found = len("\nBLOCKING STATES\n")
=======
            is_blocking = analysis.get_blockingness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nBLOCKING STATES\n"
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_content += "Blocking: ["
            chars_count = len("Blocking: [")
            text_blocking = ""
            num_blocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 1:
                    num_blocking_states += 1
            counter_blocking_states = 0
            if num_blocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking:
<<<<<<< HEAD
                        if counter_blocking_states < num_blocking_states - 1:
=======
                        if counter_blocking_states < num_blocking_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_blocking_states += 1
                        text_blocking += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_blocking += "\n               "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_blocking += "]"
            text_content += text_blocking + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"blocking": max_chars_per_row_found})


            # Not blocking
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not blocking: ["
            num_chars_per_line += len("Not blocking: [")
            max_chars_per_row_found = len("Not blocking: [")
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_blocking += "\n               "
                            chars_count = 0
            else:
                text_blocking += "]"
            text_content += text_blocking + "\n"


            # Not blocking
            text_content += "Not blocking: ["
            chars_count = len("Not blocking: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_unblocking = ""
            num_unblocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 0:
                    num_unblocking_states += 1
            counter_unblocking_states = 0
            if num_unblocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking == 0:
<<<<<<< HEAD
                        if counter_unblocking_states < num_unblocking_states - 1:
=======
                        if counter_unblocking_states < num_unblocking_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unblocking_states += 1
                        text_unblocking += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_unblocking += "\n                       "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_unblocking += "]"
            text_content += text_unblocking + "\n"
            num_chars_per_line += len("]" + "\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_blocking": max_chars_per_row_found})
            
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unblocking += "\n                       "
                            chars_count = 0
            else:
                text_unblocking += "]"
            text_content += text_unblocking + "\n"
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366

            text_content += "FSA is blocking? "
            if is_blocking == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Dead
<<<<<<< HEAD
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            analysis.get_deadness_info(f)
            text_content += "___________________________\n"
            text_content += "\nDEAD STATES\n"
            max_chars_per_row_found = len("\nDEAD STATES\n")
            text_content += "Dead: ["
            num_chars_per_line += len("Dead: [")
=======
            analysis.get_deadness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nDEAD STATES\n"
            text_content += "Dead: ["
            chars_count = len("Dead: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_dead = ""
            num_dead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 1:
                    num_dead_states += 1
            counter_dead_states = 0
            if num_dead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead:
<<<<<<< HEAD
                        if counter_dead_states < num_dead_states - 1:
=======
                        if counter_dead_states < num_dead_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_dead_states += 1
                        text_dead += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_dead += "\n                    "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_dead += "]"
            text_content += text_dead + "\n"
            num_chars_per_line += len("]"+"\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"dead": max_chars_per_row_found})


            # Not dead
            num_rows = 0
            max_chars_per_row_found = 0
            num_chars_per_line = 0
            num_states_per_row = 0
            text_content += "Not dead: ["
            num_chars_per_line += len("Not dead: [")
            max_chars_per_row_found = len("Not dead: [")
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_dead += "\n                    "
                            chars_count = 0
            else:
                text_dead += "]"
            text_content += text_dead + "\n"


            # Not dead
            text_content += "Not dead: ["
            chars_count = len("Not dead: [")
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_undead = ""
            num_undead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 0:
                    num_undead_states += 1
            counter_undead_states = 0
            if num_undead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead == 0:
<<<<<<< HEAD
                        if counter_undead_states < num_undead_states - 1:
=======
                        if counter_undead_states < num_undead_states-1:
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_undead_states += 1
                        text_undead += current_text
<<<<<<< HEAD
                        num_states_per_row += 1
                        num_chars_per_line += len(current_text)
                        if num_states_per_row >= num_elements_per_row:
                            text_undead += "\n                  "
                            num_states_per_row = 0
                            if num_rows == 0:
                                max_chars_per_row_found = num_chars_per_line
                            else:
                                if num_chars_per_line > max_chars_per_row_found:
                                    max_chars_per_row_found = num_chars_per_line
                            num_rows += 1
                            num_chars_per_line = 0
            else:
                text_undead += "]"
            text_content += text_undead + "\n"
            num_chars_per_line += len("]"+"\n")
            if num_chars_per_line > max_chars_per_row_found:
                max_chars_per_row_found = num_chars_per_line
            dict_max_chars_per_row_found.update({"not_dead": max_chars_per_row_found})

            # Trim
            is_trim = analysis.get_trim_info(f)
            text_content += "___________________________\n"
=======
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_undead += "\n                  "
                            chars_count = 0
            else:
                text_undead += "]"
            text_content += text_undead + "\n"


            # Trim
            is_trim = f.get_trim_info()
            text_content += "______________________________________"
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_content += "\nTRIM\n"
            if is_trim == 1:
                text_content += "FSA is trim? YES\n"
            else:
                text_content += "FSA is trim? NO\n"

<<<<<<< HEAD

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "___________________________\n"
=======
            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "______________________________________"
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
            text_content += "\nREVERSIBILITY:\n"
            if is_reversible == 1:
                text_content += "FSA is reversible? YES\n"
            else:
                text_content += "FSA is reversible? NO\n"

        else:
            text_content = "Error: At least the initial state must be specified."

        import tkinter as tk
        import tkinter.scrolledtext as st

        # Creating tkinter window
        win = tk.Tk()
        win.title("Results window")

        # Title Label
        tk.Label(win,
                 text="FSA analysis results",
                 font=("Times New Roman", 17)).grid(column=0, row=0)

        # download button
        from tkinter.messagebox import showinfo

        def save_fsa_analysis_results():
            """Save as a new filename"""
            # print("save_fsa_analysis_results")
            ta = TablesApp(Frame)
            filename = filedialog.asksaveasfilename(parent=ta.tablesapp_win,
                                                    defaultextension='.txt',
                                                    initialdir=ta.defaultsavedir,
<<<<<<< HEAD
                                                    filetypes=[("Text file", "*.txt"),
                                                               ("All files", "*.*")])
            if not filename:
                print('Returning')
=======
                                                    filetypes=[("Text file","*.txt"),
                                                               ("All files","*.*")])
            if not filename:
                print ('Returning')
>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
                return

            with open(filename, 'w') as fo:
                fo.write(text_content)
                fo.close()
            return

<<<<<<< HEAD
        width = 0
        for keymax in dict_max_chars_per_row_found:
            if dict_max_chars_per_row_found[keymax] > width:
                width = dict_max_chars_per_row_found[keymax]


        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green",
                              foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area widget with Read only by disabling the state
        win.geometry()
        text_area = st.ScrolledText(win, width=width, height=30, font=("Times New Roman", 12))
=======
        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green", foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area widget with Read only by disabling the state
        text_area = st.ScrolledText(win, width=50, height=30, font=("Times New Roman", 12))

>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
        text_area.grid(column=0, pady=10, padx=10)

        # Inserting Text which is read only
        text_area.insert(tk.INSERT, text_content)

        # Making the text read only
        text_area.configure(state='disabled')
        win.mainloop()

<<<<<<< HEAD
def check_syntax_errors_in_json_file(jsonObject):
    #print("check_syntax_errors_in_json_file")
    flag_syntax_error = 0
    # check if the .json the 3 elements 'X', 'E' and 'delta'
    dict_events = {}
    if 'E' in jsonObject:
        dict_events = jsonObject["E"].copy()
        iter = 0
        for key in dict_events:
            dict_events[key].update({"column": iter})
            iter += 1

        # check if there are event properties of values different from 0 or 1
        list_events_without_all_3_properties = []
        list_events_without_right_prop_values = []
        flag_event_prop_not_complete = 0
        flag_event_prop_not_allowed = 0
        for keyE in dict_events:
            if "isControllable" not in dict_events[keyE] or "isObservable" not in dict_events[keyE] or "isFault" not in \
                    dict_events[keyE]:
                list_events_without_all_3_properties.append(keyE)
                flag_event_prop_not_complete = 1
            if "isControllable" in dict_events[keyE]:
                bool_cont = (dict_events[keyE]["isControllable"] == 1 or dict_events[keyE]["isControllable"] == 0)
                if bool_cont == 0:
                    list_events_without_right_prop_values.append(keyE)
                    flag_event_prop_not_allowed = 1
            if "isObservable" in dict_events[keyE]:
                bool_obs = (dict_events[keyE]["isObservable"] == 1 or dict_events[keyE]["isObservable"] == 0)
                if bool_obs == 0:
                    list_events_without_right_prop_values.append(keyE)
                    flag_event_prop_not_allowed = 1
            if "isFault" in dict_events[keyE]:
                bool_fault = (dict_events[keyE]["isFault"] == 1 or dict_events[keyE]["isFault"] == 0)
                if bool_fault == 0:
                    list_events_without_right_prop_values.append(keyE)
                    flag_event_prop_not_allowed = 1
        if flag_event_prop_not_complete == 1:
            flag_syntax_error = 1
            for i in range(len(list_events_without_all_3_properties)):
                print(
                    "Syntax error:\t\t\tThe event '{}' has not all the properties declared ('isControllable', 'isObservable', 'isFault').".format(
                        list_events_without_all_3_properties[i]))
        if flag_event_prop_not_allowed == 1:
            flag_syntax_error = 1
            for i in range(len(list_events_without_right_prop_values)):
                print(
                    "Syntax error:\t\t\tThe event '{}' has not all the properties of allowed values (only 1 or 0).".format(
                        list_events_without_right_prop_values[i]))
    else:
        print("Syntax error:\t\tElement 'E' (dictionary of the events) not found in the .json file. Please insert it.")
        flag_syntax_error = 1


    dict_start_states = {}
    if 'X' in jsonObject:
        dict_start_states = jsonObject["X"].copy()
        iter = 0
        for key in dict_start_states:
            dict_start_states[key].update({"row": iter})
            iter += 1

        # check if there are state properties of values different from 0 or 1
        list_states_without_all_3_properties = []
        list_states_without_right_prop_values = []
        flag_state_prop_not_complete = 0
        flag_state_prop_not_allowed = 0
        for keyX in dict_start_states:
            if "isInitial" not in dict_start_states[keyX] or "isFinal" not in dict_start_states[
                keyX] or "isForbidden" not in dict_start_states[keyX]:
                list_states_without_all_3_properties.append(keyX)
                flag_state_prop_not_complete = 1
            if "isInitial" in dict_start_states[keyX]:
                bool_init = (dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX][
                    "isInitial"] == 0)
                if bool_init == 0:
                    list_states_without_right_prop_values.append(keyX)
                    flag_state_prop_not_allowed = 1
            if "isFinal" in dict_start_states[keyX]:
                bool_final = (dict_start_states[keyX]["isFinal"] == 1 or dict_start_states[keyX][
                    "isFinal"] == 0)
                if bool_final == 0:
                    list_states_without_right_prop_values.append(keyX)
                    flag_state_prop_not_allowed = 1
            if "isForbidden" in dict_start_states[keyX]:
                bool_forb = (dict_start_states[keyX]["isForbidden"] == 1 or dict_start_states[keyX][
                    "isForbidden"] == 0)
                if bool_forb == 0:
                    list_states_without_right_prop_values.append(keyX)
                    flag_state_prop_not_allowed = 1

        if flag_state_prop_not_complete == 1:
            flag_syntax_error = 1
            for i in range(len(list_states_without_all_3_properties)):
                print(
                    "Syntax error:\t\t\tThe state '{}' has not all the properties declared ('isInitial', 'isFinal', 'isForbidden').".format(
                        list_states_without_all_3_properties[i]))
        if flag_state_prop_not_allowed == 1:
            flag_syntax_error = 1
            for i in range(len(list_states_without_right_prop_values)):
                print(
                    "Syntax error:\t\t\tThe state '{}' has not all the properties of allowed values (only 1 or 0).".format(
                        list_states_without_right_prop_values[i]))

        # check if there are more initial states
        flag_first_init_state = 0
        flag_more_init_state = 0
        list_other_initial_states = []
        initial_state = ""
        for keyX in dict_start_states:
            if "isInitial" in dict_start_states[keyX] and flag_first_init_state == 0 and (
                    dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX][
                "isInitial"] == "1"):
                flag_first_init_state = 1
                initial_state = keyX
            elif "isInitial" in dict_start_states[keyX] and flag_first_init_state == 1 and (
                    dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX][
                "isInitial"] == "1"):
                flag_more_init_state = 1
                list_other_initial_states.append(keyX)
            else:
                pass
        if flag_more_init_state == 1:
            flag_syntax_error = 1
            for i in range(len(list_other_initial_states)):
                print(
                    "Syntax error:\t\t\tThe state '{}' is set as Initial, but only the first initial state specified ('{}') can be considered as the Initial one.".format(
                        list_other_initial_states[i], initial_state))

    else:
        print(
            "Syntax error:\t\tElement 'X' (dictionary of the states) not found in the .json file. Please insert it.")
        flag_syntax_error = 1

    list_start_states = []
    list_start_states = list(dict_start_states.keys())
    list_events = list(dict_events.keys())
    dict_deltas = {}

    if 'delta' in jsonObject:
        iter = 0
        for key in jsonObject["delta"]:
            dict_deltas.update({str(iter): jsonObject["delta"][key]})
            iter += 1
    else:
        print(
            "Syntax error:\t\tElement 'delta' (dictionary of deltas) not found in the .json file. Please insert it.")
        flag_syntax_error = 1

    # check if there are more states with the same label
    # not possible, since if there are more equal keys, only the last will be taken into account

    # check if there are more events with the same label
    # not possible, since if there are more equal keys, only the last will be taken into account

    flag_syntax_warning = 0
    # check if there are events with the same name as a state (Warning)
    if 'X' in jsonObject and 'E' in jsonObject:
        list_events_named_as_states = []
        flag_events_named_as_states = 0
        for keyX in dict_start_states:
            for keyE in dict_events:
                if keyE == keyX:
                    flag_events_named_as_states = 1
                    list_events_named_as_states.append(keyE)
        if flag_events_named_as_states == 1:
            flag_syntax_warning = 1
            for i in range(len(list_events_named_as_states)):
                print(
                    "Syntax warning:\t\t\tThe event '{}' has the same name as the state '{}'. Please ignore this warning if this is the correct set-up.".format(
                        list_events_named_as_states[i], list_events_named_as_states[i]))

    # check if there are start-states or end-states of a delta transition not specified as states
    if 'X' in jsonObject and 'delta' in jsonObject:
        list_start_states_not_in_states = []
        list_end_states_not_in_states = []
        flag_start_states_not_in_states = 0
        flag_end_states_not_in_states = 0
        for keyDelta in dict_deltas:
            if "start" in dict_deltas[keyDelta] and dict_deltas[keyDelta][
                "start"] not in dict_start_states:
                flag_start_states_not_in_states = 1
                list_start_states_not_in_states.append(
                    {"key": keyDelta, "start": dict_deltas[keyDelta]["start"]})
            if "ends" in dict_deltas[keyDelta] and dict_deltas[keyDelta][
                "ends"] not in dict_start_states:
                flag_end_states_not_in_states = 1
                list_end_states_not_in_states.append(
                    {"key": keyDelta, "ends": dict_deltas[keyDelta]["ends"]})
        if flag_start_states_not_in_states == 1:
            flag_syntax_error = 1
            for i in range(len(list_start_states_not_in_states)):
                print(
                    "Syntax error:\t\t\tThe start-state '{}' of the delta transition '{}' is not defined as a state in 'X'.".format(
                        list_start_states_not_in_states[i]["start"],
                        list_start_states_not_in_states[i]["key"]))
        if flag_end_states_not_in_states == 1:
            flag_syntax_error = 1
            for i in range(len(list_end_states_not_in_states)):
                print(
                    "Syntax error:\t\t\tThe end-state '{}' of the delta transition '{}' is not defined as a state in 'X'.".format(
                        list_end_states_not_in_states[i]["ends"],
                        list_end_states_not_in_states[i]["key"]))

    # check if there are events of a delta transition not specified as events
    if 'E' in jsonObject and 'delta' in jsonObject:
        list_delta_events_not_in_events = []
        flag_delta_events_not_in_events = 0
        for keyDelta in dict_deltas:
            if "name" in dict_deltas[keyDelta] and dict_deltas[keyDelta]["name"] not in dict_events:
                flag_delta_events_not_in_events = 1
                list_delta_events_not_in_events.append(
                    {"key": keyDelta, "name": dict_deltas[keyDelta]["name"]})
        if flag_delta_events_not_in_events == 1:
            flag_syntax_error = 1
            for i in range(len(list_delta_events_not_in_events)):
                print(
                    "Syntax error:\t\t\tThe event name '{}' of the delta transition '{}' is not defined as an event in 'E'.".format(
                        list_delta_events_not_in_events[i]["name"],
                        list_delta_events_not_in_events[i]["key"]))



    if flag_syntax_error == 1 or flag_syntax_warning == 1:
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title("Error parsing the file")
        win['background'] = '#fc5a27'
        Label(win,
              text="Some problems occurred parsing the file '" + GUI_Utils.last_sheet +  ".json':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                        "(Look at the terminal to see all the errors)\r\n\n"
                                                                                        "Click the button below if you want to see an example on how to "
                                                                                        "correctly populate the file.",
              font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_json_file).pack()
        win.mainloop()

        if flag_syntax_error == 1:
            return
=======

>>>>>>> 6eec0fc7ba72e11e7493637950183fe7ca785366
