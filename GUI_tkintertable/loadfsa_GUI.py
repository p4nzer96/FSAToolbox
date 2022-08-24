import re
import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, ttk, Tk, Label, Toplevel, Button, Text, BOTH, \
    StringVar, VERTICAL, RIGHT, LEFT, Y, TOP
from tkinter import *

from tkinter import Canvas, NW
import pandas as pd

import GUI_Utils
from fsatoolbox import event, state, fsa

import os   # **********************************************************************************************************
from loadfsa import * # **********************************************************************************************************

import time

class fsa_GUI(fsa):
    """Inherit the class fsatoolbox.fsa """

    def __init__(self, X=None, E=None, delta=None, x0=None, Xm=None):
        super().__init__(X, E, delta, x0, Xm)


    def from_file_GUI(self, filename, bool_table=None):

        # Load from file

        X = []  # States
        E = []  # Alphabet
        x0 = []  # Initial states
        Xm = []  # Final states

        # File opening
        # **************************************************************************************************************
        jsonObject = {}
        if os.path.isfile(filename):
            path_components = filename.split("/")
            sheet_name = path_components[-1]
            extension = os.path.splitext(filename)
            # print("extension: ", extension)
            if ".txt" in extension or ".fsa" in extension:
                if ".txt" in extension:
                    GUI_Utils.last_sheet = sheet_name.replace(".txt", "")
                    GUI_Utils.last_extension = ".txt"
                if ".fsa" in extension:
                    GUI_Utils.last_sheet = sheet_name.replace(".fsa", "")
                    GUI_Utils.last_extension = ".fsa"
                # jsonObject = load_txt_or_fsa(filename)
                jsonObject = load_txt_or_fsa_GUI(filename)  # ***********************************************************
                # print("from_file_GUI")
                # print(jsonObject)
            elif ".csv" in extension:
                # jsonObject = load_csv(filename)
                GUI_Utils.last_sheet = sheet_name.replace(".csv", "")
                jsonObject = load_csv_GUI(filename)  # ******************************************************************
            elif ".json" in extension:
                if bool_table == 0:
                    GUI_Utils.last_sheet = sheet_name.replace(".json", "")
                print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}.json ...".format(GUI_Utils.last_sheet))
                with open(filename) as file:
                    jsonObject = json.load(file)
                    print("... successfully loaded {}.json.\r\n".format(GUI_Utils.last_sheet))
                    if bool_table != 1:
                        GUI_Utils.check_syntax_errors_in_json_file(jsonObject)
            else:
                text_content = "\r\nThe file you selected has extension not allowed. \r\n Please insert only '.txt, '.fsa', '.csv' or '.json' files.\r\n"
                # print(text_content)
                win = Tk()
                # Set the geometry of Tkinter frame
                win.geometry()
                win['background'] = '#fc5a27'
                win.title("Error parsing the file")
                Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(
                    pady=20)
                # Create a button in the main Window to open the popup
                win.mainloop()
                return

        # print("jsonObject: ", jsonObject)

        # Reading states and properties
        if jsonObject is None:
            raise TypeError

        # Reading states and properties

        state_properties = {"isInitial": None, "isFinal": None, "isForbidden": None}

        for state_name in jsonObject['X']:
            for prop in state_properties.keys():

                if prop in jsonObject['X'][state_name]:
                    state_properties[prop] = jsonObject['X'][state_name][prop]

            # Creating the state
            State = state(state_name,
                          bool(state_properties["isInitial"]),
                          bool(state_properties["isFinal"]),
                          bool(state_properties["isForbidden"]))

            if state_properties["isInitial"]:  # If the state is initial, add it to initial states
                x0.append(State)

            if state_properties["isFinal"]:  # If the state is final, add it to final states
                Xm.append(State)

            # Add the state to X
            X.append(State)

        event_properties = {"isObservable": None, "isControllable": None, "isFault": None}

        # Reading events and properties

        for event_name in jsonObject['E']:
            for prop in event_properties.keys():
                if prop in jsonObject['E'][event_name]:
                    event_properties[prop] = jsonObject['E'][event_name][prop]  # Is observable?

            # Creating the event
            Event = event(event_name,
                          event_properties["isObservable"],
                          event_properties["isControllable"],
                          event_properties["isFault"])

            E.append(Event)

        data = []

        # Reading delta

        for key in jsonObject['delta']:

            start_state = jsonObject['delta'][key]['start']  # Start state

            if start_state not in [s.label for s in X]:  # Check if start state is in X
                raise ValueError("Invalid start state")

            else:

                idx = [x.label for x in X].index(str(start_state))
                i_state = X[idx]

            transition = jsonObject['delta'][key]['name']  # Transition

            if transition not in [e.label for e in E]:  # Check if transition is in E
                raise ValueError("Invalid event")

            else:

                idx = [x.label for x in E].index(str(transition))
                trans = E[idx]

            end_state = jsonObject['delta'][key]['ends']

            if end_state not in [s.label for s in X]:  # Check if end state is in X
                raise ValueError("Invalid end state")

            else:

                idx = [x.label for x in X].index(str(end_state))
                f_state = X[idx]

            data.append([i_state, trans, f_state])

        delta = pd.DataFrame(data, columns=["start", "transition", "end"])

        self._X = X
        self._x0 = x0
        self._Xm = Xm
        self._delta = delta
        self._E = E


        '''
        if kwargs.get("name"):
            fsa_name = kwargs.get("name")
            return cls(X, E, delta, x0, Xm, name=fsa_name)

        return cls(X, E, delta, x0, Xm)
        '''



def open_popup_errors_on_txt_file():
    """Open popup if some errors are present on the .txt file describing the fsa"""
    from GUI_Utils import TablesApp
    TablesApp.example_win = Toplevel()
    # Set the geometry of tkinter frame
    TablesApp.example_win.geometry("1020x670")
    TablesApp.example_win.title("Example: how to populate a .txt or .fsa description file of the FSA")
    # Create a canvas
    canvas = Canvas(TablesApp.example_win, width=1000, height=670)
    # Load an image in the script
    img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_txt_file.png')
    # Add image to the Canvas Items
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    # Adding a scrollbar on the right
    my_scrollbar = ttk.Scrollbar(TablesApp.example_win, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=my_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    TablesApp.example_win.mainloop()
    return

def open_popup_errors_on_csv_file():
    """Open popup if some errors are present on the .csv file describing the fsa"""
    from GUI_Utils import TablesApp
    # Create an instance of tkinter frame
    TablesApp.example_win = Toplevel()
    # Set the geometry of tkinter frame
    TablesApp.example_win.geometry("780x760")
    TablesApp.example_win.title("Example: how to populate a .csv description file of the FSA")
    # Create a canvas
    canvas = Canvas(TablesApp.example_win, width=755, height=750)
    # Load an image in the script
    img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_csv_file.png')
    # Add image to the Canvas Items
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    # Adding a scrollbar on the right
    my_scrollbar = ttk.Scrollbar(TablesApp.example_win, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=my_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    TablesApp.example_win.mainloop()
    return


def open_popup_errors_on_json_file():
    """Open popup if some errors are present on the .json file describing the fsa"""
    from GUI_Utils import TablesApp
    # Create an instance of tkinter frame
    TablesApp.example_win = Toplevel()
    # Set the geometry of tkinter frame
    TablesApp.example_win.geometry("955x765")
    TablesApp.example_win.title("Example: how to populate a .json description file of the FSA")
    # Create a canvas
    canvas = Canvas(TablesApp.example_win, width=930, height=755)
    # Load an image in the script
    img = PhotoImage(format='png', file='./images/popup_example_how_to_populate_the_json_file.png')
    # Add image to the Canvas Items
    canvas.create_image(0, 0, anchor=NW, image=img)
    canvas.pack(side=LEFT, fill=BOTH, expand=1)
    # Adding a scrollbar on the right
    my_scrollbar = ttk.Scrollbar(TablesApp.example_win, orient=VERTICAL, command=canvas.yview)
    my_scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=my_scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    TablesApp.example_win.mainloop()
    return



def load_txt_or_fsa_GUI(filename=None):
    """Parse the .txt file describing the fsa and it returns a json dictionary of the fsa"""
    # print("load_txt_or_fsa_GUI")

    print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}{} ...".format(GUI_Utils.last_sheet, GUI_Utils.last_extension))
    fd = open(filename, mode='rt')
    print("... successfully loaded {}{}.\r\n".format(GUI_Utils.last_sheet,GUI_Utils.last_extension))
    lines = fd.readlines()
    jsonObject = {"X": {}, "E": {}, "delta": {}}

    clean_lines = []
    counter_not_allowed_empty_lines = 0
    list_not_allowed_empty_lines = []
    for iter_list in range(len(lines)):
        clean_lines.append(lines[iter_list])
        clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
        clean_lines[iter_list] = re.sub(" +", " ", clean_lines[iter_list])
        clean_lines[iter_list] = clean_lines[iter_list].split(" ")
        if clean_lines[iter_list][0] == '' and len(clean_lines[iter_list]) == 1:
            counter_not_allowed_empty_lines += 1
            if counter_not_allowed_empty_lines >= 2 or iter_list == len(lines) - 1:
                list_not_allowed_empty_lines.append(iter_list + 1)
        else:
            counter_not_allowed_empty_lines = 0
            try:
                while True:
                    clean_lines[iter_list].remove('')
            except ValueError:
                pass
    fd.close()
    # print("clean_lines: ", clean_lines)
    # print("list_not_allowed_empty_lines: ", list_not_allowed_empty_lines)

    if len(clean_lines) == 0:
        print("Syntax error:\t\t\t\tThe file is empty. Please fill it.")
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title("Error parsing the file")
        win['background'] = '#fc5a27'
        Label(win,
              text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + GUI_Utils.last_extension + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                                                   "(Look at the terminal to see all the errors)\r\n\n"
                                                                                                                   "Click the button below if you want to see an example on how to correctly populate the file.",
              font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_txt_file).pack()
        win.mainloop()
        return




    flag_missing_num_states = 0
    if clean_lines[0][0] != '':
        if clean_lines[0][0].isnumeric() is not True:
            flag_missing_num_states = 1
            print(
                "Syntax error in line 1:\t\t\tThe number of states specified at the beginning of the file ('{}') is not an 'integer', please modify it.".format(
                    clean_lines[0][0]))
    else:
        flag_missing_num_states = 1
        print(
            "Syntax error in line 1:\t\t\tThe number of states must be specified at the beginning of the file, please insert it.")

    if len(list_not_allowed_empty_lines) != 0 or flag_missing_num_states == 1:
        if len(list_not_allowed_empty_lines) != 0:
            for iter_lnael in range(len(list_not_allowed_empty_lines)):
                if (list_not_allowed_empty_lines[iter_lnael] < 10):
                    print("Syntax error in line " + str(
                        list_not_allowed_empty_lines[iter_lnael]) + ":\t\t\tEmpty line not allowed. Please correct the error to continue the parsing.")
                else:
                    print("Syntax error in line " + str(
                        list_not_allowed_empty_lines[iter_lnael]) + ":\t\tEmpty line not allowed. Please correct the error to continue the parsing.")

        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title("Error parsing the file")
        win['background'] = '#fc5a27'
        Label(win, text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + str(GUI_Utils.last_extension) + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                            "(Look at the terminal to see all the errors)\r\n\n"
                            "Click the button below if you want to see an example on how to "
                            "correctly populate the file.", font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_txt_file).pack()
        win.mainloop()
        return


    dict_start_states = {}  # to populate column 0 with keys (states), and for every key a dictionary of info on isInitial, isFinal, isFault
    list_start_states = []  # the indexes of the list represent the row of the related the start_state value
    list_events = []  # to populate columnlabels with keys (events), and for every key a dictionary of info on isObservable, isControllable

    flag_more_than_one_same_state = 0  # when in the column of states has been specified the same state more times
    flag_more_than_one_same_event = 0  # when has been specified the same event more times

    dict_events = {}
    dict_deltas = {}
    index_row_start_states = 0
    index_column_events = 1  # the index '0' is for the column "States", so the events start from column '1'
    index_delta_events = 0
    current_start_state = ""
    flag_the_next_line_is_a_state = 0
    iter_lines = 1
    flag_exception_happened = 0
    num_corrupted_states = 0
    flag_syntax_error = 0

    # try:
    num_states = int(clean_lines[0][0])
    while iter_lines < len(clean_lines):
        if clean_lines[iter_lines][0] == '' and flag_the_next_line_is_a_state == 0:
            if len(dict_start_states) < num_states:
                flag_the_next_line_is_a_state = 1
                iter_lines += 1
            else:
                break  # all the states and their deltas have been parsed, but there are other blak lines after
        elif flag_the_next_line_is_a_state == 1:
            current_start_state = str(clean_lines[iter_lines][0])
            # print("current_start_state: ", current_start_state)
            if current_start_state not in dict_start_states:
                try:
                    bool_init = (clean_lines[iter_lines][1] == '1' or clean_lines[iter_lines][1] == '0')
                    bool_final = (clean_lines[iter_lines][2] == '1' or clean_lines[iter_lines][2] == '0')
                    bool_forbidden = (clean_lines[iter_lines][3] == '1' or clean_lines[iter_lines][3] == '0')
                    if bool_init and bool_final and bool_forbidden:
                        dict_start_states.update({current_start_state: {"line": iter_lines+1,
                                                                        "isInitial": int(clean_lines[iter_lines][1]),
                                                                        "isFinal": int(clean_lines[iter_lines][2]),
                                                                        "isForbidden": int(clean_lines[iter_lines][3])}})
                        list_start_states.append(current_start_state)
                        index_row_start_states += 1
                    else:
                        num_corrupted_states += 1
                        str_bool_init = ""
                        str_bool_final = ""
                        str_bool_forbidden = ""
                        if bool_init == 0:
                            str_bool_init = "\t\tcol 2('"+str(clean_lines[iter_lines][1])+"') must be '1' or '0'"
                        if bool_final == 0:
                            str_bool_final = "\t\tcol 3('"+str(clean_lines[iter_lines][2])+"') must be '1' or '0'"
                        if bool_forbidden == 0:
                            str_bool_forbidden = "\t\tcol 4('"+str(clean_lines[iter_lines][3])+"') must be '1' or '0'"
                        flag_syntax_error = 1
                        print("Syntax error in state line " + str(iter_lines+1) + ':' + str(str_bool_init) + str(str_bool_final) + str(str_bool_forbidden) + '.')
                except:
                    flag_syntax_error = 1
                    num_corrupted_states += 1
                    print("Syntax error in state line " + str(
                        iter_lines + 1) + ":\t\tThe state properties of '{}' are not completely defined (insert in order Initial(1/0), Final(1/0), Forbidden(1/0) after the state).".format(
                        current_start_state))
            else:
                flag_syntax_error = 1
                flag_more_than_one_same_state = 1
                # print("Syntax error in state line:" + str(iter_lines+1))
                # print("current_start_state: ", str(current_start_state))
                # print("dict_start_states[current_start_state]['line']: " + str(dict_start_states[current_start_state]["line"]))
                print("Syntax error in state line " + str(iter_lines+1) + ":\t\tMultiple occurrence of the state '{}', already specified in line {}." .format(current_start_state, dict_start_states[current_start_state]["line"]))
            flag_the_next_line_is_a_state = 0
            iter_lines += 1
        elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0 and len(clean_lines[iter_lines]) >= 5:
            bool_c_uc = (clean_lines[iter_lines][2] == 'c' or clean_lines[iter_lines][2] == 'uc')
            bool_o_uo = (clean_lines[iter_lines][3] == 'o' or clean_lines[iter_lines][3] == 'uo')
            bool_f_uf = (clean_lines[iter_lines][4] == 'f' or clean_lines[iter_lines][4] == 'uf')
            if bool_c_uc and bool_o_uo and bool_f_uf:
                flag_end_current_start_state = 0
                while flag_end_current_start_state == 0:
                    bool_event = 0
                    current_event = clean_lines[iter_lines][0]
                    if len(clean_lines[iter_lines]) >= 5:
                        # print("iter_lines: " + str(iter_lines) + ", len:" + str(len(clean_lines[iter_lines])))
                        bool_event = current_event in dict_events and \
                        (clean_lines[iter_lines][2] != dict_events[current_event]["isControllable"] \
                        or clean_lines[iter_lines][3] != dict_events[current_event]["isObservable"] \
                        or clean_lines[iter_lines][4] != dict_events[current_event]["isFault"])

                        if clean_lines[iter_lines][0] in dict_start_states:
                            print(
                                "Syntax warning:\t\t\t\tThe event '{}' specified in line {} has the same name as the state '{}' defined in line {}. Please ignore this warning if this is the correct behaviour.".format(
                                    clean_lines[iter_lines][0], iter_lines + 1, clean_lines[iter_lines][0],
                                    dict_start_states[clean_lines[iter_lines][0]]["line"]))


                        if clean_lines[iter_lines][0] not in dict_events:
                            dict_events.update({clean_lines[iter_lines][0]: {"line": iter_lines + 1,
                                                                         "isControllable": clean_lines[iter_lines][2],
                                                                         "isObservable": clean_lines[iter_lines][3],
                                                                         "isFault": clean_lines[iter_lines][4]}})
                            list_events.append(clean_lines[iter_lines][0])
                            dict_deltas.update({str(index_delta_events): {"line": iter_lines+1,
                                                                        "start": current_start_state,
                                                                         "name": current_event,
                                                                        "ends": clean_lines[iter_lines][1]}})
                            index_column_events += 1
                            index_delta_events += 1
                        elif clean_lines[iter_lines][0] in dict_events:
                            dict_deltas.update({str(index_delta_events): {"line": iter_lines+1,
                                                                      "start": current_start_state,
                                                                      "name": clean_lines[iter_lines][0],
                                                                      "ends": clean_lines[iter_lines][1]}})
                            index_delta_events += 1
                    else:
                        flag_syntax_error = 1
                        bool_event = 0
                        print("Syntax error in event line " + str(
                            iter_lines + 1) + ":\t\tFive column elements are required in this event line, or maybe it is needed a blank line above this line.")

                    if (iter_lines + 1) < len(clean_lines) and clean_lines[iter_lines + 1][0] != '':
                        iter_lines += 1  # reiteration of while flag_end_current_start_state == 0:
                        flag_the_next_line_is_a_state = 0
                    else:
                        iter_lines += 1  # reiteration of while iter_lines < len(clean_lines):
                        flag_end_current_start_state = 1  # exit from the while loop
                        flag_the_next_line_is_a_state = 0

                    if bool_event == 1:
                        flag_syntax_error = 1
                        print("Syntax error in event line " + str(iter_lines) + ":\t\tThe event in this line ('{}') has different properties respect to its first declaration in line {}.".format(current_event, dict_events[current_event]["line"]))

            else:
                str_bool_c_uc = ""
                str_bool_o_uo = ""
                str_bool_f_uf = ""
                if bool_c_uc == 0:
                    str_bool_c_uc = "\t\tcol 3('" + str(clean_lines[iter_lines][2]) + "') must be 'c' or 'uc'"
                if bool_o_uo == 0:
                    str_bool_o_uo = "\t\tcol 4('" + str(clean_lines[iter_lines][3]) + "') must be 'o' or 'uo'"
                if bool_f_uf == 0:
                    str_bool_f_uf = "\t\tcol 5('" + str(clean_lines[iter_lines][4]) + "') must be 'f' or 'uf'"
                flag_syntax_error = 1
                print("Syntax error in event line " + str(iter_lines + 1) + ':' + str(str_bool_c_uc) + str(str_bool_o_uo) + str(str_bool_f_uf) +'.')
                iter_lines += 1
        elif clean_lines[iter_lines][0] != '' and flag_the_next_line_is_a_state == 0 and len(clean_lines[iter_lines]) < 5:
            flag_syntax_error = 1
            print("Syntax error in event line " + str(iter_lines + 1) + ":\t\tFive column elements are required in this event line.")
            iter_lines += 1
    if len(dict_start_states) + num_corrupted_states != num_states:
        flag_syntax_error = 1
        print("Syntax error in line 1:\t\t\tThe number of possible states found in the file ({}) does not correspond to the number of states specified at the beginning of the file ({}).".format(len(dict_start_states) + num_corrupted_states, num_states))

    #print("dict_start_states: ", dict_start_states)
    # print("dict_events: ", dict_events)
    #print("dict_deltas: ", dict_deltas)

    for key_E in dict_events:
        # del dict_events[key_E]["line"]
        bool_controllable = 1 if dict_events[key_E]["isControllable"] == 'c' else 0
        bool_observable = 1 if dict_events[key_E]["isObservable"] == 'o' else 0
        bool_fault = 1 if dict_events[key_E]["isFault"] == 'f' else 0
        # del dict_events[key_E]
        dict_events.update({key_E: {"isControllable": bool_controllable,
                                    "isObservable": bool_observable,
                                    "isFault": bool_fault}})

    for key_delta in dict_deltas:
        #print("dict_deltas[{}]['ends']={}".format(key_delta, dict_deltas[key_delta]["ends"]))
        if dict_deltas[key_delta]["ends"] not in dict_start_states:
            flag_end_state_not_a_state = 1
            print("Syntax error in event line " + str(
                dict_deltas[key_delta]["line"]) + ":\t\tThe end-state '{}' is not a defined state (or well defined).".format(
                dict_deltas[key_delta]["ends"]))

    for key_delta in dict_deltas:
        del dict_deltas[key_delta]["line"]

    for key_X in dict_start_states:
        del dict_start_states[key_X]["line"]

    # except:
    if flag_syntax_error == 1:
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title("Error parsing the file")
        win['background'] = '#fc5a27'
        Label(win,
              text="Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + str(GUI_Utils.last_extension) + "':\r\n\nThere are some syntax error in the file you tried to import.\r\n"
                                                                                        "(Look at the terminal to see all the errors)\r\n\n"
                                                                                        "Click the button below if you want to see an example on how to "
                                                                                        "correctly populate the file.",
              font=('Helvetica 10 bold'), background='#fc9150', justify='center').pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_txt_file).pack()
        win.mainloop()
        return

    '''
    flag_zero_initial_states = 0
    flag_more_than_one_initial_state = 0
    counter_initial_states = 0
    for keyX in dict_start_states:
        if dict_start_states[keyX]["isInitial"] == 1 or dict_start_states[keyX]["isInitial"] == "1":
            counter_initial_states += 1
    if counter_initial_states > 1:
        flag_more_than_one_initial_state = 1
    elif counter_initial_states == 0:
        flag_zero_initial_states = 1

    flag_event_state = 0
    list_E = list(dict_events.keys())
    for keyX in dict_start_states:
        if keyX in list_E:
            flag_event_state = 1

    flag_different_number_of_states = 0
    flag_end_state_not_a_state = 0
    list_X = list(dict_start_states.keys())


    
    if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
            or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
        title_content = "Analysis problems"
        text_content = "Some problems occurred:\r\n"
        statements_counter = 0
        width_list = []
        if flag_different_number_of_states == 1:
            statements_counter += 1
            text_content += str(statements_counter) + ".ERROR: The number of states is different from the actual number " \
                                                      "that have been specified at the beginning of the file.\n"
            width_list.append(1000)
        if flag_zero_initial_states == 1:
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: the 'initial state' has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                width_list.append(1000)
            else:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: the 'initial state' has not been specified.\n"
                width_list.append(500)
        if flag_more_than_one_initial_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state'.\n"
            width_list.append(500)
        if flag_end_state_not_a_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: only 'states' specified at the beginning of every group are allowed as 'end states' of a transition.\n"
            width_list.append(900)
        if flag_event_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state'(ignore this warning if it is the desired behaviour).\n"
            width_list.append(900)
        if flag_more_than_one_same_state == 1:
            statements_counter += 1
            text_content += str(
                statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
            width_list.append(600)
        if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_state == 1 or flag_different_number_of_states == 1:
            text_content += "Please correct the content of the file.\n"

        # auto-adapative height of the popup
        win_geometry_height = 70 + 52 * statements_counter
        width_popup = str(max(width_list))+"x"
        win_geometry = width_popup + str(win_geometry_height)

        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        win.geometry()
        win.title(title_content)
        win['background'] = '#fc5a27'
        Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify='left').pack(pady=20)
        # Create a button in the main Window to open the popup
        win.mainloop()
        return
    '''



    jsonObject["X"].update(dict_start_states)
    jsonObject["E"].update(dict_events)
    jsonObject["delta"].update(dict_deltas)
    # print(jsonObject)
    return jsonObject

def load_csv_GUI(filename=None):
    """Parse the .csv file describing the fsa and it returns a json dictionary of the fsa"""

    print("\r\n\r\n" + time.ctime() + "\n" + chr(62) + "   Loading {}.csv ...".format(GUI_Utils.last_sheet))
    fd = open(filename, mode='rt')
    print("... loaded {}.csv.\r\n".format(GUI_Utils.last_sheet))
    lines = fd.readlines()
    clean_lines = []
    for iter_list in range(len(lines)):
        clean_lines.append(lines[iter_list])
        clean_lines[iter_list] = clean_lines[iter_list].replace("\t", " ")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\r", "")
        clean_lines[iter_list] = clean_lines[iter_list].replace("\n", "")
        clean_lines[iter_list] = re.sub(" +", "", clean_lines[iter_list])
        clean_lines[iter_list] = clean_lines[iter_list].split(",")
    fd.close()

    # Assigning a csv label to every column, like:
    # A ... Z      AA, AB, AC ... AZ      BA, BB, BC ... BZ     CA, CB, CC ... CZ     ZA, ZB, ZC ... ZZ     AAA, AAB, AAC ... AAZ   ABA, ABB, ABC ... ABZ
    csv_col_label = ['A']
    str_csv_col_label = ""
    current_iterating_csv_col_label = 0
    index_to_change = 0
    last_char_csv_col_label = ""
    dict_csv_col_label = {}
    for iter_col in range(len(clean_lines[0])):
        ascii_counter = 65 + iter_col % 26
        # print(ascii_counter)
        current_iterating_csv_col_label = chr(ascii_counter)
        # print(current_iterating_csv_col_label)
        # print("current_iterating_csv_col_label: ", current_iterating_csv_col_label)
        # print("index_to_change: ", index_to_change)
        csv_col_label[index_to_change] = current_iterating_csv_col_label

        # csv_col_label.insert(current_iterating_csv_col_label, last_char_csv_col_label)
        str_csv_col_label = ''.join(csv_col_label)
        # print("str_csv_col_label: ", str_csv_col_label)
        dict_csv_col_label.update({str(iter_col): str_csv_col_label})
        # print(dict_csv_col_label)
        if ascii_counter >= 90:

            # print(ascii_counter)
            # ascii_counter_prev = 65 + iter_col % 26
            # current_iterating_csv_col_label += 1
            bool_all_Zs = all(element == 'Z' for element in csv_col_label)


            # print("len(csv_col_label): ", len(csv_col_label))
            if bool_all_Zs:
                num_current_chars_on_label = len(csv_col_label)
                for i in range(num_current_chars_on_label):
                    csv_col_label[i] = 'A'
                # print("index_to_change: ", index_to_change)
                index_to_change = len(csv_col_label)
                csv_col_label.insert(len(csv_col_label), 'A')
                # index_to_change = num_current_chars_on_label

            else:
                current_iterating_index = index_to_change
                for j in range(current_iterating_index, 0, -1):
                    # print("j: ", j)
                    if csv_col_label[j] == 'Z' and csv_col_label[j - 1] != 'Z':
                        # index_to_change -= 1
                        index_to_change = current_iterating_index
                        csv_col_label[j] = 'A'
                        csv_col_label[j - 1] = chr(ord(csv_col_label[j - 1]) + 1)


            # print("csv_col_label: ", csv_col_label)

    # print(dict_csv_col_label)

    # check missing event name (empty event name but not empty column)
    flag_empty_event = 0
    for i in range(len(clean_lines[0])):
        temp_clean_lines_row0 = clean_lines[0][i]
        if temp_clean_lines_row0 == '':
            flag_empty_event = 1
            print("Syntax error in event col {}:\t\tEvent name not specified, please insert it.".format(dict_csv_col_label[str(i)]))


    # check missing state name (empty state name but not empty row)
    flag_empty_state = 0
    for j in range(len(clean_lines)):
        if clean_lines[j][0] == '':
            flag_empty_state = 1
            print("Syntax error in row {}, col A:\t\tState name not specified, please insert it.".format(str(j+1)))

    if flag_empty_state == 1 or flag_empty_event == 1:
        win = Tk()
        # Set the geometry of Tkinter frame
        # win.geometry(win_geometry)
        text_cntnt = ""
        text_cntnt += "Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + ".csv':\r\n"
        if flag_empty_state == 1:
            text_cntnt += "- One or more of the State names are not specified (empty), please insert it/them.\r\n"
        if flag_empty_event == 1:
            text_cntnt += "- One or more of the event names are not specified (empty), please insert it/them.\r\n"
        text_cntnt += "\nPlease look at the terminal for more accurate info, and correct the content of the file.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the file."
        win.geometry()
        win['background'] = '#fc5a27'
        win.title("Error parsing the file")
        Label(win, text=text_cntnt, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
        win.mainloop()
        return



    flag_more_than_one_same_state = 0  # when in the column of states has been specified the same state more times
    flag_more_than_one_same_event = 0  # when has been specified the same event more times

    jsonObject = {"X": {}, "E": {}, "delta": {}}
    dict_X = {}
    dict_E = {}
    dict_delta = {}
    list_columns = []
    dict_events_first_csv_col = {}


    # parsing events
    for i in range(1, len(clean_lines[0])):
        current_event = clean_lines[0][i]
        if clean_lines[0][i] and clean_lines[0][i] != '_':
            if current_event.endswith("_uc_f_uo") or current_event.endswith("_uc_uo_f") or current_event.endswith(
                    "_f_uc_uo") or current_event.endswith("_f_uo_uc") or current_event.endswith(
                "_uo_f_uc") or current_event.endswith("_uo_uc_f"):
                substring_to_remove = current_event[-8:]
                current_event = current_event.replace(str(substring_to_remove), "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print("Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(dict_csv_col_label[
                        str(i)], current_event, dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_f"):
                current_event = current_event.replace("_uc_f", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_f_uc"):
                current_event = current_event.replace("_f_uc", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_uo"):
                current_event = current_event.replace("_uc_uo", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_uc"):
                current_event = current_event.replace("_uo_uc", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_f"):
                current_event = current_event.replace("_uo_f", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_f_uo"):
                current_event = current_event.replace("_f_uo", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uc"):
                current_event = current_event.replace("_uc", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 1, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_f"):
                current_event = current_event.replace("_f", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 1, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uo"):
                current_event = current_event.replace("_uo", "")
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 0, "isControllable": 1, "isFault": 0}})
            else:
                current_event = re.sub(" +", "", current_event)
                if current_event not in dict_E:
                    dict_events_first_csv_col.update({current_event: i})
                else:
                    flag_more_than_one_same_event = 1
                    print(
                        "Syntax error in event col {}:\t\tMultiple occurrence of the event '{}', already specified in col {}.".format(
                            dict_csv_col_label[
                                str(i)], current_event,
                            dict_csv_col_label[str(dict_events_first_csv_col[current_event])]))
                dict_E.update({current_event: {"col": i, "isObservable": 1, "isControllable": 1, "isFault": 0}})
            list_columns.append(current_event)


    dict_states_first_csv_row = {}
    # parsing states
    current_state = ""
    iter_delta_key = 0
    num_rows = len(clean_lines)
    num_cols = len(clean_lines[0])
    # ascii_counter = 65  # char A
    initial_state = ""
    flag_initial_state_found = 0
    dict_initial_states_found = {}

    for iter_row in range(1, num_rows):
        for iter_col in range(num_cols):
            if clean_lines[iter_row][iter_col] != None:
                current_cell = clean_lines[iter_row][iter_col]
                if iter_col == 0:
                    if current_cell[0] and current_cell[0] != '_':
                        if current_cell.endswith("_i_f_p") or current_cell.endswith(
                                "_i_p_f") or current_cell.endswith("_f_i_p") or current_cell.endswith(
                            "_f_p_i") or current_cell.endswith("_p_f_i") or current_cell.endswith("_p_i_f"):
                            substring_to_remove = current_cell[-6:]
                            current_state = current_cell.replace(str(substring_to_remove), "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1, "isForbidden": 1}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_i_f"):
                            current_state = current_cell.replace("_i_f", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_f_i"):
                            current_state = current_cell.replace("_f_i", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 1, "isForbidden": 0}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_i_p"):
                            current_state = current_cell.replace("_i_p", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_p_i"):
                            current_state = current_cell.replace("_p_i", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0, "isForbidden": 1}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_p_f"):
                            current_state = current_cell.replace("_p_f", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1, "isForbidden": 1}})

                        elif current_cell.endswith("_f_p"):
                            current_state = current_cell.replace("_f_p", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1, "isForbidden": 1}})

                        elif current_cell.endswith("_i"):
                            current_state = current_cell.replace("_i", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 1, "isFinal": 0, "isForbidden": 0}})
                            dict_initial_states_found.update({str(iter_row + 1): {"state": current_state}})
                            if flag_initial_state_found == 0:
                                initial_state = str(current_state)
                                flag_initial_state_found = 1

                        elif current_cell.endswith("_f"):
                            current_state = current_cell.replace("_f", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 1, "isForbidden": 0}})

                        elif current_cell.endswith("_p"):
                            current_state = current_cell.replace("_p", "")
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print(
                                    "Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                        str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state,
                                        dict_states_first_csv_row[str(current_state)],
                                        dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 0, "isForbidden": 1}})

                        else:
                            current_state = current_cell
                            current_state = re.sub(" +", " ", current_state)
                            if str(current_state) not in dict_X:
                                dict_states_first_csv_row.update({str(current_state): iter_row + 1})
                            else:
                                flag_more_than_one_same_state = 1
                                print("Syntax error in row {}, col {}:\t\tMultiple occurrence of the state '{}', already specified in row {}, col {}.".format(
                                    str(iter_row + 1), dict_csv_col_label[str(iter_col)], current_state, dict_states_first_csv_row[str(current_state)], dict_csv_col_label[str(iter_col)]))
                            dict_X.update(
                                {str(current_state): {"row": iter_row + 1, "isInitial": 0, "isFinal": 0, "isForbidden": 0}})


                    else:
                        #TODO: make a try except in this if-else
                        print("Syntax error:\t\tCell(" + str(iter_row) + "," + str(iter_col) + " is not a valid name for a state.\nPlease insert a valid one.")
                else:
                    current_delta_ends = current_cell.split("-")
                    flag_end_while = 0
                    while (flag_end_while == 0):
                        if '' in current_delta_ends:
                            current_delta_ends.remove('')
                        else:
                            flag_end_while = 1

                    for i in range(len(current_delta_ends)):
                        dict_delta.update({str(iter_delta_key): {"start": str(current_state), "name": list_columns[iter_col-1], "ends": str(current_delta_ends[i])}})
                        current_key_event = clean_lines[iter_row][iter_col]
                        iter_delta_key += 1

            else:
                pass



    # print("dict_X: ", dict_X)
    # print("dict_E: ", dict_E)
    # print("dict_delta: ", dict_delta)

    flag_zero_initial_states = 0
    flag_more_than_one_initial_state = 0
    counter_initial_states = 0

    for key_init in dict_initial_states_found:
        counter_initial_states += 1
        if dict_initial_states_found[key_init]["state"] != initial_state:
            print("Syntax error in row {}, col {}:\t\tAnother initial state has been specified ('{}'), while the first defined was already specified in row {} as '{}'.".format(key_init, dict_csv_col_label[str(0)],
                      dict_initial_states_found[key_init]["state"], dict_states_first_csv_row[initial_state], initial_state))

    if counter_initial_states > 1:
        flag_more_than_one_initial_state = 1
    elif counter_initial_states == 0:
        flag_zero_initial_states = 1

    flag_event_state = 0
    list_E = list(dict_E.keys())
    for keyX in dict_X:
        if keyX in list_E:
            # flag_event_state = 1  # it is better not to use a popup to advertise the user of the Warning, or the FSA analysis cannot procede
            print("Syntax warning:\t\t\t\tThe event '{}' of col {} is named as the state '{}' of row {}. Please ignore this warning if this is the correct behaviour." .format(keyX, dict_csv_col_label[str(dict_E[keyX]["col"])], keyX, dict_X[keyX]["row"]))


    flag_end_state_not_a_state = 0
    if flag_more_than_one_same_state == 0:
        list_X = list(dict_X.keys())
        for keydelta in dict_delta:
            if dict_delta[keydelta]["ends"] not in list_X:
                flag_end_state_not_a_state = 1
                if flag_more_than_one_same_event == 0:
                    print("Syntax error in row {}, col {}:\t\tThe end-state '{}' specified in this cell is not defined in the column 'State'." .format(dict_X[dict_delta[keydelta]["start"]]["row"], dict_csv_col_label[str(dict_E[dict_delta[keydelta]["name"]]["col"])], dict_delta[keydelta]["ends"]))

    flag_error = flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                 or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1

    if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
            or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
        title_content = "Error parsing the file"
        text_content = "Some problems occurred while parsing the file '" + GUI_Utils.last_sheet + ".csv':\r\n"
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
            text_content += "\nPlease look at the terminal for more accurate info, and correct the content of the file.\n\n\nAlso click the button below if you want to see an example on how to correctly populate the file."

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
        Label(win, text=text_content, font=('Helvetica 10 bold'), background='#fc9150', justify="left").pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
        win.mainloop()
        if flag_error == 1:
            return

    for key_X in dict_X:
        del dict_X[key_X]["row"]

    for key_E in dict_E:
        del dict_E[key_E]["col"]

    jsonObject["X"] = dict_X
    jsonObject["delta"] = dict_delta
    jsonObject["E"] = dict_E
    return jsonObject

