import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, ttk, Tk, Label, Toplevel, Button, Text, BOTH, \
    StringVar
from tkinter.ttk import Frame

import re
from tkinter.ttk import Combobox


dictcolObservableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolControllableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolFaultyEvents = {'event1': 0, 'event2': 0, 'event3': 0, 'event4': 0}

last_sheet = "Sheet1"

def setEventAsUnobservable(MyTable, column_name=None):
    """Set the event as Unobservable - can be used in a table header"""
    # print("setEventAsUnobservable")
    global dictcolObservableEvents
    if column_name is None:
        n = messagebox.askyesno("Setting",
                                "Unobservable Event?")
        if n:

            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolObservableEvents[str(current_col_name)] = 0
    else:
        dictcolObservableEvents[str(column_name)] = 0

def setEventAsObservable(MyTable, column_name=None):
    """Set the event as Observable - can be used in a table header"""
    # print("setEventAsObservable")
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

def setEventAsUncontrollable(MyTable, column_name=None):
    """Set the event as Uncontrollable - can be used in a table header"""
    # print("setEventAsUncontrollable")
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

def setEventAsControllable(MyTable, column_name=None):
    """Set the event as Controllable - can be used in a table header"""
    # print("setEventAsControllable")
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

def setEventAsFaulty(MyTable, column_name=None):
    """Set the event as Faulty - can be used in a table header"""
    # print("setEventAsFaulty")
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

def setEventAsUnfaulty(MyTable, column_name=None):
    """Set the event as Unfaulty - can be used in a table header"""
    # print("setEventAsUnfaulty")
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

def fromTableToJson(MyTable):
    """Convert the current table content into a Json file"""
    # print("fromTableToJson")
    global dictcolControllableEvents
    global dictcolObservableEvents
    global dictcolFaultyEvents

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
class TablesApp(Frame):
    """
    Tables app
    """

    def __init__(self, parent=None, data=None, datafile=None):
        "Initialize the application."
        ## print("TablesApp__init__")
        super().__init__()
        self.parent = parent

        #If there is data to be loaded, show the dialog first
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

        #self.preferences=Preferences('TablesApp',{'check_for_update':1})
        # self.loadprefs()
        self.tablesapp_win.title('Save')
        self.tablesapp_win.geometry('+40+40')
        self.x_size = 800
        self.y_size = 600

        # self.createMenuBar()
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

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta

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
            num_forbidden_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].isForbidden == 1:
                    num_forbidden_states += 1
            if num_forbidden_states != 0:
                counter_forbidden_states = 0
                text_forbidden_states = ""
                text_forbidden_states += "Forbidden states: ["
                chars_count = len(text_forbidden_states)
                for i in range(len(X)):
                    if X[i].isForbidden == 1:
                        if counter_forbidden_states < num_forbidden_states - 1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_forbidden_states += 1
                        text_forbidden_states += current_text
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
            num_unobservable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isObservable == 0:
                    num_unobservable_events += 1
            if num_unobservable_events != 0:
                counter_unobservable_events = 0
                text_alphabet = ""
                text_alphabet += "Unobservable events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isObservable == 0:
                        if counter_unobservable_events < num_unobservable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_unobservable_events += 1
                        text_alphabet += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Unobservable events: []\n"

            # uncontrollable events
            num_uncontrollable_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isControllable == 0:
                    num_uncontrollable_events += 1
            if num_uncontrollable_events != 0:
                counter_uncontrollable_events = 0
                text_alphabet = ""
                text_alphabet += "Uncontrollable events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isControllable == 0:
                        if counter_uncontrollable_events < num_uncontrollable_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_uncontrollable_events += 1
                        text_alphabet += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_alphabet += "\n                                   "
                            chars_count = 0
                text_content += text_alphabet + "\n"
            else:
                text_content += "Uncontrollable events: []\n"

            # fault events
            num_fault_events = 0
            for iter_E in range(len(E)):
                if E[iter_E].isFault == 1:
                    num_fault_events += 1
            if num_fault_events != 0:
                counter_fault_events = 0
                text_alphabet = ""
                text_alphabet += "Fault events: ["
                chars_count = len(text_alphabet)
                for i in range(len(E)):
                    if E[i].isFault == 1:
                        if counter_fault_events < num_fault_events - 1:
                            current_text = str(E[i].label) + ", "
                        else:
                            current_text = str(E[i].label) + "]"
                        counter_fault_events += 1
                        text_alphabet += current_text
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
                    if len(current_start_filtered_deltas) == 0:
                        pass
                    else:
                        for iter_delta_row in range(len(current_start_filtered_deltas)):
                            if current_start_filtered_deltas.index[iter_delta_row] is not None:
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
            text_reachability = ""
            num_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 1:
                    num_reachable_states += 1
            if num_reachable_states != 0:
                counter_reachable_states = 0
                for i in range(len(X)):
                    if X[i].is_Reachable:
                        if counter_reachable_states < num_reachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_reachable_states += 1
                        text_reachability += current_text
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
            text_unreachability = ""
            num_unreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Reachable == 0:
                    num_unreachable_states += 1
            counter_unreachable_states = 0
            if num_unreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_Reachable == 0:
                        if counter_unreachable_states < num_unreachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unreachable_states += 1
                        text_unreachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unreachability += "\n                           "
                            chars_count = 0
            else:
                text_unreachability += "]"
            text_content += text_unreachability + "\n"

            text_content += "FSA is reachable? "
            if is_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Co-Reachability
            is_co_reachable = analysis.get_co_reachability_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nCO-REACHABLE STATES\n"
            text_content += "Co-reachable: ["
            chars_count = len("Co-reachable: [")
            text_co_reachability = ""
            num_co_reachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 1:
                    num_co_reachable_states += 1
            counter_co_reachable_states = 0
            if num_co_reachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable:
                        if counter_co_reachable_states < num_co_reachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_co_reachable_states += 1
                        text_co_reachability += current_text
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
            text_uncoreachability = ""
            num_uncoreachable_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_co_Reachable == 0:
                    num_uncoreachable_states += 1
            counter_uncoreachable_states = 0
            if num_uncoreachable_states != 0:
                for i in range(len(X)):
                    if X[i].is_co_Reachable == 0:
                        if counter_uncoreachable_states < num_uncoreachable_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_uncoreachable_states += 1
                        text_uncoreachability += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_uncoreachability += "\n                                "
                            chars_count = 0
            else:
                text_uncoreachability += "]"
            text_content += text_uncoreachability + "\n"

            text_content += "FSA is co-reachable? "
            if is_co_reachable == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Blocking
            is_blocking = analysis.get_blockingness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nBLOCKING STATES\n"
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
                        if counter_blocking_states < num_blocking_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_blocking_states += 1
                        text_blocking += current_text
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
            text_unblocking = ""
            num_unblocking_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Blocking == 0:
                    num_unblocking_states += 1
            counter_unblocking_states = 0
            if num_unblocking_states != 0:
                for i in range(len(X)):
                    if X[i].is_Blocking == 0:
                        if counter_unblocking_states < num_unblocking_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_unblocking_states += 1
                        text_unblocking += current_text
                        chars_count += len(current_text)
                        if chars_count >= num_chars_per_line:
                            text_unblocking += "\n                       "
                            chars_count = 0
            else:
                text_unblocking += "]"
            text_content += text_unblocking + "\n"

            text_content += "FSA is blocking? "
            if is_blocking == 1:
                text_content += "YES\n"
            else:
                text_content += "NO\n"


            # Dead
            analysis.get_deadness_info(f)
            num_chars_per_line = 50
            text_content += "______________________________________"
            text_content += "\nDEAD STATES\n"
            text_content += "Dead: ["
            chars_count = len("Dead: [")
            text_dead = ""
            num_dead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 1:
                    num_dead_states += 1
            counter_dead_states = 0
            if num_dead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead:
                        if counter_dead_states < num_dead_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_dead_states += 1
                        text_dead += current_text
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
            text_undead = ""
            num_undead_states = 0
            for iter_X in range(len(X)):
                if X[iter_X].is_Dead == 0:
                    num_undead_states += 1
            counter_undead_states = 0
            if num_undead_states != 0:
                for i in range(len(X)):
                    if X[i].is_Dead == 0:
                        if counter_undead_states < num_undead_states-1:
                            current_text = str(X[i].label) + ", "
                        else:
                            current_text = str(X[i].label) + "]"
                        counter_undead_states += 1
                        text_undead += current_text
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
            text_content += "\nTRIM\n"
            if is_trim == 1:
                text_content += "FSA is trim? YES\n"
            else:
                text_content += "FSA is trim? NO\n"

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "______________________________________"
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
                                                    filetypes=[("Text file","*.txt"),
                                                               ("All files","*.*")])
            if not filename:
                print ('Returning')
                return

            with open(filename, 'w') as fo:
                fo.write(text_content)
                fo.close()
            return

        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green", foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area widget with Read only by disabling the state
        text_area = st.ScrolledText(win, width=50, height=30, font=("Times New Roman", 12))

        text_area.grid(column=0, pady=10, padx=10)

        # Inserting Text which is read only
        text_area.insert(tk.INSERT, text_content)

        # Making the text read only
        text_area.configure(state='disabled')
        win.mainloop()

