import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, ttk, Tk, Label, Toplevel, Button, Text, BOTH, \
    StringVar
from tkinter.ttk import Frame
#from tkintertable.Tables import TableCanvas


#global dictcolControllableEvents
#global dictcolObservableEvents
#global dictcolFaultyEvents
from tkinter.ttk import Combobox

dictcolObservableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolControllableEvents = {'event1': 1, 'event2': 1, 'event3': 1, 'event4': 1}
dictcolFaultyEvents = {'event1': 0, 'event2': 0, 'event3': 0, 'event4': 0}


# added by me ******************************************************************************************************
def setEventAsUnobservable(MyTable, column_name=None):
    """Set the event as Unobservable - can be used in a table header"""
    print("setEventAsUnobservable")
    global dictcolObservableEvents
    if column_name == None:
        n = messagebox.askyesno("Setting",
                                "Unobservable Event?")
        if n:


            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolObservableEvents[str(current_col_name)] = 0
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Observable events:", dictcolObservableEvents)
    else:
        dictcolObservableEvents[str(column_name)] = 0


# ******************************************************************************************************************


# added by me ******************************************************************************************************
def setEventAsObservable(MyTable, column_name=None):
    """Set the event as Observable - can be used in a table header"""
    print("setEventAsObservable")

    global dictcolObservableEvents
    if column_name == None:

        n = messagebox.askyesno("Setting",
                                "Observable Event?")
        if n:
            # global dictcolObservableEvents
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolObservableEvents[str(current_col_name)] = 1
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Observable events:", dictcolObservableEvents)
    else:
        dictcolObservableEvents[str(column_name)] = 1
        # print(current_col_index)
        # print(str(self.model.getColumnLabel(current_col_index)))
        print("Observable events:", dictcolObservableEvents)


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setEventAsUncontrollable(MyTable, column_name=None):
    """Set the event as Uncontrollable - can be used in a table header"""
    print("setEventAsUncontrollable")

    global dictcolControllableEvents

    if column_name == None:

        n = messagebox.askyesno("Setting",
                                "Uncontrollable Event?")
        if n:
            # global dictcolControllableEvents
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolControllableEvents[str(current_col_name)] = 0
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Controllable events:", dictcolControllableEvents)
    else:
        dictcolControllableEvents[str(column_name)] = 0


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setEventAsControllable(MyTable, column_name=None):
    """Set the event as Controllable - can be used in a table header"""
    print("setEventAsControllable")

    global dictcolControllableEvents

    if column_name == None:

        n = messagebox.askyesno("Setting",
                                "Controllable Event?")
        if n:
            # global dictcolControllableEvents
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolControllableEvents[str(current_col_name)] = 1
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Controllable events:", dictcolControllableEvents)
    else:
        dictcolControllableEvents[str(column_name)] = 1


# ******************************************************************************************************************


# added by me ******************************************************************************************************
def setEventAsFaulty(MyTable, column_name=None):
    """Set the event as Faulty - can be used in a table header"""
    print("setEventAsFaulty")

    global dictcolFaultyEvents

    if column_name == None:
        n = messagebox.askyesno("Setting",
                                "Faulty Event?")
        if n:
            # global dictcolFaultyEvents

            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolFaultyEvents[str(current_col_name)] = 1
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Faulty events:", dictcolFaultyEvents)
    else:
        dictcolFaultyEvents[str(column_name)] = 1


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setEventAsUnfaulty(MyTable, column_name=None):
    """Set the event as Unfaulty - can be used in a table header"""
    print("setEventAsUnfaulty")

    global dictcolFaultyEvents

    if column_name == None:

        n = messagebox.askyesno("Setting",
                                "Observable Event?")
        if n:
            # global dictcolFaultyEvents
            current_col_index = MyTable.getSelectedColumn()
            current_col_name = MyTable.model.getColumnLabel(current_col_index)
            dictcolFaultyEvents[str(current_col_name)] = 0
            # print(current_col_index)
            # print(str(self.model.getColumnLabel(current_col_index)))
            print("Faulty events:", dictcolFaultyEvents)
    else:
        dictcolFaultyEvents[str(column_name)] = 0
        # print(current_col_index)
        # print(str(self.model.getColumnLabel(current_col_index)))
        print("Faulty events:", dictcolFaultyEvents)


# ******************************************************************************************************************


# added by me *******************************************************************************************************
def fromTableToJson(MyTable):
    """Convert the current table content into a Json file"""
    print("fromTableToJson")

    global dictcolControllableEvents
    global dictcolObservableEvents
    global dictcolFaultyEvents

    # Algorithm of conversion of the current table to a json file
    n = messagebox.askyesno("Convert",
                            "Convert table to json file?",
                            parent=MyTable.parentframe)
    if n:

        flag_more_than_one_same_state = 0 # when in the column of states has been specified the same state more times
        flag_more_than_one_same_event = 0 # when has been specified the same event more times

        list_columnlabels = list(MyTable.model.columnlabels.values())
        for i in range(len(list_columnlabels)):
            if list_columnlabels.count(list_columnlabels[i]) > 1:
                flag_more_than_one_same_event = 1

        print("columnlabels:", MyTable.model.columnlabels.values())
        # rows start from 0, columns start from 0

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
                print("iter_row,iter_col:" + str(iter_row) + "," + str(iter_col))
                if MyTable.model.getCellRecord(iter_row, iter_col) != None:
                    current_cell = MyTable.model.getCellRecord(iter_row, iter_col)
                    print("current_cell: ", current_cell)
                    if iter_col == 0:
                        if current_cell[0] and current_cell[0] != '_':
                            if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                    "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                                    "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                                string_lenght = len(current_cell)
                                substring_to_remove = current_cell[-6:]
                                current_state = current_cell.replace(str(substring_to_remove), "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_i_f"):
                                current_state = current_cell.replace("_i_f", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_f_i"):
                                current_state = current_cell.replace("_f_i", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_i_p"):
                                current_state = current_cell.replace("_i_p", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            elif current_cell.endswith("_p_i"):
                                current_state = current_cell.replace("_p_i", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            elif current_cell.endswith("_p_f"):
                                current_state = current_cell.replace("_p_f", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_f_p"):
                                current_state = current_cell.replace("_f_p", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 1}})
                            elif current_cell.endswith("_i"):
                                current_state = current_cell.replace("_i", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 1, "isFinal": 0, "isForbidden": 0}})
                            elif current_cell.endswith("_f"):
                                current_state = current_cell.replace("_f", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 1, "isForbidden": 0}})
                            elif current_cell.endswith("_p"):
                                current_state = current_cell.replace("_p", "")
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 1}})
                            else:
                                current_state = current_cell
                                current_state.replace(" ", "")
                                if current_state in dict_X:
                                    flag_more_than_one_same_state = 1
                                dict_X.update(
                                    {str(current_state): {"isInitial": 0, "isFinal": 0, "isForbidden": 0}})
                        else:
                            print("cell(" + str(iter_row) + "," + str(
                                iter_col) + " is not a valid name for a state.\nPlease insert a valid one.")
                    else:
                        current_delta_ends = current_cell.split("-")
                        flag_end_while = 0
                        while (flag_end_while == 0):
                            if '' in current_delta_ends:
                                current_delta_ends.remove('')
                            else:
                                flag_end_while = 1

                        for i in range(len(current_delta_ends)):
                            dict_delta.update({str(iter_delta_key): {"start": str(current_state), "name": str(
                                MyTable.model.getColumnLabel(iter_col)), "ends": str(current_delta_ends[i])}})
                            print("dict_delta", dict_delta)
                            current_key_event = str(MyTable.model.getColumnLabel(iter_col))

                            '''
                            if current_key_event.endswith("_uc_f_uo") or current_key_event.endswith(
                                    "_uc_uo_f") or current_key_event.endswith(
                                    "_f_uc_uo") or current_key_event.endswith("_f_uo_uc") or current_key_event.endswith(
                                "_uo_f_uc") or current_key_event.endswith("_uo_uc_f"):
                                print("_uc_f_uo")
                                string_lenght = len(current_key_event)
                                substring_to_remove = current_key_event[-6:]
                                current_key_event = current_key_event.replace(str(substring_to_remove), "")
                            elif current_key_event.endswith("_uc_f"):
                                print("_uc_f")
                                current_key_event = current_key_event.replace("_uc_f", "")
                            elif current_key_event.endswith("_f_uc"):
                                print("_f_uc")
                                current_key_event = current_key_event.replace("_f_uc", "")
                            elif current_key_event.endswith("_uc_uo"):
                                print("_uc_uo")
                                current_key_event = current_key_event.replace("_uc_uo", "")
                            elif current_key_event.endswith("_uo_uc"):
                                print("_uo_uc")
                                current_key_event = current_key_event.replace("_uo_uc", "")
                            elif current_key_event.endswith("_uo_f"):
                                print("_uo_f")
                                current_key_event = current_key_event.replace("_uo_f", "")
                            elif current_key_event.endswith("_f_uo"):
                                print("_f_uo")
                                current_key_event = current_key_event.replace("_f_uo", "")
                            elif current_key_event.endswith("_uc"):
                                print("_uc")
                                current_key_event = current_key_event.replace("_uc", "")
                            elif current_key_event.endswith("_f"):
                                print("_f")
                                current_key_event = current_key_event.replace("_f", "")
                            elif current_key_event.endswith("_uo"):
                                print("_uo")
                                current_key_event = current_key_event.replace("_uo", "")
                            '''

                            dict_E.update({current_key_event: {"isObservable": dictcolObservableEvents[current_key_event],
                                                               "isControllable":
                                                                   dictcolControllableEvents[current_key_event],
                                                               "isFault":
                                                                   dictcolFaultyEvents[current_key_event]}})
                            iter_delta_key += 1

                        print(current_delta_ends)
                else:
                    pass

        print(dict_X)

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
            win_geometry = ""
            if flag_zero_initial_states == 1:
                if flag_more_than_one_same_state == 1:
                    statements_counter += 1
                    text_content += str(statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                    win_geometry = "950x"
                else:
                    statements_counter += 1
                    text_content += str(statements_counter) + ".ERROR: the 'initial state' (_i) has not been specified.\n"
                    win_geometry = "500x"
            if flag_more_than_one_initial_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state' (_i).\n"
                win_geometry = "500x"
            if flag_end_state_not_a_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: only 'states' specified in the column 'State' are allowed as 'end states' of a transition.\n"
                win_geometry = "700x"
            if flag_event_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state' like those in the first column (ignore this warning if it is the desired behaviour).\n"
                win_geometry = "950x"
            if flag_more_than_one_same_event == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: an 'event' can be defined only once (only one column per 'event').\n"
                win_geometry = "500x"
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
                win_geometry = "950x"
            if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
                text_content += "Please correct the content of the table.\n"


            # auto-adapative height of the popup
            win_geometry_height = 70 + 52 * statements_counter
            win_geometry += str(win_geometry_height)

            win = Tk()
            # Set the geometry of Tkinter frame
            win.geometry(win_geometry)
            # win.aspect(70,70,70,70)
            win.title(title_content)
            Label(win, text=text_content, font=('Helvetica 10 bold')).pack(pady=20)
            # Create a button in the main Window to open the popup
            # ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()


        json_dict["X"] = dict_X
        json_dict["delta"] = dict_delta
        json_dict["E"] = dict_E
        print(json_dict)

        with open("sample.json", "w") as outfile:
            # json_object = json.dumps(json_dict, outfile, indent=4 )
            json.dump(json_dict, outfile, indent=4)

        # print("cella 1,1", self.model.getCellRecord(1,1))

        outfile.close()
        print("Tabella convertita in un json file")

    return


# ******************************************************************************************************************


# added by me *******************************************************************************************************
def from_table_to_json():
# def fromTableToJson():
    img = PhotoImage(format='png', file='./venv/Lib/site-packages/tkintertable/logo_convert_to_json.png', height=32, width=32)
    return img
# ******************************************************************************************************************

# added by me *******************************************************************************************************
def analyze_fsa():
    img = PhotoImage(format='png', file='./venv/Lib/site-packages/tkintertable/logo_analyze_fsa.png', height=32, width=32)
    return img
# ******************************************************************************************************************


import os
from tkintertable.Prefs import Preferences
class TablesApp(Frame):
    """
    Tables app
    """

    def __init__(self, parent=None, data=None, datafile=None):
        "Initialize the application."
        #print("TablesApp__init__")
        super().__init__()
        self.parent = parent

        #If there is data to be loaded, show the dialog first
        if not self.parent:
            Frame.__init__(self)
            self.tablesapp_win = self.master
        else:
            self.tablesapp_win=Toplevel()

        # Get platform into a variable
        import platform
        self.currplatform=platform.system()
        if not hasattr(self,'defaultsavedir'):
            self.defaultsavedir = os.getcwd()

        #self.preferences=Preferences('TablesApp',{'check_for_update':1})
        # self.loadprefs()
        self.tablesapp_win.title('Save')
        self.tablesapp_win.geometry('+40+40')
        self.x_size=800
        self.y_size=600
        # self.createMenuBar()
        #self.apptoolBar = ToolBar(self.tablesapp_win, self)
        #self.apptoolBar.pack(fill=BOTH, expand=NO)
        # add find bar TODO
        # self.createSearchBar()


        #self.tablesapp_win.protocol('WM_DELETE_WINDOW',self.quit)
        return

# added by me ******************************************************************************************************
def analyzeFsa(MyTable):

    n = messagebox.askyesno("Analyze",
                            "Analyze the FSA?",
                            parent=MyTable.parentframe)
    if n:

        from fsatoolbox.fsa import fsa
        import analysis
        # f = fsa()

        # f.from_file('file_co-reach-for-Xm.json')

        f = fsa.from_file('sample.json')
        # f = fsa.from_file('fsa.csv')
        # f = fsa.from_file('fsa.txt')

        # print(getattr(f, "X"))

        # X = []  # States
        # E = []  # Alphabet
        # x0 = []  # Initial states
        # Xm = []  # Final states
        # delta = pd.DataFrame()
        # filtered_delta = []

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta



        if x0:
            print("TEST AREA:")
            print("Stati: ", X)
            print("Stati iniziali: ", x0)
            print("Stati finali: ", Xm)
            print("Eventi/alfabeto: ", E)
            print("Transizioni delta dataFrame view:\n", delta)

            print("\n REACHABILITY TEST:")
            is_reachable = analysis.get_reachability_info(f)

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Reachable: " + str(X[iter].is_Reachable))
            print("The FSA is Reachable? :" + str(is_reachable))

            print("\n CO-REACHABILITY TEST:")
            is_co_reachable = analysis.get_co_reachability_info(f)

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_co_Reachable: " + str(X[iter].is_co_Reachable))
            print("The FSA is Co-Reachable? :" + str(is_co_reachable))

            print("\n BLOCKINGNESS TEST:")
            is_blocking = analysis.get_blockingness_info(f)

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Blocking: " + str(X[iter].is_Blocking))
            print("The FSA is blocking? :" + str(is_blocking))

            print("\n TRIM TEST:")
            is_trim = analysis.get_trim_info(f)
            print("The FSA is trim? :" + str(is_trim))

            print("\n DEADNESS TEST:")
            analysis.get_deadness_info(f)

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Dead: " + str(X[iter].is_Dead))

            print("\n REVERSIBILITY TEST:")
            is_reversible = analysis.get_reversibility_info(f)
            print("The FSA is reversible? :" + str(is_reversible))
        else:
            print("Error: At least the initial state must be specified.")


        num_chars_per_line = 50
        text_content = ""
        if x0:
            text_content += "FSA 5-TUPLA:\n"
            # states
            text_states = ""
            text_states += "States: ["
            chars_count = len(text_states)
            for i in range(len(X) - 1):
                current_text = str(X[i]) + ", "
                text_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_states += "\n           "
                    chars_count = 0
            text_states += str(X[len(X) - 1]) + "]\n"
            text_content += text_states

            # initial states
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            chars_count = len(text_initial_states)
            for i in range(len(x0) - 1):
                current_text = str(x0[i]) + ", "
                text_initial_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_initial_states += "\n                    "
                    chars_count = 0
            text_initial_states += str(x0[len(x0) - 1]) + "]\n"
            text_content += text_initial_states

            # final states
            if Xm:
                text_final_states = ""
                text_final_states += "Final states: ["
                chars_count = len(text_final_states)
                for i in range(len(Xm) - 1):
                    current_text = str(Xm[i]) + ", "
                    text_final_states += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_final_states += "\n                   "
                        chars_count = 0
                text_final_states += str(Xm[len(Xm) - 1]) + "]\n"
                text_content += text_final_states
            else:
                text_content += "Final states: []\n"

            # alphabet
            if E:
                text_alphabet = ""
                text_alphabet += "Alphabet: ["
                chars_count = len(text_alphabet)
                for i in range(len(E) - 1):
                    current_text = str(E[i]) + ", "
                    text_alphabet += current_text
                    chars_count += len(current_text)
                    if chars_count >= num_chars_per_line:
                        text_alphabet += "\n                "
                        chars_count = 0
                text_alphabet += str(E[len(E) - 1]) + "]\n"
                text_content += text_alphabet
            else:
                text_content += "Alphabet: []\n"


            # delta transitions
            if len(delta):
                text_delta = "\n"
                text_delta += "Delta transitions:\n"
                text_delta += str(delta)
                text_content += text_delta + "\n"
            else:
                text_content += "Delta transitions: []\n"

            # Reachability
            is_reachable = analysis.get_reachability_info(f)
            text_content += "\nREACHABILITY:\n"
            text_reachability = ""
            for i in range(len(X)):
                text_reachability += str(X[i].label) + " is reachable?: " + str(X[i].is_Reachable) + "\n"
            text_content += text_reachability

            text_content += "The FSA is reachable? :" + str(is_reachable) + "\n"

            # Co-Reachability
            is_co_reachable = analysis.get_co_reachability_info(f)
            text_content += "\nCO-REACHABILITY:\n"
            text_co_reachability = ""
            for i in range(len(X)):
                text_co_reachability += str(X[i].label) + " is co-reachable?: " + str(X[i].is_co_Reachable) + "\n"
            text_content += text_co_reachability

            text_content += "The FSA is co-reachable? :" + str(is_co_reachable) + "\n"

            # Blockingness
            is_blocking = analysis.get_blockingness_info(f)
            text_content += "\nBLOCKINGNESS:\n"
            text_blockingness = ""
            for i in range(len(X)):
                text_blockingness += str(X[i].label) + " is blocking?: " + str(X[i].is_Blocking) + "\n"
            text_content += text_blockingness

            text_content += "The FSA is blocking? :" + str(is_blocking) + "\n"

            # Deadness
            analysis.get_deadness_info(f)
            text_content += "\nDEADNESS:\n"
            text_deadness = ""
            for i in range(len(X)):
                text_deadness += str(X[i].label) + " is dead?: " + str(X[i].is_Dead) + "\n"
            text_content += text_deadness

            # Trim
            is_trim = f.get_trim_info()
            text_content += "\nTRIM:\n"
            text_content += "The FSA is trim? :" + str(is_trim) + "\n"

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "\nREVERSIBILITY:\n"
            text_content += "The FSA is reversible? :" + str(is_reversible)

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
            # showinfo(title='Information', message='Download button clicked!')
            """Save as a new filename"""
            ta = TablesApp(Frame)
            filename = filedialog.asksaveasfilename(parent=ta.tablesapp_win,
                                                defaultextension='.txt',
                                                initialdir=ta.defaultsavedir,
                                                filetypes=[("Text file","*.txt"),
                                                           ("All files","*.*")])
            if not filename:
                print ('Returning')
                return

            with open(filename, 'w') as f:
                f.write(text_content)
            return



        importButton = Button(win, text='Save on file', command=save_fsa_analysis_results, background="green", foreground="white")
        importButton.grid(row=20, column=0, sticky='news', padx=2, pady=2)

        # Creating scrolled text area
        # widget with Read only by
        # disabling the state
        text_area = st.ScrolledText(win, width=50, height=30, font=("Times New Roman", 12))

        text_area.grid(column=0, pady=10, padx=10)

        # Inserting Text which is read only
        text_area.insert(tk.INSERT, text_content)

        # Making the text read only
        text_area.configure(state='disabled')
        win.mainloop()



'''
# added by me ******************************************************************************************************
def analyzeFsa(MyTable):

    n = messagebox.askyesno("Analyze",
                            "Analyze the FSA?",
                            parent=MyTable.parentframe)
    if n:

        from fsatoolbox.fsa import fsa
        import analysis
        f = fsa()

        # f.from_file('file_co-reach-for-Xm.json')

        # f = fsa.from_file('sample.json')
        # f = fsa.from_file('fsa.csv')
        f = fsa.from_file('fsa.txt')

        # print(getattr(f, "X"))

        # X = []  # States
        # E = []  # Alphabet
        # x0 = []  # Initial states
        # Xm = []  # Final states
        # delta = pd.DataFrame()
        # filtered_delta = []

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta

        # filtered_delta = f.filter_delta(start='x2', transition=None, end=None)


        from tkintertable.Tables_IO import TableImporter
        import tkinter as tk
        root = Tk()

        # specify size of window.
        root.geometry("500x600")

        # Create text widget and specify size.
        T = Text(root, height=450, width=560)

        # Create label
        l = Label(root, text="Analysis results of the FSA")
        l.config(font=("Courier", 14))

        # Create a scrollbar
        scroll_bar = tk.Scrollbar(root)

        # Pack the scroll bar
        # Place it to the right side, using tk.RIGHT
        scroll_bar.pack(side=tk.RIGHT, fill="y")


        num_chars_per_line = 40
        text_content = ""
        if x0:
            text_content += "FSA 5-TUPLA:\n"
            # states
            text_states = ""
            text_states += "States: ["
            chars_count = len(text_states)
            for i in range(len(X)-1):
                current_text = str(X[i]) + ", "
                text_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_states += "\n"
                    chars_count = 0
            text_states += str(X[len(X)-1]) + "]\n"
            text_content += text_states
            
            # initial states
            text_initial_states = ""
            text_initial_states += "Initial states: ["
            chars_count = len(text_initial_states)
            for i in range(len(x0)-1):
                current_text = str(x0[i]) + ", "
                text_initial_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_initial_states += "\n"
                    chars_count = 0
            text_initial_states += str(x0[len(x0)-1]) + "]\n"
            text_content += text_initial_states
            
            # final states
            text_final_states = ""
            text_final_states += "Final states: ["
            chars_count = len(text_final_states)
            for i in range(len(Xm)-1):
                current_text = str(Xm[i]) + ", "
                text_final_states += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_final_states += "\n"
                    chars_count = 0
            text_final_states += str(Xm[len(Xm)-1]) + "]\n"
            text_content += text_final_states
            
            # alphabet
            text_alphabet = ""
            text_alphabet += "Alphabet: ["
            chars_count = len(text_alphabet)
            for i in range(len(E)-1):
                current_text = str(E[i]) + ", "
                text_alphabet += current_text
                chars_count += len(current_text)
                if chars_count >= num_chars_per_line:
                    text_alphabet += "\n"
                    chars_count = 0
            text_alphabet += str(E[len(E)-1]) + "]\n"
            text_content += text_alphabet

            # delta transitions
            text_delta = "\n"
            text_delta += "Delta transitions:\n"
            text_delta += str(delta)
            text_content += text_delta + "\n"

            # Reachability
            is_reachable = analysis.get_reachability_info(f)
            text_content += "\nREACHABILITY:\n"
            text_reachability = ""
            for i in range(len(X)):
                text_reachability += str(X[i].label) + " is reachable?: " + str(X[i].is_Reachable) + "\n"
            text_content += text_reachability

            text_content += "The FSA is reachable? :" + str(is_reachable) + "\n"

            # Co-Reachability
            is_co_reachable = analysis.get_co_reachability_info(f)
            text_content += "\nCO-REACHABILITY:\n"
            text_co_reachability = ""
            for i in range(len(X)):
                text_co_reachability += str(X[i].label) + " is co-reachable?: " + str(X[i].is_co_Reachable) + "\n"
            text_content += text_co_reachability

            text_content += "The FSA is co-reachable? :" + str(is_co_reachable) + "\n"

            # Blockingness
            is_blocking = analysis.get_blockingness_info(f)
            text_content += "\nBLOCKINGNESS:\n"
            text_blockingness = ""
            for i in range(len(X)):
                text_blockingness += str(X[i].label) + " is blocking?: " + str(X[i].is_Blocking) + "\n"
            text_content += text_blockingness

            text_content += "The FSA is blocking? :" + str(is_blocking) + "\n"

            # Deadness
            analysis.get_deadness_info(f)
            text_content += "\nDEADNESS:\n"
            text_deadness = ""
            for i in range(len(X)):
                text_deadness += str(X[i].label) + " is dead?: " + str(X[i].is_Dead) + "\n"
            text_content += text_deadness

            # Trim
            is_trim = f.get_trim_info()
            text_content += "\nTRIM:\n"
            text_content += "The FSA is trim? :" + str(is_trim) + "\n"

            # Reversibility
            is_reversible = analysis.get_reversibility_info(f)
            text_content += "\nREVERSIBILITY:\n"
            text_content += "The FSA is reversible? :" + str(is_reversible) + "\n"





            print("TEST AREA:")
            print("Stati: ", X)
            print("Stati iniziali: ", x0)
            print("Stati finali: ", Xm)
            print("Eventi/alfabeto: ", E)
            print("Transizioni delta dataFrame view:\n", delta)



        else:
            text_content = "Error: At least the initial state must be specified."




        # Create button for next text.
        b1 = Button(root, text="Next", )

        # Create an Exit button.
        b2 = Button(root, text="Exit",
                    command=root.destroy)

        l.pack()
        T.pack()
        b1.pack()
        b2.pack()

        # Insert The Fact.
        T.insert(tk.END, text_content)

        tk.mainloop()



# ******************************************************************************************************************
'''



'''
# added by me ******************************************************************************************************
def analyzeFsa(MyTable):

    n = messagebox.askyesno("Analyze",
                            "Analyze the FSA?",
                            parent=MyTable.parentframe)
    if n:

        from fsatoolbox.fsa import fsa
        f = fsa()

        # f.from_file('file_co-reach-for-Xm.json')
        f.from_file('sample.json')
        # print(getattr(f, "X"))

        # X = []  # States
        # E = []  # Alphabet
        # x0 = []  # Initial states
        # Xm = []  # Final states
        # delta = pd.DataFrame()
        # filtered_delta = []

        X = f.X
        E = f.E
        x0 = f.x0
        Xm = f.Xm
        delta = f.delta

        # filtered_delta = f.filter_delta(start='x2', transition=None, end=None)

        if x0:
            print("TEST AREA:")
            print("Stati: ", X)
            print("Stati iniziali: ", x0)
            print("Stati finali: ", Xm)
            print("Eventi/alfabeto: ", E)
            print("Transizioni delta dataFrame view:\n", delta)

            print("\n REACHABILITY TEST:")
            is_reachable = f.get_reachability_info()

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Reachable: " + str(X[iter].is_Reachable))
            print("The FSA is Reachable? :" + str(is_reachable))

            print("\n CO-REACHABILITY TEST:")
            is_co_reachable = f.get_co_reachability_info()

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_co_Reachable: " + str(X[iter].is_co_Reachable))
            print("The FSA is Co-Reachable? :" + str(is_co_reachable))

            print("\n BLOCKINGNESS TEST:")
            is_blocking = f.get_blockingness_info()

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Blocking: " + str(X[iter].is_Blocking))
            print("The FSA is blocking? :" + str(is_blocking))

            print("\n TRIM TEST:")
            is_trim = f.get_trim_info()
            print("The FSA is trim? :" + str(is_trim))

            print("\n DEADNESS TEST:")
            f.get_deadness_info()

            for iter in range(len(X)):
                print("X[" + str(iter) + "].is_Dead: " + str(X[iter].is_Dead))

            print("\n REVERSIBILITY TEST:")
            is_reversible = f.get_reversibility_info()
            print("The FSA is reversible? :" + str(is_reversible))
        else:
            print("Error: At least the initial state must be specified.")

# ******************************************************************************************************************
'''






# added by me ******************************************************************************************************
def setCurrentEventAsUnobservable(TableCanvas):
    """Set the event as Unobservable - can be used in a table header"""
    print("setCurrentEventAsUnobservable")

    n = messagebox.askyesno("Setting",
                            "Unobservable Event?")
    if n:
        # global dictcolObservableEvents
        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)

        # current_col_name = TableCanvas.getSelectedColumn()
        dictcolObservableEvents[str(current_col_name)] = 0
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Observable events:", dictcolObservableEvents)


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setCurrentEventAsObservable(TableCanvas):
    """Set the event as Observable - can be used in a table header"""
    print("setCurrentEventAsObservable")

    n = messagebox.askyesno("Setting",
                            "Observable Event?")
    if n:
        # global dictcolObservableEvents
        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)
        dictcolObservableEvents[str(current_col_name)] = 1
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Observable events:", dictcolObservableEvents)


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setCurrentEventAsUncontrollable(TableCanvas):
    """Set the event as Uncontrollable - can be used in a table header"""
    print("setCurrentEventAsUncontrollable")

    n = messagebox.askyesno("Setting",
                            "Uncontrollable Event?")
    if n:
        # global dictcolControllableEvents
        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)
        dictcolControllableEvents[str(current_col_name)] = 0
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Controllable events:", dictcolControllableEvents)


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setCurrentEventAsControllable(TableCanvas):
    """Set the event as Controllable - can be used in a table header"""
    print("setCurrentEventAsControllable")

    n = messagebox.askyesno("Setting",
                            "Controllable Event?")
    if n:
        # global dictcolControllableEvents
        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)
        dictcolControllableEvents[str(current_col_name)] = 1
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Controllable events:", dictcolControllableEvents)


# ******************************************************************************************************************


# added by me ******************************************************************************************************
def setCurrentEventAsFaulty(TableCanvas):
    """Set the event as Faulty - can be used in a table header"""
    print("setCurrentEventAsFaulty")

    n = messagebox.askyesno("Setting",
                            "Faulty Event?")
    if n:
        # global dictcolFaultyEvents

        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)
        dictcolFaultyEvents[str(current_col_name)] = 1
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Faulty events:", dictcolFaultyEvents)


# ******************************************************************************************************************

# added by me ******************************************************************************************************
def setCurrentEventAsUnfaulty(TableCanvas):
    """Set the event as Unfaulty - can be used in a table header"""
    print("setCurrentEventAsUnfaulty")

    n = messagebox.askyesno("Setting",
                            "Observable Event?")
    if n:
        # global dictcolFaultyEvents
        current_col_index = TableCanvas.getSelectedColumn()
        current_col_name = TableCanvas.model.getColumnLabel(current_col_index)
        dictcolFaultyEvents[str(current_col_name)] = 0
        # print(current_col_index)
        # print(str(TableCanvas.model.getColumnLabel(current_col_index)))
        print("Faulty events:", dictcolFaultyEvents)


# ******************************************************************************************************************


def initialize():

    dictcolObservableEvents = {'event1':1, 'event2':1, 'event3':1, 'event4':1}
    dictcolControllableEvents = {'event1':1, 'event2':1, 'event3':1, 'event4':1}
    dictcolFaultyEvents = {'event1':0, 'event2':0, 'event3':0, 'event4':0}



