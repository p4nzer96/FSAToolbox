
from __future__ import absolute_import, division, print_function




# from tkintertable import TableCanvas, TableModel




#import Pmw
import re, sys, os, time, pickle

script_dir = os.path.dirname( __file__ )
tkintertable_dir = os.path.join( script_dir, 'venv', 'Lib', 'site-packages')
sys.path.append(tkintertable_dir)

from collections import OrderedDict
from tkintertable.Custom import MyTable
from tkintertable.TableModels import TableModel
from tkintertable.Tables_IO import TableImporter
from tkintertable.Prefs import Preferences


# added by me **********************************************************************************************************

import io

# from tkintertable.Tables import *
#from tkintertable.Tables import dictcolObservableEvents
#from tkintertable.Tables import dictcolControllableEvents
#from tkintertable.Tables import dictcolFaultyEvents


# from tkintertable.Tables import TableCanvas
from tkinter import ttk

# from PIL import Image, ImageTk
# import PIL.Image, PIL.ImageTk
# import PIL.Image, PIL.ImageTk

import json
import my_globals

# **********************************************************************************************************************


try:
    from tkinter import *
    from tkinter.ttk import *
    import tkMessageBox
except:
    pass
    #from Tkinter import *
    #from ttk import *
if sys.version_info > (3, 0):
    from tkinter import filedialog, messagebox, simpledialog
    from tkinter import font
else:
    from tkinter import filedialog
    from tkinter import simpledialog
    from tkinter import messagebox
    from tkinter import font







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

        self.preferences=Preferences('TablesApp',{'check_for_update':1})
        self.loadprefs()
        self.tablesapp_win.title('Tables Application')
        self.tablesapp_win.geometry('+200+200')
        self.x_size=800
        self.y_size=600
        self.createMenuBar()
        self.apptoolBar = ToolBar(self.tablesapp_win, self)
        self.apptoolBar.pack(fill=BOTH, expand=NO)
        # add find bar TODO
        # self.createSearchBar()


        if data != None:
            self.data = data
            self.new_project(data)
        elif datafile != None:
            self.open_project(datafile)
        else:
            self.new_project()

        self.tablesapp_win.protocol('WM_DELETE_WINDOW',self.quit)
        return

    def print_some_table_value_test(self):
        #print("**************************************")
        #print("getSelectedColumn: ", self.currenttable.getSelectedColumn())
        #print("getSelectedRow: ", self.currenttable.getSelectedRow())
        list_cols = self.currenttable.model.columnlabels.values()
        #print("list_cols: ", list_cols)
        #print("getColumnLabel: ", self.currenttable.model.getColumnLabel(0))
        #print("getValueAt: ", self.currenttable.model.getValueAt(self.currenttable.getSelectedColumn(), self.currenttable.getSelectedRow()))
        #print("getRowCount: ", self.currenttable.model.getRowCount())
        #print("getColumnCount: ", self.currenttable.model.getColumnCount())
        #print("getRecordAtRow: ", self.currenttable.model.getRecordAtRow(0))

        for colname in self.currenttable.model.columnNames:
            print(self.currenttable.model.columnlabels[colname])

        # print(self.currenttable.model.columnlabels[0])
        # filtered_value_per_column = self.currenttable.model.filterBy(self.currenttable.model.columnlabels.value, "ciao")
        # print(filtered_value_per_column)

        #print("dictcolObservableEvents:", my_globals.dictcolObservableEvents)
        #print("dictcolControllableEvents:", my_globals.dictcolControllableEvents)



        #print("**************************************")

    def createMenuBar(self):
        """Create the menu bar for the application. """
        #print("createMenuBar")
        self.menu=Menu(self.tablesapp_win)
        self.proj_menu={'01New':{'cmd':self.new_project},
                        '02Open':{'cmd':self.open_project},
                        '03Import file on table(.txt,.fsa,.csv,.json)': {'cmd':self.import_file},
                        '04Analyze file(.txt,.fsa,.csv,.json)': {'cmd': self.just_analyze_file},
                        '05Close':{'cmd':self.close_project},
                        '06Save':{'cmd':self.save_project},
                        '07Save As':{'cmd':self.save_as_project},
                        '08Preferences..':{'cmd':self.showPrefsDialog},
                        '09Quit':{'cmd':self.quit}}
        if self.parent:
            self.proj_menu['08Return to Database']={'cmd':self.return_data}
        self.proj_menu=self.create_pulldown(self.menu,self.proj_menu)
        self.menu.add_cascade(label='Project',menu=self.proj_menu['var'])

        self.records_menu={'01Add Row':{'cmd':self.add_Row},
                         '02Delete Row':{'cmd':self.delete_Row},
                         '03Add Column':{'cmd':self.add_Column},
                         '04Delete Column':{'cmd':self.delete_Column},
                         '05Auto Add Rows':{'cmd':self.autoAdd_Rows},
                         '06Auto Add Columns':{'cmd':self.autoAdd_Columns},
                         '07Find':{'cmd':self.createSearchBar},
                         '08From table to Json': {'cmd': self.from_Table_To_Json},
                         '09Analyze FSA': {'cmd': self.analyze_FSA},
                         }
        self.records_menu=self.create_pulldown(self.menu,self.records_menu)
        self.menu.add_cascade(label='Records',menu=self.records_menu['var'])

        self.sheet_menu={'01Add Sheet':{'cmd':self.add_Sheet},
                         '02Remove Sheet':{'cmd':self.delete_Sheet},
                         '03Copy Sheet':{'cmd':self.copy_Sheet},
                         '04Rename Sheet':{'cmd':self.rename_Sheet},
                         }
        self.sheet_menu=self.create_pulldown(self.menu,self.sheet_menu)
        self.menu.add_cascade(label='Sheet',menu=self.sheet_menu['var'])

        self.IO_menu={'01Import from csv file':{'cmd':self.import_csv},
                      '02Export to csv file':{'cmd':self.export_csv},
                      }

        self.IO_menu=self.create_pulldown(self.menu,self.IO_menu)
        self.menu.add_cascade(label='Import/Export',menu=self.IO_menu['var'])

        # Help menu
        self.help_menu={'01Online Help':{'cmd':self.online_documentation},
                        '02About':{'cmd':self.about_Tables}}
        self.help_menu=self.create_pulldown(self.menu,self.help_menu)
        self.menu.add_cascade(label='Help',menu=self.help_menu['var'])

        self.tablesapp_win.config(menu=self.menu)

        return

    def create_pulldown(self,menu,dict):
        """ Create a pulldown in var from the info in dict  """
        #print("create_pulldown")
        var = Menu(menu,tearoff=0)
        items = dict.keys()
        #items.sort()
        for item in items:
            if item[-3:]=='sep':
                var.add_separator()
            else:
                # Do we have a command?
                command=None
                if 'cmd' in  dict[item]:
                    command=dict[item]['cmd']

                # Put the command in there
                if 'sc' in dict[item]:
                    var.add_command(label='%-25s %9s' %(item[2:],dict[item]['sc']),command=command)
                else:
                    var.add_command(label='%-25s' %(item[2:]),command=command)
        dict['var']=var
        return dict

    def createSearchBar(self, event=None):
        """Add a find entry box"""
        #print("createSearchBar")
        frame = Frame(self.tablesapp_win)
        row=0
        def close():
            frame.destroy()
        self.findtext=StringVar()
        self.findbox=Entry(frame,textvariable=self.findtext,width=30,bg='white')
        self.findbox.grid(row=row,column=1,sticky='news',columnspan=2,padx=2,pady=2)
        self.findbox.bind('<Return>',self.do_find_text)
        Label(frame,text='Find:').grid(row=row,column=0,sticky='ew')
        self.findagainbutton=Button(frame,text='Find Again', command=self.do_find_again)
        self.findagainbutton.grid(row=row,column=3,sticky='news',padx=2,pady=2)
        self.cbutton=Button(frame,text='Close', command=close)
        self.cbutton.grid(row=row,column=4,sticky='news',padx=2,pady=2)
        frame.pack(fill=BOTH, expand=NO)
        return

    def loadprefs(self):
        """Setup default prefs file if any of the keys are not present"""
        #print("loadprefs")
        defaultprefs = {'textsize':14,
                         'windowwidth': 800 ,'windowheight':600}
        for prop in defaultprefs.keys():
            try:
                self.preferences.get(prop)
            except:
                self.preferences.set(prop, defaultprefs[prop])

        return

    def showPrefsDialog(self):
        #print("showPrefsDialog")
        self.prefswindow = self.currenttable.showtablePrefs()
        return

    def new_project(self, data=None):
        """Create a new table, with model and add the frame"""
        #print("new_project")
        if hasattr(self,'currenttable'):
            self.notebook.destroy()
            self.currenttable.destroy()

        #Create the sheets dict
        self.sheets = {}
        self.notebook = Notebook(self.tablesapp_win)
        self.notebook.pack(fill='both', expand=1, padx=4, pady=4)
        if data !=None:
            for s in data.keys():
                sdata = data[s]
                try:
                    self.add_Sheet(s ,sdata)
                except:
                    print ('skipping')
        else:
            #do the table adding stuff for the initial sheet
            self.add_Sheet('sheet1')
        #self.notebook.setnaturalsize()
        return

    def open_project(self, filename=None):
        #print("open_project")
        if filename == None:
            filename=filedialog.askopenfilename(defaultextension='.tblprj"',
                                                      initialdir=os.getcwd(),
                                                      filetypes=[("TableApp project","*.tblprj"),
                                                                 ("All files","*.*")],
                                                      parent=self.tablesapp_win)
        if os.path.isfile(filename):
            fd = open(filename, 'rb')
            data = pickle.load(fd)
            fd.close()
        self.new_project(data)
        self.filename=filename
        return

    def save_project(self):
        #print("save_project")
        if not hasattr(self, 'filename'):
            self.save_as_project()
        elif self.filename == None:
            self.save_as_project()
        else:
            self.do_save_project(self.filename)

        return

    def save_as_project(self):
        """Save as a new filename"""
        #print("save_as_project")
        filename=filedialog.asksaveasfilename(parent=self.tablesapp_win,
                                                defaultextension='.tblprj',
                                                initialdir=self.defaultsavedir,
                                                filetypes=[("TableApp project","*.tblprj"),
                                                           ("All files","*.*")])
        if not filename:
            print ('Returning')
            return
        self.filename=filename
        self.do_save_project(self.filename)
        return

    def do_save_project(self, filename):
        """Get model dicts and write all to pickle file"""
        #print("do_save_project")
        data = {}
        for s in self.sheets.keys():
            currtable = self.sheets[s]
            model = currtable.getModel()
            data[s] = model.getData()

        fd=open(filename,'wb')
        pickle.dump(data,fd)
        fd.close()
        return




    # added by me ******************************************************************************************************
    def just_analyze_file(self, filename=None):
        """Just analyze the imported file description of the fsa (txt, .fsa, .json or .csv)"""
        if filename == None:
            filename = filedialog.askopenfilename(defaultextension='.txt',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[("Text files","*.txt"),
                                                             ("fsa files", "*.fsa"),
                                                             ("csv files","*.csv"),
                                                             ("json files","*.json"),
                                                             ("All files","*.*")],
                                                  parent=self.tablesapp_win)
        from fsatoolbox.fsa import fsa
        import analysis

        f = fsa.from_file(filename)

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
            is_reachable = analysis.get_reachability_info(f)

            for iter in range(len(X)):
                print(str(X[iter].label) + ".is_Reachable: " + str(X[iter].is_Reachable))
            print("The FSA is Reachable? :" + str(is_reachable))

            print("\n CO-REACHABILITY TEST:")
            is_co_reachable = analysis.get_co_reachability_info(f)

            for iter in range(len(X)):
                print(str(X[iter].label) + ".is_co_Reachable: " + str(X[iter].is_co_Reachable))
            print("The FSA is Co-Reachable? :" + str(is_co_reachable))

            print("\n BLOCKINGNESS TEST:")
            is_blocking = analysis.get_blockingness_info(f)

            for iter in range(len(X)):
                print(str(X[iter].label) + ".is_Blocking: " + str(X[iter].is_Blocking))
            print("The FSA is blocking? :" + str(is_blocking))

            print("\n TRIM TEST:")
            is_trim = f.get_trim_info()
            print("The FSA is trim? :" + str(is_trim))

            print("\n DEADNESS TEST:")
            analysis.get_deadness_info(f)

            for iter in range(len(X)):
                print(str(X[iter].label) + ".is_Dead: " + str(X[iter].is_Dead))

            print("\n REVERSIBILITY TEST:")
            is_reversible = analysis.get_reversibility_info(f)
            print("The FSA is reversible? :" + str(is_reversible))
        else:
            print("Error: At least the initial state must be specified.")

    # ******************************************************************************************************************




    # added by me ******************************************************************************************************
    def import_file(self, filename=None):
        """Import and place on the current table the content of a file of extension .txt, .csv or .json"""
        #print("import_file")
        if filename == None:
            filename = filedialog.askopenfilename(defaultextension='.txt',
                                                  initialdir=os.getcwd(),
                                                  filetypes=[("Text files","*.txt"),
                                                             ("fsa files", "*.fsa"),
                                                             ("csv files","*.csv"),
                                                             ("json files","*.json"),
                                                             ("All files","*.*")],
                                                  parent=self.tablesapp_win)
        if os.path.isfile(filename):
            extension = os.path.splitext(filename)
            #print("extension: ", extension)
            if ".txt" in extension:
                self.parse_txt_file_and_obtain_the_json(filename)
            elif ".json" in extension:
                self.parse_json_file_and_populate_the_table(filename)
            elif ".csv" in extension:
                self.parse_csv_file_and_populate_the_table(filename)



    # ******************************************************************************************************************



    # added by me ******************************************************************************************************
    def parse_txt_file_and_obtain_the_json(self, filename=None):
        """Parse the .txt file describing the fsa and convert it to a json file"""
        print("****************************************************************************************************************************")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("**                                          parse_txt_file_and_obtain_the_json                                            **")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("****************************************************************************************************************************")

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



        dict_start_states = {}  # to populate column 0 with keys (states), and for every key a dictionary of info on isInitial, isFinal, isFault
        list_start_states = []  # the indexes of the list represent the row of the related the start_state value
        num_states = 1
        list_events = []  # to populate columnlabels with keys (events), and for every key a dictionary of info on isObservable, isControllable
        dict_deltas = {}

        print("clean_lines: ", clean_lines)
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
                    #print("state")
                    current_start_state = str(clean_lines[iter_lines][0])
                    dict_start_states.update({current_start_state: {"row": index_row_start_states,
                                                                    "isInitial": clean_lines[iter_lines][1],
                                                                    "isFinal": clean_lines[iter_lines][2],
                                                                    "isForbidden": clean_lines[iter_lines][3]}})
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
                            dict_events.update({clean_lines[iter_lines][0]: {"column": index_column_events,
                                                                             "isControllable": clean_lines[iter_lines][2],
                                                                             "isObservable": clean_lines[iter_lines][3],
                                                                             "isFault": clean_lines[iter_lines][4]}})
                            list_events.append(clean_lines[iter_lines][0])
                            dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                          "name": clean_lines[iter_lines][0],
                                                                          "ends": clean_lines[iter_lines][1]}})
                            index_column_events += 1
                            index_delta_events += 1
                            #print("index_delta_events: ", index_delta_events)
                            #print("dict_events: ", dict_events)
                        else:
                            #print("event already present")
                            current_end_state = clean_lines[iter_lines][1]
                            current_event_end_states = current_end_state
                            for key in range(index_delta_events):
                                #print("key: ", key)
                                #print("current_event: ", clean_lines[iter_lines][0])
                                if (str(key) in dict_deltas) and dict_deltas[str(key)]["name"] == \
                                        clean_lines[iter_lines][0] and dict_deltas[str(key)][
                                    "start"] == current_start_state:
                                    #print("dict_deltas[str(" + str(key) + ")]:", dict_deltas[str(key)])
                                    current_event_end_states = current_event_end_states + "-" + dict_deltas[str(key)][
                                        "ends"]
                                    #print("current_event_end_states: ", current_event_end_states)
                                    del dict_deltas[str(key)]
                            dict_deltas.update({str(index_delta_events): {"start": current_start_state,
                                                                          "name": clean_lines[iter_lines][0],
                                                                          "ends": current_event_end_states}})
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
            # Create an instance of Tkinter frame
            win = Tk()
            # Set the geometry of Tkinter frame
            win.geometry("400x200")
            # win.aspect(70,70,70,70)
            Label(win, text="There is a sintax error in the .txt file you tried to import.\r\n"
                            "Click here if you want to see an example on how to\r\ncorrectly populate the file.",
                  font=('Helvetica 10 bold')).pack(pady=20)
            # Create a button in the main Window to open the popup
            ttk.Button(win, text="Example", command=self.open_popup_errors_on_txt_file).pack()
            win.mainloop()

        #print("dict_deltas: ", dict_deltas)
        print("-----------------------------------------------------------------------------------------------------")
        print("CHECK VALUES:\n")
        print("dict_start_states: ", dict_start_states)
        print("list_start_states: ", list_start_states)
        print("dict_events: ", dict_events)
        print("list_events: ", list_events)
        print("dict_deltas: ", dict_deltas)
        print("-----------------------------------------------------------------------------------------------------")

        #print("before fitting the table")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)
        # fit the table

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        #global dictcolControllableEvents
        #global dictcolObservableEvents
        #global dictcolFaultyEvents
        # from tkintertable.Tables import dictcolControllableEvents, dictcolObservableEvents, dictcolFaultyEvents
        my_globals.dictcolControllableEvents.clear()
        my_globals.dictcolObservableEvents.clear()
        my_globals.dictcolFaultyEvents.clear()
        #print("clear", self.currenttable.model.columnlabels)
        self.currenttable.model.addColumn("State")
        i = 1
        while len(self.currenttable.model.columnlabels) <= len(list_events):
            # self.currenttable.model.addColumn("name"+str(len(self.currenttable.model.columnlabels)))
            self.currenttable.model.addColumn(list_events[i - 1])
            print(self.currenttable.model.columnlabels)


            if dict_events[list_events[i - 1]]["isObservable"]:
                if dict_events[list_events[i - 1]]["isObservable"] == "o":
                    #print("o")
                    my_globals.setEventAsObservable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isObservable"] == "uo":
                    # print("uo")
                    my_globals.setEventAsUnobservable(self.currenttable, list_events[i - 1])
            else:
                #print("uo")
                my_globals.setEventAsUnobservable(self.currenttable, list_events[i - 1])

            if dict_events[list_events[i - 1]]["isControllable"]:
                if dict_events[list_events[i - 1]]["isControllable"] == "c":
                    #print("c")
                    my_globals.setEventAsControllable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isControllable"] == "uc":
                    # print("uc")
                    my_globals.setEventAsUncontrollable(self.currenttable, list_events[i - 1])
            else:
                #print("uc")
                my_globals.setEventAsUncontrollable(self.currenttable, list_events[i - 1])

            if dict_events[list_events[i - 1]]["isFault"]:
                if dict_events[list_events[i - 1]]["isFault"] == "f":
                    #print("c")
                    my_globals.setEventAsFaulty(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isFault"] == "uf":
                    # print("uc")
                    my_globals.setEventAsUnfaulty(self.currenttable, list_events[i - 1])
            else:
                #print("uc")
                my_globals.setEventAsUnfaulty(self.currenttable, list_events[i - 1])

            i += 1




        while self.currenttable.model.getRowCount() < len(list_start_states):
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(list_start_states):
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)



        # naming the columns with the events
        #print("before clear")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)

        # self.currenttable.resizeColumn(0, 100)
        # self.currenttable.model.columnlabels.clear()
        # self.currenttable.model.columnNames.clear() #PROBLEMATICO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #print("clear")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)



        # naming the rows of the column "States" with the start_states
        for i in range(len(list_start_states)):
            #print("i: ", i)


            str_check = ""
            if "isInitial" in dict_start_states[list_start_states[i]]:
                str_check += "_i"
            if "isFinal" in dict_start_states[list_start_states[i]]:
                str_check += "_f"
            if "isForbidden" in dict_start_states[list_start_states[i]]:
                str_check += "_p"

            def return_suffix(str_check):
                suffix = ""

                if str_check == "_i_f_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_i_f":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                elif str_check == "_i_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_f_p":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                elif str_check == "_i":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1":
                        suffix += "_i"
                elif str_check == "_f":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1":
                        suffix += "_f"
                elif str_check == "_p":
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                        suffix += "_p"
                return suffix


            self.currenttable.model.setValueAt(list_start_states[i]+return_suffix(str_check), i, 0)


            '''
            if dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i], i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_f_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_f", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_f_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_f", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_p", i, 0)
            '''
            #print("list_start_states[i]: ", list_start_states[i])

        print(self.currenttable.model.columnlabels)

        flag_parsed_dict_deltas = 0
        key_dict_deltas = 0
        counter_macro_deltas = 0
        # inserting records in the table cells
        while counter_macro_deltas < len(dict_deltas):
            if counter_macro_deltas >= len(dict_deltas):
                break
            if str(key_dict_deltas) in dict_deltas:
                #print("key_dict_deltas: ", key_dict_deltas)

                column_index = self.currenttable.model.getColumnIndex(dict_deltas[str(key_dict_deltas)]["name"])
                row_index = dict_start_states[dict_deltas[str(key_dict_deltas)]["start"]]["row"]
                #print("(row_index, column_index): ", row_index, column_index)
                #print("dict_deltas[str(key_dict_deltas)][event]: ", dict_deltas[str(key_dict_deltas)]["name"])
                #print("dict_deltas[str(key_dict_deltas)][end]: ", dict_deltas[str(key_dict_deltas)]["ends"])
                # self.currenttable.model.setValueAt(dict_deltas[str(key_dict_deltas)]["ends"], row_index, column_index)

                list_cell_value_end_states = dict_deltas[str(key_dict_deltas)]["ends"].split(";")
                #print("qui, list_cell_value_end_states: ", list_cell_value_end_states)
                i = 0
                while i < len(list_cell_value_end_states):
                    #print("i: ", i)
                    current_value = list_cell_value_end_states[i]
                    #print("current_value: ", current_value)
                    num_occurrences = list_cell_value_end_states.count(current_value)
                    #print("num_occurrences: ", num_occurrences)
                    while num_occurrences > 1:
                        list_cell_value_end_states.remove(current_value)
                        num_occurrences = list_cell_value_end_states.count(current_value)
                        i += 1
                        #print("i: ", i)
                    i += 1

                string_cell_value_end_states = " ".join(map(str, list_cell_value_end_states))
                #print("string_cell_value_end_states: ", string_cell_value_end_states)
                string_cell_value_end_states = re.sub(" +", ";", string_cell_value_end_states)
                self.currenttable.model.setValueAt(string_cell_value_end_states, row_index, column_index)
                #print("string_cell_value_end_states: ", string_cell_value_end_states)

                num_chars = len(string_cell_value_end_states)
                if num_chars >= 10:
                    width_col = 100 + (num_chars - 10) * 7
                    self.currenttable.resizeColumn(column_index, width_col)
                counter_macro_deltas += 1
                key_dict_deltas += 1
            else:
                key_dict_deltas += 1
                pass





        # in order to make the update of the table visible without the need to be touched before by the user
        self.currenttable.resizeColumn(0, 101)  # dummy resize
        self.currenttable.resizeColumn(0, 100)  # reset the width of col 0 to the default value

        # self.new_project(data)
        # self.filename=filename
        fd.close()
        return

    # ******************************************************************************************************************



    # added by me ******************************************************************************************************
    def parse_json_file_and_populate_the_table(self, filename=None):
        """Parse the .json file describing the fsa and populate the current table with its data"""

        #print("****************************************************************************************************************************")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("**                                          parse_json_file_and_populate_the_table                                        **")
        #print("**                                                                                                                        **")
        #print("**                                                                                                                        **")
        #print("****************************************************************************************************************************")

        with open(filename) as json_file:
            data = json.load(json_file)
        print(data)


        dict_deltas = {}


        dict_events = data["E"].copy()
        #print("dict_events: ", dict_events)
        iter = 0
        for key in dict_events:
            dict_events[key].update({"column": iter})
            iter += 1
        #print("dict_events: ", dict_events)

        dict_start_states = data["X"].copy()
        #print("dict_start_states: ", dict_start_states)
        iter = 0
        for key in dict_start_states:
            dict_start_states[key].update({"row": iter})
            iter += 1
        #print("dict_start_states: ", dict_start_states)



        list_start_states = []
        list_start_states = list(dict_start_states.keys())
        #print("list_start_states: ", list_start_states)

        list_events = []
        list_events = list(dict_events.keys())
        #print("list_events: ", list_events)


        dict_deltas = {}

        #print("dict_deltas: ", dict_deltas)
        iter = 0
        for key in data["delta"]:
            dict_deltas.update({str(iter): data["delta"][key]})
            iter += 1
        #print("dict_deltas: ", dict_deltas)

        list_keys_already_done = []
        dict_start_state_events_already_done = {}
        flag_time_to_delete = 0
        for current_key in range(len(dict_deltas)):
            if(str(current_key) in dict_deltas):
                current_start_state = dict_deltas[str(current_key)]["start"]
                current_event = dict_deltas[str(current_key)]["name"]
                current_ends = dict_deltas[str(current_key)]["ends"]
                list_keys_already_done.clear()
                # list_keys_already_done.append(current_key)
                flag_time_to_delete = 0
                for key in dict_deltas:
                    #print("current_key="+str(current_key)+", key="+str(key)+")")
                    #print("dict_deltas[str(key)]: ", dict_deltas[str(key)])
                    if dict_deltas[str(key)]["start"] == current_start_state and dict_deltas[str(key)]["name"] == current_event and key != str(current_key) and key not in list_keys_already_done and (dict_deltas[str(current_key)]["start"] not in dict_start_state_events_already_done and dict_deltas[str(current_key)]["name"] not in dict_start_state_events_already_done):
                        current_ends = current_ends + "-" + dict_deltas[str(key)]["ends"]
                        list_keys_already_done.append(key)
                        dict_start_state_events_already_done.update(dict_deltas[str(key)])
                        #print("dict_start_state_events_already_done: ", dict_start_state_events_already_done)
                        #print("list_keys_already_done at (current_key="+str(current_key)+", key="+str(key)+"): ", list_keys_already_done)
                        #print("dict_deltas[str(key)]: ", dict_deltas[str(key)])
                        # del dict_deltas[str(key)]
                        flag_time_to_delete = 1
                if (flag_time_to_delete == 1):
                    dict_deltas[str(current_key)]["ends"] = current_ends
                    #print("TO DELETE")
                    for i in range(len(list_keys_already_done)):
                        #print("i:", i)
                        del dict_deltas[list_keys_already_done[i]]
                        #print("dict_deltas: ", dict_deltas)




        #print("dict_deltas: ", dict_deltas)
        #print("dict_start_states: ", dict_start_states)
        #print("list_start_states: ", list_start_states)
        #print("dict_events: ", dict_events)
        #print("list_events: ", list_events)
        #print("dict_deltas: ", dict_deltas)

        #print("before fitting the table")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)
        # fit the table

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        #global dictcolControllableEvents
        #global dictcolObservableEvents
        #global dictcolFaultyEvents
        # from tkintertable.Tables import dictcolControllableEvents, dictcolObservableEvents, dictcolFaultyEvents

        my_globals.dictcolControllableEvents.clear()
        my_globals.dictcolObservableEvents.clear()
        my_globals.dictcolFaultyEvents.clear()
        #print("clear", self.currenttable.model.columnlabels)
        self.currenttable.model.addColumn("State")
        i = 1
        while len(self.currenttable.model.columnlabels) <= len(list_events):
            # self.currenttable.model.addColumn("name"+str(len(self.currenttable.model.columnlabels)))
            self.currenttable.model.addColumn(list_events[i - 1])
            print(self.currenttable.model.columnlabels)

            from tkintertable.Tables import TableCanvas
            if "isObservable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isObservable"] == "1" or dict_events[list_events[i - 1]]["isObservable"] == 1:
                    #print("o")
                    my_globals.setEventAsObservable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isObservable"] == "0" or dict_events[list_events[i - 1]]["isObservable"] == 0:
                    # print("uo")
                    my_globals.setEventAsUnobservable(self.currenttable, list_events[i - 1])
            else:
                #print("uo")
                my_globals.setEventAsUnobservable(self.currenttable, list_events[i - 1])

            if "isControllable" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isControllable"] == "1" or dict_events[list_events[i - 1]]["isControllable"] == 1:
                    #print("c")
                    my_globals.setEventAsControllable(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isControllable"] == "0" or dict_events[list_events[i - 1]]["isControllable"] == 0:
                    # print("uc")
                    my_globals.setEventAsUncontrollable(self.currenttable, list_events[i - 1])
            else:
                #print("uc")
                my_globals.setEventAsUncontrollable(self.currenttable, list_events[i - 1])

            if "isFault" in dict_events[list_events[i - 1]]:
                if dict_events[list_events[i - 1]]["isFault"] == "1" or dict_events[list_events[i - 1]]["isFault"] == 1:
                    #print("c")
                    my_globals.setEventAsFaulty(self.currenttable, list_events[i - 1])
                elif dict_events[list_events[i - 1]]["isFault"] == "0" or dict_events[list_events[i - 1]]["isFault"] == 0:
                    # print("uc")
                    my_globals.setEventAsUnfaulty(self.currenttable, list_events[i - 1])
            else:
                #print("uc")
                my_globals.setEventAsUnfaulty(self.currenttable, list_events[i - 1])

            i += 1

        while self.currenttable.model.getRowCount() < len(list_start_states):
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(list_start_states):
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)



        # naming the columns with the events
        #print("before clear")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)

        #self.currenttable.resizeColumn(0, 100)
        # self.currenttable.model.columnlabels.clear()
        # self.currenttable.model.columnNames.clear() #PROBLEMATICO !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #print("clear")
        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
        #print("self.currenttable.model.columnNames:", self.currenttable.model.columnNames)



        # naming the rows of the column "States" with the start_states
        for i in range(len(list_start_states)):
            #print("i: ", i)

            str_check = ""
            if "isInitial" in dict_start_states[list_start_states[i]]:
                str_check += "_i"
            if "isFinal" in dict_start_states[list_start_states[i]]:
                str_check += "_f"
            if "isForbidden" in dict_start_states[list_start_states[i]]:
                str_check += "_p"

            def return_suffix(str_check):
                suffix = ""

                if str_check == "_i_f_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_i_f":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                elif str_check == "_i_p":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_f_p":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                elif str_check == "_i":
                    if dict_start_states[list_start_states[i]]["isInitial"] == "1" or dict_start_states[list_start_states[i]]["isInitial"] == 1:
                        suffix += "_i"
                elif str_check == "_f":
                    if dict_start_states[list_start_states[i]]["isFinal"] == "1" or dict_start_states[list_start_states[i]]["isFinal"] == 1:
                        suffix += "_f"
                elif str_check == "_p":
                    if dict_start_states[list_start_states[i]]["isForbidden"] == "1" or dict_start_states[list_start_states[i]]["isForbidden"] == 1:
                        suffix += "_p"
                return suffix


            self.currenttable.model.setValueAt(list_start_states[i]+return_suffix(str_check), i, 0)

            '''
            if dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i], i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_f_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_f", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_f_p", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "1" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_i", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "1" and dict_start_states[list_start_states[i]]["isForbidden"] == "0":
                self.currenttable.model.setValueAt(list_start_states[i] + "_f", i, 0)
            elif dict_start_states[list_start_states[i]]["isInitial"] == "0" and dict_start_states[list_start_states[i]][
                "isFinal"] == "0" and dict_start_states[list_start_states[i]]["isForbidden"] == "1":
                self.currenttable.model.setValueAt(list_start_states[i] + "_p", i, 0)
            '''
            #print("list_start_states[i]: ", list_start_states[i])

        #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)





        flag_parsed_dict_deltas = 0
        key_dict_deltas = 0
        counter_macro_deltas = 0
        column_index = 0
        row_index = 0
        # inserting records in the table cells
        while counter_macro_deltas < len(dict_deltas):
            if counter_macro_deltas >= len(dict_deltas):
                break
            if str(key_dict_deltas) in dict_deltas:
                #print("key_dict_deltas: ", key_dict_deltas)

                column_index = self.currenttable.model.getColumnIndex(dict_deltas[str(key_dict_deltas)]["name"])
                row_index = dict_start_states[dict_deltas[str(key_dict_deltas)]["start"]]["row"]
                #print("(row_index, column_index): ", row_index, column_index)
                #print("dict_deltas[str(key_dict_deltas)][name]: ", dict_deltas[str(key_dict_deltas)]["name"])
                #print("dict_deltas[str(key_dict_deltas)][ends]: ", dict_deltas[str(key_dict_deltas)]["ends"])
                # self.currenttable.model.setValueAt(dict_deltas[str(key_dict_deltas)]["ends"], row_index, column_index)

                list_cell_value_end_states = dict_deltas[str(key_dict_deltas)]["ends"].split("-")
                #print("qui, list_cell_value_end_states: ", list_cell_value_end_states)
                i = 0

                #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
                #print("self.currenttable.model.columnNames: ", self.currenttable.model.columnNames)

                while i < len(list_cell_value_end_states):
                    #print("i: ", i)
                    current_value = list_cell_value_end_states[i]
                    #print("current_value: ", current_value)
                    num_occurrences = list_cell_value_end_states.count(current_value)
                    #print("num_occurrences: ", num_occurrences)
                    while num_occurrences > 1:
                        list_cell_value_end_states.remove(current_value)
                        num_occurrences = list_cell_value_end_states.count(current_value)
                        i += 1
                        #print("i: ", i)
                    i += 1

                string_cell_value_end_states = " ".join(map(str, list_cell_value_end_states))
                #print("string_cell_value_end_states: ", string_cell_value_end_states)
                string_cell_value_end_states = re.sub(" +", "-", string_cell_value_end_states)
                self.currenttable.model.setValueAt(string_cell_value_end_states, row_index, column_index)
                #print("string_cell_value_end_states: ", string_cell_value_end_states)

                #print("column_index: ", column_index)
                #print("get_column_Name", self.currenttable.model.getColumnName(column_index))
                num_chars = len(string_cell_value_end_states)
                if num_chars >= 10:
                    #print("self.currenttable.model.columnlabels: ", self.currenttable.model.columnlabels)
                    #print("self.currenttable.model.columnNames: ", self.currenttable.model.columnNames)
                    #print("column_index: ", column_index)
                    #print("get_column_Name", self.currenttable.model.getColumnName(column_index))
                    width_col = 100 + (num_chars - 10) * 7
                    self.currenttable.resizeColumn(column_index, width_col)
                counter_macro_deltas += 1
                key_dict_deltas += 1
            else:
                key_dict_deltas += 1
                pass


        # in order to make the update of the table visible without the need to be touched before by the user
        self.currenttable.resizeColumn(0, 101)  # dummy resize
        self.currenttable.resizeColumn(0, 100)  # reset the width of col 0 to the default value

        # self.new_project(data)
        # self.filename=filename

        json_file.close()
        return

    # ******************************************************************************************************************



    # added by me ******************************************************************************************************
    def parse_csv_file_and_populate_the_table(self, filename=None):
        """Parse the .csv file describing the fsa and populate the current table"""

        print("****************************************************************************************************************************")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("**                                          parse_csv_file_and_populate_the_table                                         **")
        print("**                                                                                                                        **")
        print("**                                                                                                                        **")
        print("****************************************************************************************************************************")

        with open(filename, encoding='utf-8') as csvf:
            fd = open(filename, mode='rt')
            lines = fd.readlines()

        print(lines)



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


        # print clean_lines
        for row in range(1, len(clean_lines)):
            for col in range(0, len(clean_lines[0])):
                print("(row, col): ("+str(row)+","+str(col)+")"+": "+str(clean_lines[row][col]))
                pass


        # fit the table

        self.currenttable.model.columnNames.clear()
        self.currenttable.model.columnlabels.clear()
        #global dictcolControllableEvents
        #global dictcolObservableEvents
        #global dictcolFaultyEvents
        # from tkintertable.Tables import dictcolControllableEvents, dictcolObservableEvents, dictcolFaultyEvents

        my_globals.dictcolControllableEvents.clear()
        my_globals.dictcolObservableEvents.clear()
        my_globals.dictcolFaultyEvents.clear()
        #print("clear", self.currenttable.model.columnlabels)
        self.currenttable.model.addColumn("State")


        dict_event_properties = {}
        # events properties, row 0

        i = 1
        for i in range(1,len(clean_lines[0])):
            current_event = clean_lines[0][i]
            if clean_lines[0][i] and clean_lines[0][i] != '_':
                if current_event.endswith("_uc_f_uo") or current_event.endswith("_uc_uo_f") or current_event.endswith(
                        "_f_uc_uo") or current_event.endswith("_f_uo_uc") or current_event.endswith(
                        "_uo_f_uc") or current_event.endswith("_uo_uc_f"):
                    string_lenght = len(current_event)
                    substring_to_remove = current_event[-6:]
                    current_event = current_event.replace(str(substring_to_remove), "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_uc_f"):
                    current_event = current_event.replace("_uc_f", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_f_uc"):
                    current_event = current_event.replace("_f_uc", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 1}})
                elif current_event.endswith("_uc_uo"):
                    current_event = current_event.replace("_uc_uo", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_uo_uc"):
                    current_event = current_event.replace("_uo_uc", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_uo_f"):
                    current_event = current_event.replace("_uo_f", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_f_uo"):
                    current_event = current_event.replace("_f_uo", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_uc"):
                    current_event = current_event.replace("_uc", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 0, "isFault": 0}})
                elif current_event.endswith("_f"):
                    current_event = current_event.replace("_f", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 1}})
                elif current_event.endswith("_uo"):
                    current_event = current_event.replace("_uo", "")
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 0, "isControllable": 1, "isFault": 0}})
                else:
                    current_event.replace(" ", "")
                    dict_event_properties.update({current_event: {"isObservable": 1, "isControllable": 1, "isFault": 0}})
                #print("current_event: ", current_event)

            #print("dict_event_properties: ", dict_event_properties)
            clean_lines[0][i] = current_event
            self.currenttable.model.addColumn(current_event)

            if "isObservable" in dict_event_properties[current_event]:
                if dict_event_properties[current_event]["isObservable"] == 1:
                    #print("o")
                    my_globals.setEventAsObservable(self.currenttable, current_event)
                elif dict_event_properties[current_event]["isObservable"] == 0:
                    # print("uo")
                    my_globals.setEventAsUnobservable(self.currenttable, current_event)
            else:
                #print("uo")
                my_globals.setEventAsUnobservable(self.currenttable, current_event)

            if "isControllable" in dict_event_properties[current_event]:
                if dict_event_properties[current_event]["isControllable"] == 1:
                    #print("c")
                    my_globals.setEventAsControllable(self.currenttable, current_event)
                elif dict_event_properties[current_event]["isControllable"] == 0:
                    # print("uc")
                    my_globals.setEventAsUncontrollable(self.currenttable, current_event)
            else:
                #print("uc")
                my_globals.setEventAsUncontrollable(self.currenttable, current_event)

            if "isFault" in dict_event_properties[current_event]:
                if dict_event_properties[current_event]["isFault"] == 1:
                    #print("c")
                    my_globals.setEventAsFaulty(self.currenttable, current_event)
                elif dict_event_properties[current_event]["isFault"] == 0:
                    # print("uc")
                    my_globals.setEventAsUnfaulty(self.currenttable, current_event)
            else:
                #print("uc")
                my_globals.setEventAsUnfaulty(self.currenttable, current_event)



        #print("dict_event_properties: ", dict_event_properties)



        # adding or deleting rows
        while self.currenttable.model.getRowCount() < len(clean_lines)-1:
            self.currenttable.model.addRow()

        while self.currenttable.model.getRowCount() > len(clean_lines)-1:
            self.currenttable.model.deleteRow(self.currenttable.model.getRowCount() - 1)


        # print clean_lines
        for row in range(0, len(clean_lines)):
            for col in range(0, len(clean_lines[0])):
                #print("(row, col): ("+str(row)+","+str(col)+")"+": "+str(clean_lines[row][col]))
                pass

        # populating the table
        for row in range(1, len(clean_lines)):
            for col in range(0, len(clean_lines[0])):
                #print("row, col): ("+str(row)+","+str(col)+")"+": "+str(clean_lines[row][col]))
                self.currenttable.model.setValueAt(clean_lines[row][col], row-1, col)
                if len(clean_lines[row][col]) >= 10:
                    width_col = 100 + (len(clean_lines[row][col]) - 10) * 7
                    self.currenttable.resizeColumn(col, width_col)

        # in order to make the update of the table visible without the need to be touched before by the user
        self.currenttable.resizeColumn(0, 101)  # dummy resize
        self.currenttable.resizeColumn(0, 100)  # reset the width of col 0 to the default value

        fd.close()


        print("---------------------------------------------------------------------------------------------------------")
        print("dict_event_properties: ", dict_event_properties)
        print("---------------------------------------------------------------------------------------------------------")


        return

    # ******************************************************************************************************************



    # TODO open_popup_errors_on_txt_file, vedi backup 4 in questa riga
    '''
    # added by me ******************************************************************************************************

    def open_popup_errors_on_txt_file(self, win=None):
        """Open popup if some errors are present on the .txt file describing the fsa"""

        #self.error_win=Toplevel(win)
        #self.error_win.geometry('+100+350')
        #self.error_win.title('About TablesApp')
        #self.error_win.resizable(True, True)

        from tkintertable import Table_images

        # img = PhotoImage(format='png', file='./popup_example_how_to_populate_the_txt_file.png')

        # Create an instance of tkinter frame
        #self.example_win = Tk()
        self.example_win = Toplevel(win)

        # Set the geometry of tkinter frame
        self.example_win.geometry("1200x670")
        self.example_win.title("Example: how to populate a .txt description file of the FSA")
        # Create a canvas
        canvas = Canvas(self.example_win, width=1200, height=670)
        canvas.pack()
        # Load an image in the script
        img = (PIL.Image.open("./popup_example_how_to_populate_the_txt_file.png"))

        # Resize the Image using resize method
        resized_image = img.resize((1200, 670), PIL.Image.LANCZOS)
        new_image = PIL.ImageTk.PhotoImage(resized_image)

        # Add image to the Canvas Items
        canvas.create_image(10, 10, anchor=NW, image=new_image)

        self.example_win.mainloop()


        # create the text widget
        #text = Text(self.ab_win, height=900, width=2800)
        #text.grid(row=0, column=0, sticky='ew')

        # create a scrollbar widget and set its command to the text widget
        #scrollbar = ttk.Scrollbar(self.ab_win, orient='vertical', command=text.yview)
        #scrollbar.grid(row=0, column=2700, sticky='ns')

        #  communicate back to the scrollbar
        #text['yscrollcommand'] = scrollbar.set

        return

    # ******************************************************************************************************************
    '''





    # added by me ******************************************************************************************************

    def from_txt_file_to_current_table(self, filename=None):
        """Parse a file of extension .txt and place the extracted FSA on the current table"""

        #print("from_txt_file_content_to_current_table")


    # ******************************************************************************************************************


    def close_project(self):
        #print("close_project")
        if hasattr(self,'currenttable'):
            #self.notebook.destroy()
            self.currenttable.destroy()
        return

    def import_csv(self):
        #print("import_csv")
        importer = TableImporter()
        #just use the dialog to load and import the file
        importdialog = importer.import_Dialog(self.tablesapp_win)
        self.tablesapp_win.wait_window(importdialog)
        model = TableModel()
        model.importDict(importer.data)
        sheetdata = {}
        sheetdata['sheet1'] = model.getData()
        self.new_project(sheetdata)
        return

    def export_csv(self):
        #print("export_csv")
        from tkintertable.Tables_IO import TableExporter
        exporter = TableExporter()
        exporter.ExportTableData(self.currenttable)
        return

    def add_Sheet(self, sheetname=None, sheetdata=None):
        """Add a new sheet - handles all the table creation stuff"""
        #print("add_Sheet")
        def checksheet_name(name):
            if name == '':
                messagebox.showwarning("Whoops", "Name should not be blank.")
                return 0
            if name in self.sheets:
                messagebox.showwarning("Name exists", "Sheet name already exists!")
                return 0
        names = [self.notebook.tab(i, "text") for i in self.notebook.tabs()]
        noshts = len(names)
        if sheetname == None:
            sheetname = simpledialog.askstring("New sheet name?", "Enter sheet name:",
                                                initialvalue='sheet'+str(noshts+1))
        checksheet_name(sheetname)
        page = Frame(self.notebook)
        self.notebook.add(page, text=sheetname)
        #Create the table and model if data present
        if sheetdata != None:
            model = TableModel(sheetdata)
            self.currenttable = MyTable(page, model)
        else:
            self.currenttable = MyTable(page)

        #Load preferences into table
        self.currenttable.loadPrefs(self.preferences)
        #This handles all the canvas and header in the frame passed to constructor
        self.currenttable.createTableFrame()
        #add the table to the sheet dict
        self.sheets[sheetname] = self.currenttable
        self.saved = 0
        return sheetname

    def delete_Sheet(self):
        """Delete a sheet"""
        #print("delete_Sheet")
        s = self.notebook.index(self.notebook.select())
        name = self.notebook.tab(s, 'text')
        #self.notebook.delete(s)
        self.notebook.forget(s)
        del self.sheets[s]
        return

    def copy_Sheet(self, newname=None):
        """Copy a sheet"""
        #print("copy_Sheet")
        newdata = self.currenttable.getModel().getData().copy()
        if newname==None:
            self.add_Sheet(None, newdata)
        else:
            self.add_Sheet(newname, newdata)
        return

    def rename_Sheet(self):
        """Rename a sheet"""
        #print("rename_Sheet")
        #s = self.notebook.getcurselection()
        s = self.notebook.index(self.notebook.select())
        newname = simpledialog.askstring("New sheet name?", "Enter new sheet name:",
                                                initialvalue=s)
        if newname == None:
            return
        self.copy_Sheet(newname)
        self.delete_Sheet()
        return

    def setcurrenttable(self, event):
        """Set the currenttable so that menu items work with visible sheet"""
        #print("setcurrenttable")
        try:
            #s = self.notebook.getcurselection()
            s = self.notebook.index(self.notebook.select())
            self.currenttable = self.sheets[s]
        except:
            pass
        return

    def add_Row(self):
        """Add a new row"""
        #print("add_Row")
        self.currenttable.addRow()
        self.saved = 0
        return

    def delete_Row(self):
        """Delete currently selected row"""
        #print("delete_Row")
        self.currenttable.deleteRow()
        self.saved = 0
        return

    def add_Column(self):
        """Add a new column"""
        #print("add_Column")
        self.currenttable.addColumn()
        self.saved = 0
        return

    def delete_Column(self):
        """Delete currently selected column in table"""
        #print("delete_Column")
        self.currenttable.deleteColumn()
        self.saved = 0
        return

    # added by me ******************************************************************************************************
    def from_Table_To_Json(self):
        """Convert the current table content into a Json file"""
        #self.print_some_table_value_test()
        my_globals.fromTableToJson(self.currenttable)

        self.saved = 0
        return
    # ******************************************************************************************************************

    # added by me ******************************************************************************************************
    def analyze_FSA(self):
        """Convert the current table content into a Json file"""
        my_globals.analyzeFsa(self.currenttable)

        self.saved = 0
        return
    # ******************************************************************************************************************



    def autoAdd_Rows(self):
        """Auto add x rows"""
        #print("autoAdd_Rows")
        self.currenttable.autoAddRows()
        self.saved = 0
        return

    def autoAdd_Columns(self):
        """Auto add x rows"""
        #print("autoAdd_Columns")
        self.currenttable.autoAddColumns()
        self.saved = 0
        return

    def findValue(self):
        #print("findValue")
        self.currenttable.findValue()
        return

    def do_find_text(self, event=None):
        """Find the text in the table"""
        #print("do_find_text")
        if not hasattr(self,'currenttable'):
            return
        import string
        if string.strip(self.findtext.get())=='':
            return
        searchstring=self.findtext.get()
        if self.currenttable!=None:
            self.currenttable.findValue(searchstring)
        return

    def do_find_again(self, event=None):
        """Find again"""
        #print("do_find_again")
        if not hasattr(self,'currenttable'):
            return
        searchstring=self.findtext.get()
        if self.currenttable!=None:
            self.currenttable.findValue(searchstring, findagain=1)
        return

    def plot(self, event=None):
        #print("plot")
        self.currenttable.plotSelected()
        return

    def plotSetup(self, event=None):
        #print("plotSetup")
        self.currenttable.plotSetup()
        return

    def about_Tables(self):
        #print("about_Tables")
        self.ab_win=Toplevel()
        self.ab_win.geometry('+100+350')
        self.ab_win.title('About TablesApp')

        from tkintertable import Table_images
        logo = Table_images.tableapp_logo()
        label = Label(self.ab_win,image=logo)
        label.image = logo
        label.grid(row=0,column=0,sticky='news',padx=5,pady=5)

        text=['Tables Sample App ','Shows the use of Tablecanvas class for tkinter',
                'Copyright (C) Damien Farrell 2008-', 'This program is free software; you can redistribute it and/or',
                'modify it under the terms of the GNU General Public License',
                'as published by the Free Software Foundation; either version 2',
                'of the License, or (at your option) any later version.']
        row=1
        for line in text:
            tmp=Label(self.ab_win,text=line)
            tmp.grid(row=row,column=0,sticky='news',padx=4)
            row=row+1
        return

    def online_documentation(self,event=None):
        """Open the online documentation"""
        #print("online_documentation")
        import webbrowser
        link='http://sourceforge.net/projects/tkintertable/'
        webbrowser.open(link,autoraise=bool(1))
        return

    def quit(self):
        #print("quit")
        self.tablesapp_win.destroy()

        return

class ToolBar(Frame):
    """Uses the parent instance to provide the functions"""

    def __init__(self, parent=None, parentapp=None):
        #print("ToolBar__init__")
        Frame.__init__(self, parent, width=600, height=40)
        from tkintertable import Table_images
        self.parentframe = parent
        self.parentapp = parentapp
        #add buttons
        '''
        img = Table_images.new_proj()
        self.add_button('New Project', self.parentapp.new_project, img)
        img = Table_images.open_proj()
        self.add_button('Open Project', self.parentapp.open_project, img)
        img = Table_images.open_proj()
        self.add_button('Import file', self.parentapp.import_file, img)
        img = Table_images.save_proj()
        self.add_button('Save Project', self.parentapp.save_project, img)
        img = Table_images.add_row()
        self.add_button('Add record', self.parentapp.add_Row, img)
        img = Table_images.add_col()
        self.add_button('Add col', self.parentapp.add_Column, img)
        img = Table_images.del_row()
        self.add_button('Delete record', self.parentapp.delete_Row, img)
        img = Table_images.del_col()
        self.add_button('Delete col', self.parentapp.delete_Column, img)
        img = Table_images.plot()
        self.add_button('Plot', self.parentapp.plot, img)
        img = Table_images.plotprefs()
        self.add_button('Plot Prefs', self.parentapp.plotSetup, img)
        '''
        # added by me **************************************************************************************************
        try:
            img = my_globals.from_table_to_json()
            self.add_button('From table to json', self.parentapp.from_Table_To_Json, img)
            img = my_globals.analyze_fsa()
            self.add_button('Analyze FSA', self.parentapp.analyze_FSA, img)
        except:
            #print("errore button from table to json, in main.py, line 1739")
            pass
        # **************************************************************************************************************
        return

    def add_button(self, name, callback, img=None):
        #print("add_button")
        if img==None:
            b = Button(self, text=name, command=callback)
        else:
            b = Button(self, text=name, command=callback,
                             image=img)
        b.image = img
        b.pack(side=LEFT, padx=2, pady=2, ipadx=1, ipady=1)

        return





# Main function, run when invoked as a stand-alone Python program.

def main():
    "Run the application"
    import sys, os
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="tablefile",
                        help="Open a table file", metavar="FILE")
    opts, remainder = parser.parse_args()
    if opts.tablefile != None:
        app=TablesApp(datafile=opts.tablefile)
    else:
        app=TablesApp()


    app.mainloop()
    return

if __name__ == '__main__':
    my_globals.initialize()
    main()










# TEST PROGETTO ############################################################################################################




'''
from fsatoolbox.fsa import fsa
import pandas as pd


# X = []  # States
# E = []  # Alphabet
# x0 = []  # Initial states
# Xm = []  # Final states
# delta = pd.DataFrame()
# f = FSA(X,E,delta,x0,Xm)


f = fsa()

# f.from_file('file_co-reach-for-Xm.json')
f.from_file('file.json')


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

#filtered_delta = f.filter_delta(start='x2', transition=None, end=None)


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



#print("\nfiltered delta: \n", filtered_delta)


#print(filtered_delta.end)
#print("len is:", len(filtered_delta.end))
#print(str(filtered_delta.end))
#print(filtered_delta.index)
#print(filtered_delta.index[1])

#for iter in range(len(filtered_delta)):
    #print(filtered_delta.end[filtered_delta.index[iter]])

#print(isinstance(str(filtered_delta.transition[0]), (str)))

'''























# other things *********************************************************************************************************




'''
import tkinter as tk

window = tk.Tk()

for i in range(5):
    for j in range(5):
        frame = tk.Frame(
            master=window,
            relief=tk.RAISED,
            borderwidth=0.3
        )

        frame.grid(row=i, column=j, padx=5, pady=5)
        # ent_temperature = tk.Entry(master=frame, width=10)
        label = tk.Entry(master=frame, width=10)
        #label = tk.Label(master=frame, text=f"Row {i}/nColumn {j}")
        label.pack(padx=5, pady=5)


window.mainloop()
'''



'''
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
    """Open a file for editing."""
    filepath = askopenfilename(
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if not filepath:
        return
    txt_edit.delete("1.0", tk.END)
    with open(filepath, mode="r", encoding="utf-8") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text)
    window.title(f"Simple Text Editor - {filepath}")

def save_file():
    """Save the current file as a new file."""
    filepath = asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
    )
    if not filepath:
        return
    with open(filepath, mode="w", encoding="utf-8") as output_file:
        text = txt_edit.get("1.0", tk.END)
        output_file.write(text)
    window.title(f"Simple Text Editor - {filepath}")

window = tk.Tk()
window.title("Simple Text Editor")

window.rowconfigure(0, minsize=800, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, sticky="nsew")

window.mainloop()

'''





#!/usr/bin/env python
"""
    Sample App to illustrate table functionality.
    Created January 2008
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 2
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""




'''
# import pandas as pd
import json
import pandas as pd

# list of strings
lst = ['Geeks', 'For', 'Geeks', 'is', 'portal', 'for', 'Geeks']



# Calling DataFrame constructor on list
df = pd.DataFrame(lst)
print(df)
'''