import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage
#from tkintertable.Tables import TableCanvas


#global dictcolControllableEvents
#global dictcolObservableEvents
#global dictcolFaultyEvents
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
        print("columnlabels:", MyTable.model.columnlabels.values())
        # rows start from 0, columns start from 0

        json_dict = {"X": {}, "E": {}, "delta": {}}
        dict_X = {}
        dict_E = {}
        dict_delta = {}
        current_state = ""
        iter_ascii_delta = 65  # decimal value of the ASCII character 'A'
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
                            dict_delta.update({str(chr(iter_ascii_delta)): {"start": str(current_state), "name": str(
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

                            dict_E.update({current_key_event: {"isObservable": str(dictcolObservableEvents[current_key_event]),
                                                               "isControllable": str(
                                                                   dictcolControllableEvents[current_key_event]),
                                                               "isFault": str(
                                                                   dictcolFaultyEvents[current_key_event])}})
                            iter_ascii_delta += 1

                        print(current_delta_ends)
                else:
                    pass

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



