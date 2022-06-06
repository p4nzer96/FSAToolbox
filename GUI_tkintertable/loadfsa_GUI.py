import re
import json
from tkinter import filedialog, messagebox, simpledialog, PhotoImage, ttk, Tk, Label, Toplevel, Button, Text, BOTH, \
    StringVar
from tkinter.ttk import Frame
from tkinter import Canvas, NW


from tkinter import Canvas, NW

def open_popup_errors_on_txt_file():
    """Open popup if some errors are present on the .txt file describing the fsa"""
    from my_globals import TablesApp
    TablesApp.example_win = Toplevel()

    # Set the geometry of tkinter frame
    TablesApp.example_win.geometry("1000x670")
    TablesApp.example_win.title("Example: how to populate a .txt description file of the FSA")
    # Create a canvas
    canvas = Canvas(TablesApp.example_win, width=1000, height=670)
    canvas.pack()
    # Load an image in the script
    img = PhotoImage(format='png', file='./popup_example_how_to_populate_the_txt_file.png')
    # Add image to the Canvas Items
    canvas.create_image(10, 10, anchor=NW, image=img)
    TablesApp.example_win.mainloop()

    # create the text widget
    # text = Text(TablesApp.ab_win, height=900, width=2800)
    # text.grid(row=0, column=0, sticky='ew')

    # create a scrollbar widget and set its command to the text widget
    # scrollbar = ttk.Scrollbar(TablesApp.ab_win, orient='vertical', command=text.yview)
    # scrollbar.grid(row=0, column=2700, sticky='ns')

    #  communicate back to the scrollbar
    # text['yscrollcommand'] = scrollbar.set

    return
# ******************************************************************************************************************


def open_popup_errors_on_csv_file():
    """Open popup if some errors are present on the .csv file describing the fsa"""

    from my_globals import TablesApp

    # Create an instance of tkinter frame
    TablesApp.example_win = Toplevel()
    # Set the geometry of tkinter frame
    TablesApp.example_win.geometry("740x720")
    TablesApp.example_win.title("Example: how to populate a .csv description file of the FSA")
    # Create a canvas
    canvas = Canvas(TablesApp.example_win, width=730, height=710)
    canvas.pack()
    # Load an image in the script
    img = PhotoImage(format='png', file='./popup_example_how_to_populate_the_csv_file.png')

    # Add image to the Canvas Items
    canvas.create_image(10, 10, anchor=NW, image=img)

    TablesApp.example_win.mainloop()

    return

# ******************************************************************************************************************




def load_txt_or_fsa_GUI(filename=None):
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


    flag_more_than_one_same_state = 0  # when in the column of states has been specified the same state more times
    flag_more_than_one_same_event = 0  # when has been specified the same event more times

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

    flag_exception_happened = 0
    try:
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

                current_start_state = str(clean_lines[iter_lines][0])
                print("current_start_state: ", current_start_state)
                if current_start_state in dict_start_states:
                    flag_more_than_one_same_state = 1

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

    except:
        flag_exception_happened = 1
        # Create an instance of Tkinter frame
        win = Tk()
        # Set the geometry of Tkinter frame
        win.geometry("400x200")
        # win.aspect(70,70,70,70)
        Label(win, text="There are some sintax error in the .txt file you tried to import.\r\n"
                        "Click here if you want to see an example on how to\r\ncorrectly populate the file.",
              font=('Helvetica 10 bold')).pack(pady=20)
        # Create a button in the main Window to open the popup
        ttk.Button(win, text="Example", command=open_popup_errors_on_txt_file).pack()
        win.mainloop()




    if flag_exception_happened == 0:
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
        try:
            for keydelta in dict_deltas:
                if dict_deltas[keydelta]["ends"] not in list_X:
                    flag_end_state_not_a_state = 1
        except:
            flag_different_number_of_states = 1



        if flag_event_state == 1 or flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                or flag_zero_initial_states == 1 or flag_more_than_one_same_event == 1 or flag_more_than_one_same_state == 1:
            title_content = "Analysis problems"
            text_content = "Some problems occurred:\r\n"
            statements_counter = 0
            win_geometry = ""

            if flag_different_number_of_states == 1:
                statements_counter += 1
                text_content += str(statements_counter) + ".ERROR: The number of states is different from the actual number " \
                                                          "that have been specified at the beginning of the file.\n"
                win_geometry = "500x"
            if flag_zero_initial_states == 1:
                if flag_more_than_one_same_state == 1:
                    statements_counter += 1
                    text_content += str(
                        statements_counter) + ".ERROR: the 'initial state' has not been specified or it could have been overwritten by the same 'state' specified more than once.\n"
                    win_geometry = "950x"
                else:
                    statements_counter += 1
                    text_content += str(statements_counter) + ".ERROR: the 'initial state' has not been specified.\n"
                    win_geometry = "500x"
            if flag_more_than_one_initial_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: only one 'state' can be specified as an 'initial state'.\n"
                win_geometry = "500x"
            if flag_end_state_not_a_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: only 'states' specified at the beginning of every group are allowed as 'end states' of a transition.\n"
                win_geometry = "700x"
            if flag_event_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".WARNING: one or many 'events' is/are named as a 'state'(ignore this warning if it is the desired behaviour).\n"
                win_geometry = "950x"
            if flag_more_than_one_same_state == 1:
                statements_counter += 1
                text_content += str(
                    statements_counter) + ".ERROR: a 'state' can be defined only once (only one row per 'state').\n"
                win_geometry = "950x"
            if flag_end_state_not_a_state == 1 or flag_more_than_one_initial_state == 1 \
                    or flag_zero_initial_states == 1 or flag_more_than_one_same_state == 1 or flag_different_number_of_states == 1:
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
            return

    jsonObject["X"].update(dict_start_states)
    jsonObject["E"].update(dict_events)
    jsonObject["delta"].update(dict_deltas)

    #print("from txt to jsonobject:", jsonObject)
    return jsonObject


def load_csv_GUI(filename=None):
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
    #for row in range(1, len(clean_lines)):
    #for col in range(0, len(clean_lines[0])):
    #print("(row, col): ("+str(row)+","+str(col)+")"+": "+str(clean_lines[row][col]))
    #pass

    flag_more_than_one_same_state = 0  # when in the column of states has been specified the same state more times
    flag_more_than_one_same_event = 0  # when has been specified the same event more times

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
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_f"):
                current_event = current_event.replace("_uc_f", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_f_uc"):
                current_event = current_event.replace("_f_uc", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
            elif current_event.endswith("_uc_uo"):
                current_event = current_event.replace("_uc_uo", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_uc"):
                current_event = current_event.replace("_uo_uc", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_uo_f"):
                current_event = current_event.replace("_uo_f", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_f_uo"):
                current_event = current_event.replace("_f_uo", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uc"):
                current_event = current_event.replace("_uc", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 0}})
            elif current_event.endswith("_f"):
                current_event = current_event.replace("_f", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 1}})
            elif current_event.endswith("_uo"):
                current_event = current_event.replace("_uo", "")
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 0}})
            else:
                current_event.replace(" ", "")
                if current_event in dict_E:
                    flag_more_than_one_same_event = 1
                dict_E.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 0}})
            #print("current_event: ", current_event)
            list_columns.append(current_event)

    current_state = ""
    iter_delta_key = 0
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
                        dict_delta.update({str(iter_delta_key): {"start": str(current_state), "name": list_columns[iter_col-1], "ends": str(current_delta_ends[i])}})
                        # print("dict_delta", dict_delta)
                        current_key_event = clean_lines[iter_row][iter_col]
                        iter_delta_key += 1

                    # print(current_delta_ends)
            else:
                pass

    print("dict_X: ", dict_X)
    print("dict_E: ", dict_E)
    print("dict_delta: ", dict_delta)

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
        title_content = "Analysis problems"
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
            text_content += "Please correct the content of the table.\n\nClick here if you want to see an example on how to correctly populate the file."


        # auto-adapative height of the popup
        win_geometry_height = 100 + 52 * statements_counter
        win_geometry += str(win_geometry_height)

        win = Tk()
        # Set the geometry of Tkinter frame
        win.geometry(win_geometry)
        # win.aspect(70,70,70,70)
        win.title(title_content)
        Label(win, text=text_content, font=('Helvetica 10 bold')).pack(pady=20)
        # Create a button in the main Window to open the popup
        # ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()

        ttk.Button(win, text="Example", command=open_popup_errors_on_csv_file).pack()
        
        win.mainloop()
        return


    jsonObject["X"] = dict_X
    jsonObject["delta"] = dict_delta
    jsonObject["E"] = dict_E
    # print(jsonObject)

    return jsonObject

